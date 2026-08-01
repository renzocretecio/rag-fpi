from __future__ import annotations

import json
from typing import Any, Iterator, Sequence

import httpx

from app.core.config import settings


class LLMServiceError(Exception):
    pass


SYSTEM_PROMPT = """You are an assistant embedded in {name}'s developer portfolio.
Answer questions about their skills, experience, and projects using ONLY the
context provided below. Be concise and conversational — 2-4 sentences unless
asked for detail.

Rules:
- If the context doesn't contain the answer, say you don't have that info
  and suggest what they could ask instead.
- Don't make up projects, technologies, or dates not in the context.
- When relevant, mention which project you're referencing by name.
"""


class LLMService:
    def __init__(self) -> None:
        self.base_url = settings.GROQ_URL.rstrip("/")
        self.api_key = settings.GROQ_API_KEY
        self.model = settings.GROQ_MODEL
        self.fallback_model = settings.GROQ_FALLBACK_MODEL

    def _build_messages(self, question: str, matches: Sequence[dict]) -> list[dict]:
        context = "\n\n".join(
            f"[{m['metadata'].get('source_type', 'info')}]\n{m['content']}"
            for m in matches
        )
        return [
            {"role": "system", "content": SYSTEM_PROMPT.format(name="Renzo Cretecio")},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ]

    def _post(self, payload: dict) -> httpx.Response:
        with httpx.Client(timeout=60.0) as client:
            response = client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=payload,
            )
            response.raise_for_status()
            return response

    def generate_answer_sync(self, question: str, matches: Sequence[dict]) -> str:
        if not matches:
            return "I don't have specific info on that — try asking about my projects, skills, or background!"

        payload = {"model": self.model, "messages": self._build_messages(question, matches), "stream": False}

        try:
            data: dict[str, Any] = self._post(payload).json()
        except httpx.HTTPError:
            try:
                payload["model"] = self.fallback_model
                data = self._post(payload).json()
            except httpx.HTTPError as exc:
                raise LLMServiceError(f"Groq request failed: {exc}") from exc

        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as exc:
            raise LLMServiceError("Invalid response from Groq") from exc

    def stream_answer_sync(self, question: str, matches: Sequence[dict]) -> Iterator[str]:
        if not matches:
            yield "I don't have specific info on that — try asking about my projects, skills, or background!"
            return

        payload = {"model": self.model, "messages": self._build_messages(question, matches), "stream": True}

        try:
            with httpx.Client(timeout=60.0) as client:
                with client.stream(
                    "POST",
                    f"{self.base_url}/chat/completions",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json=payload,
                ) as response:
                    response.raise_for_status()
                    for line in response.iter_lines():
                        if not line or not line.startswith("data: "):
                            continue
                        chunk = line.removeprefix("data: ")
                        if chunk.strip() == "[DONE]":
                            break
                        delta = json.loads(chunk)["choices"][0]["delta"].get("content")
                        if delta:
                            yield delta
        except httpx.HTTPError as exc:
            raise LLMServiceError(f"Groq streaming request failed: {exc}") from exc


llm_service = LLMService()