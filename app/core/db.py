from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


if not settings.DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. Set DATABASE_URL in your Railway service variables."
    )

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
