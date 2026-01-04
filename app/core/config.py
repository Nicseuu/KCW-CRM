from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Loads settings from environment variables (Railway Variables),
    and optionally from a local .env for development.

    DATABASE_URL and REDIS_URL are optional so the API can boot and expose /health
    even if Railway variables aren't configured yet.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    ENV: str = Field(default="dev")

    DATABASE_URL: str | None = Field(default=None)
    REDIS_URL: str | None = Field(default=None)

    TZ: str = Field(default="Asia/Manila")
    JWT_SECRET: str = Field(default="change-me")


settings = Settings()
