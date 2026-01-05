# app/workers/tasks.py

import logging
from datetime import datetime, timezone
from celery import shared_task

logger = logging.getLogger(__name__)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@shared_task(name="app.workers.tasks.pull_orders_tiktok")
def pull_orders_tiktok() -> dict:
    """
    TODO: Implement TikTok Shop order pull.
    Expected behavior:
      - Fetch new/updated orders since last cursor
      - Upsert orders into PostgreSQL
    """
    logger.warning("Running pull_orders_tiktok at %s", _now_iso())
    return {"channel": "tiktok", "status": "stub", "ts": _now_iso()}


@shared_task(name="app.workers.tasks.pull_orders_shopee")
def pull_orders_shopee() -> dict:
    """
    TODO: Implement Shopee order pull.
    """
    logger.warning("Running pull_orders_shopee at %s", _now_iso())
    return {"channel": "shopee", "status": "stub", "ts": _now_iso()}


@shared_task(name="app.workers.tasks.pull_orders_lazada")
def pull_orders_lazada() -> dict:
    """
    TODO: Implement Lazada order pull.
    """
    logger.warning("Running pull_orders_lazada at %s", _now_iso())
    return {"channel": "lazada", "status": "stub", "ts": _now_iso()}


@shared_task(name="app.workers.tasks.sync_excel_inventory_to_db")
def sync_excel_inventory_to_db() -> dict:
    """
    TODO: Implement Excel master inventory -> DB sync.
    Expected behavior:
      - Load Excel file from configured source (local path, S3, Google Drive, etc.)
      - Parse via openpyxl
      - Upsert SKUs, costs, quantities, variants into DB
    """
    logger.warning("Running sync_excel_inventory_to_db at %s", _now_iso())
    return {"job": "excel_sync", "status": "stub", "ts": _now_iso()}


@shared_task(name="app.workers.tasks.reconcile_stock")
def reconcile_stock() -> dict:
    """
    TODO: Implement stock reconciliation.
    Expected behavior:
      - Compare DB inventory vs channel inventory snapshots
      - Produce "to_push" deltas / discrepancies
    """
    logger.warning("Running reconcile_stock at %s", _now_iso())
    return {"job": "reconcile_stock", "status": "stub", "ts": _now_iso()}


@shared_task(name="app.workers.tasks.push_stock_updates_to_channels")
def push_stock_updates_to_channels() -> dict:
    """
    TODO: Implement pushing stock updates to channels.
    Expected behavior:
      - Read pending deltas from DB
      - Push to TikTok/Shopee/Lazada APIs
      - Mark success/fail with retry strategy
    """
    logger.warning("Running push_stock_updates_to_channels at %s", _now_iso())
    return {"job": "push_stock", "status": "stub", "ts": _now_iso()}
