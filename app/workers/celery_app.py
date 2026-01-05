# app/workers/celery_app.py

import os
from celery import Celery


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} is not set")
    return value


def make_celery() -> Celery:
    redis_url = _require_env("REDIS_URL")

    celery_app = Celery(
        "ecom_crm",
        broker=redis_url,
        backend=redis_url,
        include=[
            "app.workers.tasks",  # ensure tasks are registered
        ],
    )

    celery_app.conf.update(
        # Celery 6+ deprecation warning fix:
        broker_connection_retry_on_startup=True,

        # Recommended operational defaults:
        timezone=os.getenv("CELERY_TIMEZONE", "UTC"),
        enable_utc=True,
        task_track_started=True,
        worker_prefetch_multiplier=int(os.getenv("CELERY_PREFETCH_MULTIPLIER", "1")),

        # Beat schedule (proof-of-life task every 30 seconds)
        beat_schedule={
            "heartbeat-every-30-seconds": {
                "task": "app.workers.tasks.heartbeat",
                "schedule": 30.0,
            }
        },
    )

    return celery_app


celery_app = make_celery()
