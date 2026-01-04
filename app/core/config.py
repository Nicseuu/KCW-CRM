from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    ENV: str = Field(default="dev")
    DATABASE_URL: str
    REDIS_URL: str

    JWT_SECRET: str = Field(default="change-me")

    TZ: str = Field(default="Asia/Manila")
    CURRENCY: str = Field(default="PHP")

    # Platform app keys (optional placeholders; platform_account stores per-shop tokens)
    SHOPEE_PARTNER_ID: str | None = None
    SHOPEE_PARTNER_KEY: str | None = None

    # Sync defaults
    ORDER_PULL_MINUTES: int = 5
    STOCK_PUSH_MINUTES: int = 10
    EXCEL_POLL_MINUTES: int = 30


settings = Settings()
