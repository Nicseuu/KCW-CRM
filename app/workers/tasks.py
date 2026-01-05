# app/workers/tasks.py

import logging
import time
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(name="app.workers.tasks.heartbeat")
def heartbeat() -> str:
    """
    Beat should enqueue this, worker should run it.
    Check worker logs for: "HEARTBEAT task executed"
    """
    logger.warning("HEARTBEAT task executed")
    time.sleep(1)
    return "ok"
