from datetime import datetime, timedelta
from time import sleep
from decimal import Decimal, getcontext

from celery import Celery

from sqlalchemy import update

from config import settings
from auth.models import User # noqa
from payment.models import Payment
from payment.utils import BlockchainNode

from database import get_sync_session

celery = Celery('tasks',
                broker=settings.CELERY_BROKER_URL,
                backend=settings.CELERY_RESULT_BACKEND)


@celery.task
def check_payment(blockchain: str,
                  payment_id: int,
                  wallet_address: str,
                  pay_amount: float):
    node = BlockchainNode(blockchain).get_web3_instance()
    getcontext().prec = 18

    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=10)

    while datetime.now() <= end_time:
        wei_balance = node.eth.get_balance(wallet_address)
        ether_balance = Decimal(node.from_wei(wei_balance, 'ether'))
        if ether_balance >= Decimal(pay_amount):
            with get_sync_session() as session:
                stmt = (
                    update(Payment)
                    .where(Payment.id == payment_id)
                    .values(payment_status="confirmed")
                )
                session.execute(stmt)
                session.commit()
                return "Платеж выполнен успешно"
        sleep(5)

    with get_sync_session() as session:
        stmt = (
            update(Payment)
            .where(Payment.id == payment_id)
            .values(payment_status="expired")
        )
        session.execute(stmt)
        session.commit()
        return "Платеж не выполнен"
