from eth_account import Account
from fastapi import Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from currency.models import Currency
from database import get_async_session
from .models import Wallet, Payment


# Создание ERC20 кошелька
async def create_wallet(db: AsyncSession = Depends(get_async_session)):
    wallet = Account.create()
    async with db as session:
        new_wallet = Wallet(wallet_key=wallet.address,
                            wallet_pk=wallet.key.hex())
        session.add(new_wallet)
        await session.commit()
        return new_wallet


async def check_ticker_availability(ticker: str, db: AsyncSession = Depends(get_async_session)):
    if ticker.lower() in ('arbitrum', 'ethereum', 'optimism', 'zksync'):
        ticker = 'ETH'
    async with db as session:
        stmt = select(Currency.ticker)
        result = await session.execute(stmt)
        tickers = result.scalars().all()
        if ticker in tickers:
            return True, ticker
        return False


async def get_payment_by_id(payment_id: int, db: AsyncSession = Depends(get_async_session)):
    async with db as session:
        query = (select(Payment)
                 .options(selectinload(Payment.wallet))
                 .where(Payment.id == payment_id))
        print(query)
        result = await session.execute(query)
        payment = result.scalars().first()
        return payment
