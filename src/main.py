from fastapi import FastAPI

from auth.auth import auth_backend
from auth.schemas import UserRead, UserCreate
from auth.routes import fastapi_users, router as auth_router
from currency.routes import router as currency_router
from payment.routes import router as payment_router

app = FastAPI()


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(auth_router)
app.include_router(currency_router)
app.include_router(payment_router)


@app.get("/v1/status")
async def get_status():
    return {"message": "прикол"}
