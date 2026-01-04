from __future__ import annotations

from typing import Generator

from sqlalchemy.orm import Session

from app.core.db import SessionLocal, init_db


def get_db() -> Generator[Session, None, None]:
    init_db()
    assert SessionLocal is not None

    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
