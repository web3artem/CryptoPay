from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from auth.models import User
from auth.routes import fastapi_users
from currency.routes import convert_fiat_to_crypto
from database import get_async_session
from .models import Payment
from .schemas import PaymentCreation
from .schemas import PaymentStatus

router = APIRouter(
    prefix="",
    tags=["Payments"]
)


# Создание платежа
@router.post("/payment")
async def create_payment(payment: PaymentCreation,
                         user: User = Depends(fastapi_users.current_user()),
                         db: AsyncSession = Depends(get_async_session)):
    response = await convert_fiat_to_crypto(payment.price_amount,
                                            payment.price_currency,
                                            payment.pay_currency,
                                            user)

    if isinstance(response, JSONResponse):
        return response

    pay_amount = float(response.get("estimated_price"))

    new_payment = Payment(
        price_amount=payment.price_amount,
        price_currency=payment.price_currency,
        pay_currency=payment.pay_currency,
        pay_amount=pay_amount,
        order_id=payment.order_id,
        order_description=payment.order_description,
        payment_status=PaymentStatus.waiting
    )
    async with db as session:
        session.add(new_payment)
        await session.commit()
