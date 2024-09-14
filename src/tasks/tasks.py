from celery import Celery

from eth_account import Account

from config import settings
from database import get_sync_session

celery = Celery('tasks',
                broker=settings.CELERY_BROKER_URL,
                backend=settings.CELERY_RESULT_BACKEND)


# @celery.task
# async def create_wallet():
#     wallet = Account.create()
#     with get_sync_session() as session:
