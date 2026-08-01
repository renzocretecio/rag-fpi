from __future__ import annotations

import json
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from app.core.config import settings
from app.db.postgres import database
from app.services.embeddings import embedding_service

ALLOWED_SOURCE_TYPES = {
    "about",
    "experience",
    "hobbies",
    "contact",
    "tech-stack",
    "projects",
}


def chunk_markdown(text: str, max_chars: int = 1200) -> list[str]:
    blocks = [b.strip() for b in text.split("\n\n") if b.strip()]
    chunks: list[str] = []
    current = ""

    for block in blocks:
        if len(current) + len(block) + 2 <= max_chars:
            current = f"{current}\n\n{block}".strip()
        else:
            if current:
                chunks.append(current)
            current = block

    if current:
        chunks.append(current)

    return chunks


def is_hidden(path: Path) -> bool:
    return any(part.startswith(".") for part in path.parts)


def iter_markdown_files(root: Path):
    for source_type in ALLOWED_SOURCE_TYPES:
        folder = root / source_type
        if not folder.exists():
            continue
        for path in folder.rglob("*.md"):
            if path.is_file() and not is_hidden(path):
                yield source_type, path


def main() -> None:
    data_root = Path("data")
    rows = []

    for source_type, file_path in iter_markdown_files(data_root):
        text = file_path.read_text(encoding="utf-8").strip()
        if not text:
            continue

        chunks = chunk_markdown(text)
        embeddings = embedding_service.embed_batch_sync(chunks)

        for idx, (content, embedding) in enumerate(zip(chunks, embeddings), start=1):
            rows.append(
                (
                    content,
                    embedding,
                    json.dumps(
                        {
                            "source_type": source_type,
                            "source_file": str(file_path),
                            "chunk_index": idx,
                            "file_type": ".md",
                        }
                    ),
                )
            )

    database.database_url = settings.DATABASE_URL
    database.connect()
    try:
        database.fetch("delete from public.chunks;")
        for content, embedding, metadata in rows:
            database.fetch(
                """
                insert into public.chunks (content, embedding, metadata)
                values (%s, %s::vector, %s::jsonb);
                """,
                content,
                embedding,
                metadata,
            )
    finally:
        database.disconnect()

    print(f"Inserted {len(rows)} chunks from Markdown files.")


if __name__ == "__main__":
    main()