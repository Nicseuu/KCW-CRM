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
            "app.workers.tasks",
        ],
    )

    default_queue = os.getenv("CELERY_QUEUE", "celery")

    celery_app.conf.update(
        # Fix Celery 6+ startup retry deprecation warning
        broker_connection_retry_on_startup=True,

        # Serialization (safe defaults)
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",

        # Queue defaults (ensures Beat + Worker use the same queue)
        task_default_queue=default_queue,
        task_default_exchange=default_queue,
        task_default_routing_key=default_queue,

        # Operational defaults
        timezone=os.getenv("CELERY_TIMEZONE", "UTC"),
        enable_utc=True,
        task_track_started=True,
        worker_prefetch_multiplier=int(os.getenv("CELERY_PREFETCH_MULTIPLIER", "1")),

        # Proof-of-life schedule
        beat_schedule={
            "heartbeat-every-30-seconds": {
                "task": "app.workers.tasks.heartbeat",
                "schedule": 30.0,
                "options": {"queue": default_queue},
            }
        },
    )

    return celery_app


celery_app = make_celery()
