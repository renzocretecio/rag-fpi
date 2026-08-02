from __future__ import annotations

from typing import Any, Sequence

import httpx

from app.core.config import settings


class EmbeddingServiceError(Exception):
    pass


class EmbeddingService:
    def __init__(self) -> None:
        self.model = settings.HF_EMBEDDING_MODEL
        self.api_url = f"https://router.huggingface.co/hf-inference/models/{self.model}/pipeline/feature-extraction"
        
        token = settings.HF_TOKEN.strip().strip("'\"") if settings.HF_TOKEN else ""
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def embed_text_sync(self, text: str) -> list[float]:
        vectors = self.embed_batch_sync([text])
        return vectors[0]

    def embed_batch_sync(self, texts: Sequence[str]) -> list[list[float]]:
        if not texts:
            return []

        payload = {
            "inputs": list(texts),
            "options": {
                "wait_for_model": True
            },
        }

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                )
                response.raise_for_status()
                data: Any = response.json()
        except httpx.HTTPError as exc:
            raise EmbeddingServiceError(f"Hugging Face embedding request failed: {exc}") from exc

        if isinstance(data, list) and all(isinstance(v, list) for v in data):
            return data

        raise EmbeddingServiceError(f"Invalid embedding response structure: {data}")


embedding_service = EmbeddingService()