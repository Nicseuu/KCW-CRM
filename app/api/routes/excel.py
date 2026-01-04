from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.excel import ExcelInventoryFile  # ensures model import is valid

router = APIRouter()


@router.get("/ping")
def excel_ping(db: Session = Depends(get_db)):
    # If DATABASE_URL is configured, this verifies DB connectivity
    db.execute(text("SELECT 1"))
    return {"ok": True, "model_loaded": ExcelInventoryFile.__tablename__}
