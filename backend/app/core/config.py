"""Application settings."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment-backed application settings."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "AI Investment Copilot"
    app_env: str = "local"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "sqlite+aiosqlite:///./investment_copilot.db"
    test_database_url: str = "sqlite+aiosqlite:///:memory:"
    jwt_secret_key: str = Field(default="change-me-in-production", min_length=16)
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"
    yfinance_timeout_seconds: int = 10
    redis_url: str | None = None
    backend_cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]


@lru_cache
def get_settings() -> Settings:
    """Return cached settings."""
    return Settings()


settings = get_settings()
