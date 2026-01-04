from __future__ import annotations

from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.excel import router as excel_router
from app.api.routes.inventory import router as inventory_router
from app.api.routes.sync import router as sync_router
from app.api.routes.customers import router as customers_router

app = FastAPI(title="Multi-channel CRM + Inventory (PH)", version="0.1.0")

app.include_router(health_router, tags=["health"])
app.include_router(excel_router, prefix="/inventory/excel", tags=["excel"])
app.include_router(inventory_router, prefix="/inventory", tags=["inventory"])
app.include_router(sync_router, prefix="/sync", tags=["sync"])
app.include_router(customers_router, prefix="/customers", tags=["crm"])
