# app/workers/tasks.py

import time
from celery import shared_task


@shared_task(name="app.workers.tasks.heartbeat")
def heartbeat() -> str:
    """
    Simple task so you can confirm:
    Beat -> Redis -> Worker execution is working.
    """
    time.sleep(1)
    return "ok"
