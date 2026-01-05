# app/core/db.py
from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Generator, Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

_engine: Optional[Engine] = None
SessionLocal: Optional[sessionmaker] = None


def _build_sqlalchemy_database_url(raw_url: str) -> str:
    """
    Railway commonly provides:
      - postgresql://...
      - postgres://...

    SQLAlchemy needs the driver explicitly to use psycopg v3:
      - postgresql+psycopg://...
    """
    url = raw_url.strip()

    if url.startswith("postgresql+psycopg://"):
        return url

    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg://", 1)

    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg://", 1)

    # If you use something else (sqlite, etc.), keep as-is
    return url


def get_engine() -> Engine:
    """
    Lazy-create the SQLAlchemy Engine so imports don't crash the app.
    """
    global _engine

    if _engine is not None:
        return _engine

    raw_db_url = os.getenv("DATABASE_URL", "")
    if not raw_db_url:
        raise RuntimeError("DATABASE_URL is not set in environment variables.")

    db_url = _build_sqlalchemy_database_url(raw_db_url)

    _engine = create_engine(
        db_url,
        pool_pre_ping=True,
        future=True,
    )
    return _engine


def get_sessionmaker() -> sessionmaker:
    """
    Lazy-create the sessionmaker.
    """
    global SessionLocal

    if SessionLocal is not None:
        return SessionLocal

    engine = get_engine()
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    return SessionLocal


@contextmanager
def session_scope() -> Generator[Session, None, None]:
    """
    Context manager for scripts/CLI usage.
    """
    SessionLocal_ = get_sessionmaker()
    db: Session = SessionLocal_()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency.

    Usage:
        from fastapi import Depends
        from sqlalchemy.orm import Session
        from app.core.db import get_db

        @router.get("/something")
        def route(db: Session = Depends(get_db)):
            ...
    """
    SessionLocal_ = get_sessionmaker()
    db: Session = SessionLocal_()
    try:
        yield db
    finally:
        db.close()
