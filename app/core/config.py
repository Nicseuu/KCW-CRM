from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Settings are loaded from environment variables (Railway Variables),
    and optionally from a local .env file for development.

    IMPORTANT:
    - DATABASE_URL and REDIS_URL are optional here so the app can boot
      and show a clear /health status even when not configured yet.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    ENV: str = Field(default="dev")

    DATABASE_URL: str | None = Field(default=None)
    REDIS_URL: str | None = Field(default=None)

    # keep any other settings you use elsewhere
    JWT_SECRET: str = Field(default="change-me")
    TZ: str = Field(default="UTC")


settings = Settings()
