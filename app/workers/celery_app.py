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
    )

    # Celery 6+ deprecation: keep retrying broker connection on startup
    celery_app.conf.update(
        broker_connection_retry_on_startup=True,

        # Optional, but commonly useful defaults:
        timezone=os.getenv("CELERY_TIMEZONE", "UTC"),
        enable_utc=True,
        task_track_started=True,
        worker_prefetch_multiplier=int(os.getenv("CELERY_PREFETCH_MULTIPLIER", "1")),
    )

    # Auto-discover tasks from these modules/packages.
    # Adjust this to match where your @shared_task / @celery_app.task live.
    celery_app.autodiscover_tasks(
        [
            "app.workers.tasks",
        ]
    )

    return celery_app


celery_app = make_celery()
