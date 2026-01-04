from __future__ import annotations

from fastapi import APIRouter
from app.workers.tasks.stock_tasks import shopee_push_stock_task

router = APIRouter()
MVP_ORG_ID = 1

@router.post("/run")
def run_sync(job_type: str, base_url: str | None = None, access_token: str | None = None):
    """
    MVP manual trigger.
    Example:
      job_type=PUSH_STOCK_SHOPEE&base_url=...&access_token=...
    """
    if job_type == "PUSH_STOCK_SHOPEE":
        if not base_url or not access_token:
            return {"ok": False, "error": "base_url and access_token required"}
        task = shopee_push_stock_task.delay(org_id=MVP_ORG_ID, base_url=base_url, access_token=access_token)
        return {"ok": True, "task_id": task.id}

    return {"ok": False, "error": f"unknown job_type: {job_type}"}
