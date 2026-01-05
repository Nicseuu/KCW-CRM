# app/api/deps.py
from __future__ import annotations

from typing import Generator

from sqlalchemy.orm import Session

import app.core.db as db


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that yields a DB session.

    Important: import the db module, not SessionLocal by value,
    so we always see the updated SessionLocal after init_db().
    """
    db.init_db()

    if db.SessionLocal is None:
        raise RuntimeError("DB not initialized (SessionLocal is None).")

    session: Session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()
