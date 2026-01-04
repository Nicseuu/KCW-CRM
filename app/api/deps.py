from __future__ import annotations

from sqlalchemy.orm import Session
from app.core.db import SessionLocal

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
