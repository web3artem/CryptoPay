from sqlalchemy import ForeignKey, Integer, Text, String, Float, Enum, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from .schemas import PaymentStatus


class Payment(Base):
    __tablename__ = "payment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[str] = mapped_column(Text, nullable=True)
    order_description: Mapped[str] = mapped_column(Text, nullable=True)
    price_amount: Mapped[int] = mapped_column(Float)
    price_currency: Mapped[str] = mapped_column(String)
    pay_amount: Mapped[int] = mapped_column(Float)
    pay_currency: Mapped[str] = mapped_column(String)
    payment_status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), default=PaymentStatus.waiting)

    wallet_id: Mapped[int] = mapped_column(Integer, ForeignKey("wallet.id"))
    wallet = relationship("Wallet", back_populates="payments")

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="payments")

    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, onupdate=func.now(), default=func.now())


class Wallet(Base):
    __tablename__ = "wallet"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wallet_key: Mapped[str] = mapped_column(String, nullable=False)
    wallet_pk: Mapped[str] = mapped_column(String, nullable=False)

    payments = relationship("Payment", back_populates="wallet")
