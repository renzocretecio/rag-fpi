from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import asyncpg

from app.core.config import settings


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
        self.database_url = settings.SUPABASE_URL

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

        try:
            conn = await asyncpg.connect(self.database_url)
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