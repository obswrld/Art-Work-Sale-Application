from datetime import datetime
from typing import Optional
from pydantic import BaseModel, constr, Field


class CreateArtworkSchema(BaseModel):
    name: constr(min_length=3, max_length=100)
    description: Optional[str]
    price: float = Field(..., gt=0)
    image_url = str
    category: Optional[str]


class ArtWorkResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    image_url: str
    category: Optional[str]
    is_available: bool
    created_at: datetime
    artist_id = int

    class Config:
        from_attributes = True
