from __future__ import annotations

from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

_engine: Optional[Engine] = None
SessionLocal: sessionmaker | None = None


def get_engine() -> Engine:
    """
    Create the engine only when actually needed.
    This avoids import-time crashes and gives clearer runtime errors.
    """
    if not settings.DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL is not set. "
            "Set DATABASE_URL in your Railway service Variables."
        )

    return create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
    )


def init_db() -> None:
    """
    Initialize SessionLocal lazily.
    """
    global _engine, SessionLocal
    if SessionLocal is not None:
        return

    _engine = get_engine()
    SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False)
