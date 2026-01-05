# app/core/db.py
from __future__ import annotations

from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

_engine: Optional[Engine] = None
SessionLocal: sessionmaker | None = None


def _sqlalchemy_url_for_psycopg(raw_url: str) -> str:
    """
    Force SQLAlchemy to use Psycopg v3 driver.

    Railway commonly provides:
      - postgresql://...
      - postgres://...

    SQLAlchemy w/ psycopg v3 should be:
      - postgresql+psycopg://...
    """
    url = (raw_url or "").strip()

    if url.startswith("postgresql+psycopg://"):
        return url
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg://", 1)

    return url


def get_engine() -> Engine:
    """
    Lazy engine creation to avoid import-time crashes.
    """
    global _engine

    if _engine is not None:
        return _engine

    if not getattr(settings, "DATABASE_URL", None):
        raise RuntimeError("DATABASE_URL is not set. Set it in Railway Variables.")

    db_url = _sqlalchemy_url_for_psycopg(settings.DATABASE_URL)

    _engine = create_engine(
        db_url,
        pool_pre_ping=True,
    )
    return _engine


def init_db() -> None:
    """
    Initialize SessionLocal once.

    This function exists because your code imports:
      from app.core.db import SessionLocal, init_db
    """
    global SessionLocal

    if SessionLocal is not None:
        return

    engine = get_engine()
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
