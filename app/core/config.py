from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    PROJECT_NAME: str = "case-study-api"
    API_V1_STR: str = "/api/v1"

    # Postgres connection string (Neon). Use the direct (non-pooler) endpoint:
    # the app keeps one long-lived connection and relies on session state
    # (`SET search_path`), which a PgBouncer transaction-mode pool drops.
    DATABASE_URL: str

    OLLAMA_URL: str = "http://localhost:11434"
    OLLAMA_EMBED_MODEL: str = "all-minilm:l6-v2"

    HF_TOKEN: str
    HF_EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    GROQ_URL: str = "https://api.groq.com/openai/v1"
    GROQ_API_KEY: str
    # Groq retires models periodically; a retired model returns HTTP 404
    # ("model_not_found"). Check `GET /openai/v1/models` if answers stop working.
    GROQ_MODEL: str = "openai/gpt-oss-120b"
    GROQ_FALLBACK_MODEL: str = "openai/gpt-oss-20b"

    UPSTASH_REDIS_REST_URL: str
    UPSTASH_REDIS_REST_TOKEN: str

    ALLOWED_ORIGINS: str = "http://localhost:3000,https://creteciorenzo.vercel.app"

@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()