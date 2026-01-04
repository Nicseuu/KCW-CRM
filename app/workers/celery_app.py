from __future__ import annotations

from celery import Celery

from app.core.config import settings


def make_celery() -> Celery:
    if not settings.REDIS_URL:
        raise RuntimeError(
            "REDIS_URL is not set. "
            "Set REDIS_URL in your Railway service Variables (API/Worker/Beat)."
        )

    celery_app = Celery(
        "ecom_crm",
        broker=settings.REDIS_URL,
        backend=settings.REDIS_URL,
    )

    celery_app.conf.update(
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],
        timezone=settings.TZ,
        enable_utc=True,
        task_track_started=True,
    )
    return celery_app


celery_app = make_celery()
