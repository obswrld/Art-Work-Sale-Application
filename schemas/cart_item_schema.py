from pydantic import BaseModel, Field


class CartItemSchema(BaseModel):
    cart_id: int
    artwork_id: int
    quantity: int = Field(default=1, gt=0)
    subtotal: float = Field(..., gt=0)

    class Config:
        from_attributes = True