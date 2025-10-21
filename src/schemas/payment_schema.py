from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

class PaymentStatusSchema(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

class PaymentMethodSchema(str, Enum):
    CARD = "CARD"
    TRANSFER = "TRANSFER"

class CreatePaymentSchema(BaseModel):
    order_id: str
    amount: float = Field(..., gt=0)
    payment_method: PaymentMethodSchema

class PaymentResponseSchema(BaseModel):
    payment_id = int
    order_id: int
    amount: float
    payment_method: PaymentMethodSchema
    status: PaymentStatusSchema
    created_at: datetime

    class Config:
        from_attribute = True