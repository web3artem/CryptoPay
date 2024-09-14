from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from auth.models import User
from auth.routes import fastapi_users
from currency.routes import convert_fiat_to_crypto
from database import get_async_session, get_sync_session
from .models import Payment
from .schemas import PaymentCreation, PaymentStatus, PaymentResponse
from .services import create_wallet

from tasks.tasks import check_payment

router = APIRouter(
    prefix="",
    tags=["Payments"]
)


# Создание платежа
@router.post("/payment")
async def create_payment(payment: PaymentCreation,
                         user: User = Depends(fastapi_users.current_user()),
                         db: AsyncSession = Depends(get_async_session)):
    # Проверка возможности оплаты в переданной крипте
    # is_ticker_available = await check_ticker_availability(payment.pay_currency, db)

    # if not is_ticker_available[0]:
    #     return JSONResponse(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         content={"status": "error", "message": f"Нельзя оплатить в {payment.pay_currency}"}
    #     )

    response = await convert_fiat_to_crypto(payment.price_amount,
                                            payment.price_currency,
                                            payment.pay_currency,
                                            user)

    if isinstance(response, JSONResponse):
        return response

    pay_amount = float(response.get("estimated_amount"))
    wallet = create_wallet()

    new_payment = Payment(
        price_amount=payment.price_amount,
        price_currency=payment.price_currency,
        pay_currency=payment.pay_currency,
        pay_amount=pay_amount,
        order_id=str(payment.order_id),
        order_description=payment.order_description,
        payment_status=PaymentStatus.waiting,
        wallet_key=wallet.address,
        wallet_pk=wallet.key.hex(),
        user_id=user.id
    )

    async with db as session:
        session.add(new_payment)
        await session.commit()

    check_payment.delay(blockchain=payment.blockchain,
                        payment_id=new_payment.id,
                        wallet_address=new_payment.wallet_key,
                        pay_amount=new_payment.pay_amount)

    return PaymentResponse(
        payment_id=new_payment.id,
        payment_status=new_payment.payment_status,
        price_amount=new_payment.price_amount,
        price_currency=new_payment.price_currency,
        pay_amount=new_payment.pay_amount,
        pay_currency=new_payment.pay_currency,
        pay_address=new_payment.wallet_key,
        order_id=new_payment.order_id,
        order_description=new_payment.order_description,
        created_at=new_payment.created_at,
        updated_at=new_payment.updated_at
    )
