from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.inventory import Inventory

def recalc_available(inv: Inventory) -> None:
    inv.available_stock = max(0, int(inv.total_stock) - int(inv.reserved_stock))

def lock_inventory_row(db: Session, *, org_id: int, product_id: int) -> Inventory:
    inv = db.scalar(
        select(Inventory)
        .where(Inventory.org_id == org_id, Inventory.product_id == product_id)
        .with_for_update()
    )
    if not inv:
        raise ValueError("Inventory row missing for product")
    return inv
