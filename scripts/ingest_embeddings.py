from __future__ import annotations

import asyncio
from typing import Any

import asyncpg
import httpx

from app.core.config import settings


BATCH_SIZE = 100


async def get_pending_chunks(conn: asyncpg.Connection, limit: int = BATCH_SIZE):
    sql = """
        select id, content
        from public.chunks
        where embedding is null
        order by id
        limit $1;
    """
    return await conn.fetch(sql, limit)


async def generate_embeddings(texts: list[str]) -> list[list[float]]:
    url = f"{settings.OLLAMA_URL.rstrip('/')}/api/embed"
    payload = {
        "model": settings.OLLAMA_EMBED_MODEL,
        "input": texts,
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        data: dict[str, Any] = response.json()

    embeddings = data.get("embeddings")
    if not isinstance(embeddings, list):
        raise RuntimeError("Invalid embedding response from Ollama")

    return embeddings


async def update_embeddings(
    conn: asyncpg.Connection,
    chunk_ids: list[str],
    embeddings: list[list[float]],
):
    sql = """
        update public.chunks
        set embedding = $1::vector
        where id = $2;
    """
    async with conn.transaction():
        for chunk_id, embedding in zip(chunk_ids, embeddings):
            await conn.execute(sql, embedding, chunk_id)


async def main() -> None:
    conn = await asyncpg.connect(dsn=settings.DATABASE_URL)
    total = 0
    try:
        while True:
            rows = await get_pending_chunks(conn)
            if not rows:
                break

            chunk_ids = [str(row["id"]) for row in rows]
            texts = [row["content"] for row in rows]

            embeddings = await generate_embeddings(texts)
            await update_embeddings(conn, chunk_ids, embeddings)

            total += len(chunk_ids)
            print(f"Updated {len(chunk_ids)} chunks, total {total}")

        print(f"Done. Embedded {total} chunks.")
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(main())