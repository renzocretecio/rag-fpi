-- Database schema for the RAG backend (Neon / any Postgres 15+ with pgvector).
--
-- Mirrors the objects that previously lived only in the Supabase project, so a
-- fresh Neon database can be brought up with a single command:
--
--     python -m scripts.init_db
--
-- Every statement is idempotent, so the file is also safe to re-run.

-- pgvector is enabled per database. It installs into `public` by default,
-- which is what `pgvector.asyncpg.register_vector()` expects (schema='public').
create extension if not exists vector;

create table if not exists public.chunks (
    id          uuid primary key default gen_random_uuid(),
    embedding   vector(384),          -- all-MiniLM-L6-v2 output dimensions
    chunk_text  text,
    metadata    jsonb,
    created_at  timestamptz default now(),
    content     text,
    chunk_index integer,
    project_id  uuid
);

-- Approximate nearest-neighbour index for the cosine (`<=>`) search used by
-- app/routers/query.py, scripts/verify_search.py and match_chunks() below.
create index if not exists chunks_embedding_hnsw_idx
    on public.chunks using hnsw (embedding vector_cosine_ops);

-- Server-side counterpart of the Supabase RPC the frontend used to call.
create or replace function public.match_chunks(
    query_embedding vector,
    match_count integer default 5
)
returns table(id uuid, content text, metadata jsonb, similarity double precision)
language sql
stable
as $$
    select
        c.id,
        c.content,
        c.metadata,
        1 - (c.embedding <=> query_embedding) as similarity
    from public.chunks c
    order by c.embedding <=> query_embedding
    limit match_count;
$$;
