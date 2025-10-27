from datetime import datetime
from typing import List

from pydantic import BaseModel

class CartSchema(BaseModel):
    buyer_id: int

class CartResponse(BaseModel):
    cart_id: int
    buyer_id: int
    created_at: datetime
    updated_at: datetime
    items: List[CartSchema] = []

    class Config:
        from_attribute = True