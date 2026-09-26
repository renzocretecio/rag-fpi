from __future__ import annotations

from pathlib import Path

import psycopg2
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from app.core.config import settings
from app.db.postgres import database

SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"


def apply_schema(database_url: str) -> None:
    """Apply scripts/schema.sql to the given database.

    A raw psycopg2 connection is used on purpose: pgvector's `register_vector`
    (used by app/db/postgres.py) requires the `vector` type to already exist,
    which is exactly what this script creates on a fresh Neon database.
    """
    sql = SCHEMA_PATH.read_text(encoding="utf-8")

    conn = psycopg2.connect(database_url)
    conn.autocommit = True
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
    finally:
        conn.close()


def main() -> None:
    apply_schema(settings.DATABASE_URL)
    print(f"Applied {SCHEMA_PATH.name} to the target database.")

    # Connect through the application wrapper to smoke-test DATABASE_URL.
    database.database_url = settings.DATABASE_URL
    database.connect()
    try:
        version = database.fetchrow(
            "select extversion from pg_extension where extname = 'vector';"
        )
        chunks = database.fetchrow("select count(*) as count from public.chunks;")
    finally:
        database.disconnect()

    print(f"pgvector version: {version['extversion']}")
    print(f"public.chunks rows: {chunks['count']}")


if __name__ == "__main__":
    main()
