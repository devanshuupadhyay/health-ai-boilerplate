# backend/celery_worker.py
from celery import Celery
from app.core.config import settings

celery = Celery(__name__)

# Use the update method to apply all settings at once
celery.conf.update(
    broker_url=settings.CELERY_BROKER_URL,
    result_backend=settings.CELERY_RESULT_BACKEND,
)

# Autodiscover tasks
celery.autodiscover_tasks(["app.tasks.process_note"])
