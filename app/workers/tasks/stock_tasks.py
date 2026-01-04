from __future__ import annotations

from celery import shared_task
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.db import SessionLocal
from app.integrations.shopee.adapter import ShopeeAdapter
from app.models.inventory import Inventory
from app.models.product import Product

@shared_task(bind=True)
def shopee_push_stock_task(self, *, org_id: int, base_url: str, access_token: str, sku_list: list[str] | None = None):
    db: Session = SessionLocal()
    try:
        adapter = ShopeeAdapter(base_url=base_url, access_token=access_token)

        q = (
            select(Product.sku, Inventory.available_stock)
            .join(Inventory, Inventory.product_id == Product.id)
            .where(Product.org_id == org_id, Inventory.org_id == org_id)
        )
        if sku_list:
            q = q.where(Product.sku.in_(sku_list))

        rows = db.execute(q).all()
        items = [{"platform_sku": sku, "stock": int(avail)} for sku, avail in rows]

        batch_size = 50
        for i in range(0, len(items), batch_size):
            adapter.push_stock(items=items[i:i + batch_size])

        return {"pushed": len(items)}
    finally:
        db.close()
