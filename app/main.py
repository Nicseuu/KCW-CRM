from __future__ import annotations

from fastapi import FastAPI

from app.core.config import settings

# Your routers (keep these if they exist)
from app.api.routes.excel import router as excel_router  # noqa: E402


app = FastAPI(title="Ecom CRM")


@app.get("/health")
def health():
    return {
        "status": "ok",
        "env": settings.ENV,
        "database_configured": bool(settings.DATABASE_URL),
        "redis_configured": bool(settings.REDIS_URL),
        "missing": [
            name
            for name, ok in {
                "DATABASE_URL": bool(settings.DATABASE_URL),
                "REDIS_URL": bool(settings.REDIS_URL),
            }.items()
            if not ok
        ],
    }


app.include_router(excel_router, prefix="/excel", tags=["excel"])
