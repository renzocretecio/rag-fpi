from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.postgres import database
from app.routers.health import router as health_router
from app.routers.query import router as query_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.database_url = settings.DATABASE_URL
    database.connect()
    print(f"Starting {settings.PROJECT_NAME}")
    yield
    database.disconnect()
    print(f"Stopping {settings.PROJECT_NAME}")


app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
)

origins = [
    origin.strip()
    for origin in settings.ALLOWED_ORIGINS.split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix=settings.API_V1_STR, tags=["health"])
app.include_router(query_router, prefix=settings.API_V1_STR, tags=["query"])