from pydantic import BaseModel, Field
from sqlalchemy import Float


class CartItemSchema(BaseModel):
    cart_id: int
    artwork_id: int
    quantity: int = Field(default=1, gt=0)
    subtotal: Float = Field(..., gt=0)

class CartItemSchemaResponse(BaseModel):
    id: int
    cart_id: int
    artwork_id: int
    quantity: int
    subtotal: float

    class Config:
        from_attribute = True