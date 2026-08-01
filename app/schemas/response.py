from typing import Any

from pydantic import BaseModel


class RetrievedChunkOut(BaseModel):
    id: str
    content: str
    metadata: dict[str, Any]
    similarity: float


class QueryResponse(BaseModel):
    question: str
    matches: list[RetrievedChunkOut]

class AskResponse(QueryResponse):
    answer: str