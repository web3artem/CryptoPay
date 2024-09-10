from celery import Celery

from config import settings

celery = Celery('tasks',
                broker=settings.CELERY_BROKER_URL,
                backend=settings.CELERY_RESULT_BACKEND)


@celery.task
def add(x, y):
    return x + y
