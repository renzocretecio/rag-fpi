from __future__ import annotations

from contextlib import contextmanager
from urllib.parse import urlparse

import psycopg2
from pgvector.psycopg2 import register_vector


def is_pooled_connection(database_url: str) -> bool:
    """Detect PgBouncer-backed endpoints.

    Neon exposes a PgBouncer endpoint whose hostname ends with ``-pooler``
    (``pool_mode=transaction``); Supabase uses ``...pooler.supabase.com``.
    Transaction-mode pooling cannot preserve session state (``SET``, prepared
    statements, advisory locks), so callers need to adapt.
    """
    host = urlparse(database_url).hostname or ""
    endpoint = host.split(".", 1)[0]  # Neon: ep-xxxx-xxxx-pooler.<region>.aws.neon.tech
    return endpoint.endswith("-pooler") or ".pooler." in host


class Postgres:
    """Minimal psycopg2 wrapper for the API and the maintenance scripts.

    Provider agnostic (Neon, Supabase, local Postgres). Neon suspends idle
    compute and closes idle connections, so every operation transparently
    re-establishes a connection that the server has dropped.
    """

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
        try:
            register_vector(self.conn)
        except psycopg2.ProgrammingError as exc:
            raise RuntimeError(
                "The pgvector `vector` type is missing from this database. "
                "Run `python -m scripts.init_db` against DATABASE_URL first."
            ) from exc

    def disconnect(self) -> None:
        if self.conn:
            self.conn.close()
            self.conn = None

    @property
    def is_connected(self) -> bool:
        return self.conn is not None and self.conn.closed == 0

    def reconnect_if_closed(self) -> None:
        """Reconnect when the server closed the connection (Neon scale-to-zero)."""
        if not self.conn:
            raise RuntimeError("Database connection is not initialized")
        if not self.is_connected:
            self.connect()

    @contextmanager
    def cursor(self):
        self.reconnect_if_closed()
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