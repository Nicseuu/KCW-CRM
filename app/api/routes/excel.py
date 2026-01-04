from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.excel import ExcelInventoryFile  # ensures model import works

router = APIRouter()


@router.get("/ping")
def excel_ping(db: Session = Depends(get_db)):
    # simple DB test query so you can confirm DATABASE_URL works
    db.execute(text("SELECT 1"))
    return {"ok": True, "model_loaded": ExcelInventoryFile.__tablename__}
