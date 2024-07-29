from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from currency.models import Currency

from database import get_async_session

router = APIRouter(
    prefix="/currencies",
    tags=['currency']
)


@router.get("/")
async def get_currencies(db: AsyncSession = Depends(get_async_session)):
    query = select(Currency.blockchain)
    res = await db.execute(query)
    currencies = res.scalars().all()
    return {"currencies": currencies}

