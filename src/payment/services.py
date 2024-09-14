from eth_account import Account
from fastapi import Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from currency.models import Currency
from database import get_async_session


# Создание ERC20 кошелька
def create_wallet():
    wallet = Account.create()
    return wallet


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
