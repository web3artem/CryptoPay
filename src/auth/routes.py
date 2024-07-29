from fastapi import APIRouter, Depends

from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession

from .auth import auth_backend
from .manager import get_user_manager
from .models import User

from database import get_async_session
from .schemas import PayoutWalletUpdate

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)


# Ручка для добавления ERC20 адреса после регистрации
@router.patch("/add-payout-wallet")
async def add_wallet(wallet_update: PayoutWalletUpdate,
                     user: User = Depends(fastapi_users.current_user()),
                     db: AsyncSession = Depends(get_async_session)):
    user.payout_address = wallet_update.wallet_address
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
