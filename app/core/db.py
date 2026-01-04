from __future__ import annotations

from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


def get_engine() -> Engine:
    """
    Lazily create the engine only when actually needed.
    This prevents import-time crashes when DATABASE_URL isn't set.
    """
    if not settings.DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL is not set. "
            "Set DATABASE_URL in your Railway service Variables (API/Worker/Beat)."
        )

    return create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
    )


# These are created lazily so importing app doesn't crash.
_engine: Optional[Engine] = None
SessionLocal: sessionmaker | None = None


def init_db() -> None:
    global _engine, SessionLocal
    if SessionLocal is not None:
        return

    _engine = get_engine()
    SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False)
