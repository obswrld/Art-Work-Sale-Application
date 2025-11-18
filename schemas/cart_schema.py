from datetime import datetime
from typing import List
from pydantic import BaseModel

class CartSchema(BaseModel):
    buyer_id: int

class CartItemSchemaResponse(BaseModel):
    id: int
    cart_id: int
    artwork_id: int
    quantity: int
    subtotal: float

    class Config:
        from_attributes = True

class CartResponse(BaseModel):
    id: int
    buyer_id: int
    created_at: datetime
    updated_at: datetime
    items: List[CartItemSchemaResponse] = []

    class Config:
        from_attributes = True