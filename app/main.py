from __future__ import annotations

from fastapi import FastAPI

from app.api.routes.excel import router as excel_router
from app.core.config import settings

app = FastAPI(title="Ecom CRM")


@app.get("/")
def root():
    return {
        "message": "API is running",
        "try": ["/health", "/docs", "/excel/ping"],
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "env": settings.ENV,
        "database_configured": bool(settings.DATABASE_URL),
        "redis_configured": bool(settings.REDIS_URL),
        "missing": [
            k
            for k, ok in {
                "DATABASE_URL": bool(settings.DATABASE_URL),
                "REDIS_URL": bool(settings.REDIS_URL),
            }.items()
            if not ok
        ],
    }


app.include_router(excel_router, prefix="/excel", tags=["excel"])
