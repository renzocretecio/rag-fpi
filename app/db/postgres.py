from __future__ import annotations

from contextlib import contextmanager

import psycopg2
from pgvector.psycopg2 import register_vector


class Postgres:
    def __init__(self, database_url: str | None = None) -> None:
        self.database_url = database_url
        self.conn = None

    def connect(self) -> None:
        if not self.database_url:
            raise RuntimeError("DATABASE_URL is not configured")

        self.conn = psycopg2.connect(self.database_url)
        self.conn.autocommit = True
        with self.conn.cursor() as cur:
            cur.execute("SET search_path = public, extensions")
        register_vector(self.conn)

    def disconnect(self) -> None:
        if self.conn:
            self.conn.close()
            self.conn = None

    @contextmanager
    def cursor(self):
        if not self.conn:
            raise RuntimeError("Database connection is not initialized")
        cur = self.conn.cursor()
        try:
            yield cur
        finally:
            cur.close()

    def fetch(self, query: str, *args):
        with self.cursor() as cur:
            cur.execute(query, args)
            if cur.description is None:
                return []
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in cur.fetchall()]

    def fetchrow(self, query: str, *args):
        rows = self.fetch(query, *args)
        return rows[0] if rows else None


database = Postgres()