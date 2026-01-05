# app/workers/tasks.py

import logging
import time
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(name="app.workers.tasks.heartbeat")
def heartbeat() -> str:
    """
    Optional monitoring task. Enable scheduling in celery_app.py if you want it.
    """
    logger.warning("HEARTBEAT task executed")
    time.sleep(1)
    return "ok"
