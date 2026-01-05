# app/workers/celery_app.py

import os
from celery import Celery


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} is not set")
    return value


def _int_env(name: str, default: int) -> int:
    raw = os.getenv(name, str(default)).strip()
    try:
        return int(raw)
    except ValueError as exc:
        raise RuntimeError(f"{name} must be an integer, got: {raw!r}") from exc


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

    pull_orders_every_min = _int_env("PULL_ORDERS_EVERY_MIN", 2)
    sync_excel_every_min = _int_env("SYNC_EXCEL_EVERY_MIN", 5)
    reconcile_every_min = _int_env("RECONCILE_STOCK_EVERY_MIN", 5)
    push_stock_every_min = _int_env("PUSH_STOCK_EVERY_MIN", 2)

    # Force Beat schedule DB location/name (avoids stale schedule issues)
    beat_schedule_filename = os.getenv("CELERY_BEAT_SCHEDULE_FILE", "celerybeat-schedule")

    celery_app.conf.update(
        broker_connection_retry_on_startup=True,
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        task_default_queue=default_queue,
        task_default_exchange=default_queue,
        task_default_routing_key=default_queue,
        timezone=os.getenv("CELERY_TIMEZONE", "UTC"),
        enable_utc=True,
        task_track_started=True,
        worker_prefetch_multiplier=_int_env("CELERY_PREFETCH_MULTIPLIER", 1),
        beat_schedule_filename=beat_schedule_filename,
        beat_schedule={
            "pull-orders-tiktok": {
                "task": "app.workers.tasks.pull_orders_tiktok",
                "schedule": float(pull_orders_every_min * 60),
                "options": {"queue": default_queue},
            },
            "pull-orders-shopee": {
                "task": "app.workers.tasks.pull_orders_shopee",
                "schedule": float(pull_orders_every_min * 60),
                "options": {"queue": default_queue},
            },
            "pull-orders-lazada": {
                "task": "app.workers.tasks.pull_orders_lazada",
                "schedule": float(pull_orders_every_min * 60),
                "options": {"queue": default_queue},
            },
            "sync-excel-inventory-to-db": {
                "task": "app.workers.tasks.sync_excel_inventory_to_db",
                "schedule": float(sync_excel_every_min * 60),
                "options": {"queue": default_queue},
            },
            "reconcile-stock": {
                "task": "app.workers.tasks.reconcile_stock",
                "schedule": float(reconcile_every_min * 60),
                "options": {"queue": default_queue},
            },
            "push-stock-updates-to-channels": {
                "task": "app.workers.tasks.push_stock_updates_to_channels",
                "schedule": float(push_stock_every_min * 60),
                "options": {"queue": default_queue},
            },
        },
    )

    return celery_app


celery_app = make_celery()
