from __future__ import annotations

from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.reservations import OrderItemReservation
from app.services.inventory_service import lock_inventory_row, recalc_available


PAID_STATUSES = {"CONFIRMED", "PACKING", "SHIPPED", "DELIVERED"}
RELEASE_STATUSES = {"CANCELLED", "REFUNDED", "RETURNED"}


def ensure_reserved(
    db: Session,
    *,
    org_id: int,
    order_id: int,
    order_item_id: int,
    product_id: int,
    qty: int,
    event: str = "PAID_SYNC",
) -> bool:
    """
    Returns True if a new reservation was created and inventory was changed.
    """
    existing = db.scalar(
        select(OrderItemReservation).where(
            OrderItemReservation.org_id == org_id,
            OrderItemReservation.order_item_id == order_item_id,
        )
    )
    if existing and existing.reserved_at is not None:
        return False

    now = datetime.now(timezone.utc)
    if not existing:
        existing = OrderItemReservation(
            org_id=org_id,
            order_id=order_id,
            order_item_id=order_item_id,
            product_id=product_id,
            qty=qty,
            reserved_at=now,
            reserve_event=event,
        )
        db.add(existing)
    else:
        existing.product_id = product_id
        existing.qty = qty
        existing.reserved_at = now
        existing.reserve_event = event

    inv = lock_inventory_row(db, org_id=org_id, product_id=product_id)
    inv.reserved_stock += int(qty)
    recalc_available(inv)
    return True


def ensure_released(
    db: Session,
    *,
    org_id: int,
    order_item_id: int,
    event: str = "CANCELLED_SYNC",
) -> bool:
    """
    Returns True if a release happened and inventory was changed.
    """
    res = db.scalar(
        select(OrderItemReservation).where(
            OrderItemReservation.org_id == org_id,
            OrderItemReservation.order_item_id == order_item_id,
        )
    )
    if not res or res.reserved_at is None or res.released_at is not None:
        return False

    now = datetime.now(timezone.utc)
    res.released_at = now
    res.release_event = event

    inv = lock_inventory_row(db, org_id=org_id, product_id=res.product_id)
    inv.reserved_stock = max(0, int(inv.reserved_stock) - int(res.qty))
    recalc_available(inv)
    return True
