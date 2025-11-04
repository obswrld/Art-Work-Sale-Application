from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class OrderStatusSchema(str, Enum):
    PAID = "PAID"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"

class OrderSchema(BaseModel):
    buyer_id: int
    artwork_id: int
    quantity: int = Field(default=1, gt=0)
    total_price: float = Field(..., gt=0)

class OrderResponseSchema(BaseModel):
    id: int
    buyer_id: int
    artwork_id: int
    quantity: int
    total_price: float
    status: OrderStatusSchema
    created_at: datetime

    class Config:
        from_attributes = True