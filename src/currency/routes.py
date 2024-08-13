import httpx

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from currency.models import Currency

from database import get_async_session
from auth.models import User
from auth.routes import fastapi_users

router = APIRouter(
    tags=['currency']
)


@router.get("/currencies", description="Метод для получения информации о всех криптовалютах доступных для платежей.")
async def get_currencies(db: AsyncSession = Depends(get_async_session)):
    query = select(Currency.blockchain)
    res = await db.execute(query)
    currencies = res.scalars().all()
    return {"currencies": currencies}


@router.get("/estimate", description="Метод для получения приблизительной цены в криптовалюте для фиатной валюты")
async def convert_fiat_to_crypto(amount: int,
                                 currency_from: str,
                                 currency_to: str,
                                 user: User = Depends(fastapi_users.current_user())):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"https://api.coinconvert.net/convert/{currency_from}/{currency_to}?amount={amount}")
        if r.status_code == 403:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"status": "error", "message": r.json()["message"]}
            )

        data = r.json()
        return {"currency_from": currency_from,
                "amount_from": amount,
                "currency_to": currency_to,
                "estimated_amount": data.get(currency_to.upper())}
