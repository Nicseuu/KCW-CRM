from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.api.deps import get_db
from app.models.inventory import Inventory
from app.models.product import Product

router = APIRouter()
MVP_ORG_ID = 1

@router.get("")
def list_inventory(low_stock: bool = False, threshold: int = 5, db: Session = Depends(get_db)):
    q = (
        select(Product.sku, Product.name, Inventory.total_stock, Inventory.reserved_stock, Inventory.available_stock, Inventory.updated_at)
        .join(Inventory, Inventory.product_id == Product.id)
        .where(Product.org_id == MVP_ORG_ID, Inventory.org_id == MVP_ORG_ID)
        .order_by(Product.sku.asc())
    )
    rows = db.execute(q).all()
    items = [
        {
            "sku": sku,
            "name": name,
            "total_stock": int(total),
            "reserved_stock": int(reserved),
            "available_stock": int(avail),
            "updated_at": updated_at,
        }
        for sku, name, total, reserved, avail, updated_at in rows
    ]
    if low_stock:
        items = [x for x in items if x["available_stock"] <= threshold]
    return items
