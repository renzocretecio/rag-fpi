from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from app.core.config import settings
from app.db.postgres import database
from app.services.embeddings import embedding_service

ALLOWED_SOURCE_TYPES = [
    "about",
    "experience",
    "hobbies",
    "contact",
    "tech-stack",
    "projects",
]


def main() -> None:
    question = "Who are you?"
    query_embedding = embedding_service.embed_text_sync(question)

    database.database_url = settings.DATABASE_URL
    database.connect()
    try:
        rows = database.fetch(
            """
            select
                id::text,
                content,
                coalesce(metadata, '{}'::jsonb) as metadata,
                1 - (embedding <=> %s::vector) as similarity
            from public.chunks
            where metadata->>'source_type' = any(%s)
            order by embedding <=> %s::vector
            limit %s;
            """,
            query_embedding,
            ALLOWED_SOURCE_TYPES,
            query_embedding,
            5,
        )
    finally:
        database.disconnect()

    print(f"Question: {question}")
    print(f"Allowed source types: {', '.join(ALLOWED_SOURCE_TYPES)}")
    print(f"Matches: {len(rows)}")
    for i, row in enumerate(rows, start=1):
        print(f"\n{i}. similarity={float(row['similarity']):.4f}")
        print(f"id={row['id']}")
        print(f"content={row['content'][:300]}")
        print(f"metadata={row['metadata']}")


if __name__ == "__main__":
    main()