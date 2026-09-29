from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str | None = None
    redis_url: str | None = None
    triage_provider: str = "simulated"
    llm_api_key: str | None = None
    groq_model: str = "llama-3.1-8b-instant"
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    rate_limit_per_minute: int = 60
    cors_origins: str = (
        "http://localhost:5173,http://127.0.0.1:5173,http://civicpulse.local"
    )
    triage_failure_mode: str = ""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
