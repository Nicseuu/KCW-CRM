from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.api.deps import get_db
from app.models.crm import Customer

router = APIRouter()
MVP_ORG_ID = 1

@router.get("")
def list_customers(q: str | None = None, db: Session = Depends(get_db)):
    stmt = select(Customer).where(Customer.org_id == MVP_ORG_ID).order_by(Customer.id.desc()).limit(50)
    if q:
        like = f"%{q.strip()}%"
        stmt = stmt.where((Customer.primary_phone.ilike(like)) | (Customer.primary_email.ilike(like)) | (Customer.full_name.ilike(like)))
    rows = db.execute(stmt).scalars().all()
    return [{"id": c.id, "crn": c.crn, "name": c.full_name, "phone": c.primary_phone, "email": c.primary_email} for c in rows]
