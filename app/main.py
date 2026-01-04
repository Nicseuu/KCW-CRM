from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.excel import router as excel_router
from app.core.config import settings

app = FastAPI(title="Ecom CRM")

# For internal admin UI, you can start permissive, then restrict to your Vercel/Railway frontend domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "API is running", "try": ["/health", "/docs", "/excel/ping"]}


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
