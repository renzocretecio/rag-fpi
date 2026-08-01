from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse

from app.db.postgres import database
from app.schemas.query import QueryRequest
from app.schemas.response import QueryResponse, AskResponse, RetrievedChunkOut
from app.services.embeddings import EmbeddingServiceError, embedding_service
from app.services.llm import LLMServiceError, llm_service

from app.core.ratelimit import ratelimit

router = APIRouter()


def _retrieve(payload: QueryRequest) -> tuple[list[float], list[dict]]:
    query_embedding = embedding_service.embed_text_sync(payload.question)
    rows = database.fetch(
        """
        select
            id::text,
            content,
            coalesce(metadata, '{}'::jsonb) as metadata,
            1 - (embedding <=> %s::vector) as similarity
        from public.chunks
        order by embedding <=> %s::vector
        limit %s;
        """,
        query_embedding,
        query_embedding,
        payload.top_k,
    )
    return query_embedding, rows


@router.post("/query", response_model=QueryResponse)
def query(payload: QueryRequest):
    try:
        _, rows = _retrieve(payload)
    except EmbeddingServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    return QueryResponse(
        question=payload.question,
        matches=[
            RetrievedChunkOut(id=r["id"], content=r["content"], metadata=r["metadata"], similarity=float(r["similarity"]))
            for r in rows
        ],
    )


@router.post("/ask", response_model=AskResponse)
def ask(payload: QueryRequest):
    try:
        _, rows = _retrieve(payload)
    except EmbeddingServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    matches = [
        {"id": r["id"], "content": r["content"], "metadata": r["metadata"], "similarity": float(r["similarity"])}
        for r in rows
    ]

    try:
        answer = llm_service.generate_answer_sync(payload.question, matches)
    except LLMServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    return AskResponse(
        question=payload.question,
        answer=answer,
        matches=[RetrievedChunkOut(**m) for m in matches],
    )


@router.post("/ask/stream")
def ask_stream(payload: QueryRequest, request: Request):
    identifier = request.client.host if request.client else "unknown"
    result = ratelimit.limit(identifier)
    if not result.allowed:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")

    try:
        _, rows = _retrieve(payload)
    except EmbeddingServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    matches = [
        {"id": r["id"], "content": r["content"], "metadata": r["metadata"], "similarity": float(r["similarity"])}
        for r in rows
    ]

    return StreamingResponse(
        llm_service.stream_answer_sync(payload.question, matches),
        media_type="text/plain",
    )