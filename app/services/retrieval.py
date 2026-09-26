from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

import asyncpg
from pgvector.asyncpg import register_vector

from app.core.config import settings
from app.db.postgres import is_pooled_connection


@dataclass
class RetrievedChunk:
    id: str
    content: str
    metadata: dict[str, Any]
    similarity: float


class RetrievalServiceError(Exception):
    pass


class RetrievalService:
    def __init__(self) -> None:
        self.database_url = settings.DATABASE_URL

    async def match_chunks(
        self,
        query_embedding: list[float],
        match_count: int = 5,
    ) -> list[RetrievedChunk]:
        sql = """
            select
                id::text,
                content,
                coalesce(metadata, '{}'::jsonb) as metadata,
                1 - (embedding <=> $1::vector) as similarity
            from public.chunks
            order by embedding <=> $1::vector
            limit $2;
        """

        connect_kwargs: dict[str, Any] = {}
        if is_pooled_connection(self.database_url):
            # PgBouncer runs in transaction mode on pooled endpoints (Neon
            # `-pooler`), so asyncpg's server-side statement cache must be off.
            connect_kwargs["statement_cache_size"] = 0

        try:
            conn = await asyncpg.connect(self.database_url, **connect_kwargs)
            await register_vector(conn)
            # asyncpg returns json/jsonb as text unless a codec is registered.
            await conn.set_type_codec(
                "jsonb",
                encoder=json.dumps,
                decoder=json.loads,
                schema="pg_catalog",
            )
            rows = await conn.fetch(sql, query_embedding, match_count)
            await conn.close()
        except Exception as exc:
            raise RetrievalServiceError(f"Vector search failed: {exc}") from exc

        return [
            RetrievedChunk(
                id=row["id"],
                content=row["content"],
                metadata=dict(row["metadata"]),
                similarity=float(row["similarity"]),
            )
            for row in rows
        ]


retrieval_service = RetrievalService()