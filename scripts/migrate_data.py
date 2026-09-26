from __future__ import annotations

import os
import sys
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from app.core.config import settings
from scripts.init_db import apply_schema

# The old Supabase project runs Postgres 17, which a local pg_dump 16 refuses to
# dump. Copying the rows with psycopg2 avoids that version mismatch entirely and
# keeps ids, created_at and embeddings intact.
COLUMNS = (
    "id",
    "content",
    "chunk_text",
    "chunk_index",
    "project_id",
    "metadata",
    "created_at",
    "embedding",
)

SELECT_SQL = """
    select
        id::text         as id,
        content,
        chunk_text,
        chunk_index,
        project_id::text as project_id,
        metadata::text   as metadata,
        created_at,
        embedding::text  as embedding
    from public.chunks
    order by id;
"""

UPSERT_SQL = """
    insert into public.chunks (
        id, content, chunk_text, chunk_index, project_id, metadata, created_at, embedding
    )
    values (%s::uuid, %s, %s, %s, %s::uuid, %s::jsonb, %s, %s::vector)
    on conflict (id) do update set
        content     = excluded.content,
        chunk_text  = excluded.chunk_text,
        chunk_index = excluded.chunk_index,
        project_id  = excluded.project_id,
        metadata    = excluded.metadata,
        created_at  = excluded.created_at,
        embedding   = excluded.embedding;
"""


def fetch_rows(conn: psycopg2.extensions.connection, sql: str) -> list[dict]:
    with conn.cursor() as cur:
        cur.execute(sql)
        columns = [desc[0] for desc in cur.description]
        return [dict(zip(columns, row)) for row in cur.fetchall()]


def main() -> None:
    dry_run = "--dry-run" in sys.argv[1:]

    source_url = (os.getenv("SOURCE_DATABASE_URL") or "").strip()
    if not source_url:
        raise SystemExit(
            "SOURCE_DATABASE_URL is not set. Point it at the database to copy "
            "from (the old Supabase connection string)."
        )

    target_url = settings.DATABASE_URL
    if source_url == target_url:
        raise SystemExit(
            "SOURCE_DATABASE_URL and DATABASE_URL are identical; nothing to migrate."
        )

    source = psycopg2.connect(source_url)
    source.autocommit = True
    try:
        rows = fetch_rows(source, SELECT_SQL)
    finally:
        source.close()

    print(f"Read {len(rows)} rows from SOURCE_DATABASE_URL.")

    if dry_run:
        for row in rows[:5]:
            embedding = row["embedding"]
            preview = (row["metadata"] or "")[:120].replace("\n", " ")
            print(
                f"- id={row['id']} embedding={'yes' if embedding else 'null'} "
                f"metadata={preview}"
            )
        print("Dry run: nothing was written to the target database.")
        return

    # Idempotent: creates the extension, table, index and match_chunks() if needed.
    apply_schema(target_url)

    target = psycopg2.connect(target_url)
    try:
        with target.cursor() as cur:
            for row in rows:
                cur.execute(UPSERT_SQL, tuple(row[column] for column in COLUMNS))
            cur.execute("select count(*) from public.chunks;")
            total = cur.fetchone()[0]
        target.commit()
    except Exception:
        target.rollback()
        raise
    finally:
        target.close()

    print(f"Upserted {len(rows)} rows into {target_url.split('@')[-1]}.")
    print(f"public.chunks now holds {total} rows.")


if __name__ == "__main__":
    main()
