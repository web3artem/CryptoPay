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
    order_id: Optional[int | str] = None
    order_description: Optional[int]