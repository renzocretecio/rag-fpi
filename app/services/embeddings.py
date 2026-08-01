from __future__ import annotations

from typing import Any, Sequence

import httpx

from app.core.config import settings


class EmbeddingServiceError(Exception):
    pass


class EmbeddingService:
    def __init__(self) -> None:
        self.base_url = settings.OLLAMA_URL.rstrip("/")
        self.model = settings.OLLAMA_EMBED_MODEL

    def embed_text_sync(self, text: str) -> list[float]:
        vectors = self.embed_batch_sync([text])
        return vectors[0]

    def embed_batch_sync(self, texts: Sequence[str]) -> list[list[float]]:
        if not texts:
            return []

        url = f"{self.base_url}/api/embed"
        payload = {
            "model": self.model,
            "input": list(texts),
        }

        try:
            with httpx.Client(timeout=60.0) as client:
                response = client.post(url, json=payload)
                response.raise_for_status()
                data: dict[str, Any] = response.json()
        except httpx.HTTPError as exc:
            raise EmbeddingServiceError(f"Ollama embedding request failed: {exc}") from exc

        embeddings = data.get("embeddings")
        if not isinstance(embeddings, list):
            raise EmbeddingServiceError("Invalid embedding response from Ollama")

        return embeddings


embedding_service = EmbeddingService()