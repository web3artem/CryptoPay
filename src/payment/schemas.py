from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class PaymentStatus(Enum):
    waiting = "waiting"
    confirming = "confirming"
    confirmed = "confirmed"
    sending = "sending"
    finished = "finished"
    failed = "failed"
    refunded = "refunded"
    expired = "expired"


class PaymentCreation(BaseModel):
    price_amount: float = Field(gt=0)
    price_currency: str
    pay_currency: str
    blockchain: str
    order_id: Optional[int | str] = None
    order_description: str


class PaymentResponse(BaseModel):
    payment_id: int
    payment_status: PaymentStatus
    price_amount: float
    price_currency: str
    pay_amount: float
    pay_currency: str
    pay_address: str
    order_id: Optional[int | str]
    order_description: str
    created_at: datetime
    updated_at: datetime


class GetPaymentStatusResponse(BaseModel):
    payment_id: int
    payment_status: PaymentStatus
    pay_address: str
    price_amount: float
    price_currency: str
    pay_amount: float
    pay_currency: str
