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

    SUPABASE_URL: str
    SUPABASE_PUBLISHABLE_KEY: str | None = None
    SUPABASE_SECRET_KEY: str
    SUPABASE_JWKS_URL: str | None = None

    DATABASE_URL: str

    OLLAMA_URL: str = "http://localhost:11434"
    OLLAMA_EMBED_MODEL: str = "all-minilm:l6-v2"

    HF_TOKEN: str
    HF_EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    GROQ_URL: str = "https://api.groq.com/openai/v1"
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    GROQ_FALLBACK_MODEL: str = "llama-3.1-8b-instant"

    UPSTASH_REDIS_REST_URL: str
    UPSTASH_REDIS_REST_TOKEN: str

    ALLOWED_ORIGINS: str = "http://localhost:3000,https://creteciorenzo.vercel.app"

@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()