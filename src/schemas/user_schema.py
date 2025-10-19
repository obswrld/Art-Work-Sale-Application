from enum import Enum
from typing import Optional

from pydantic import BaseModel, constr, EmailStr


class UserRole(str, Enum):
    BUYER = "BUYER"
    ARTIST = "ARTIST"
    ADMIN = "ADMIN"

class CreateUserSchema(BaseModel):
    first_name: constr(min_length=3, max_length=30)
    last_name: constr(min_length=3, max_length=30)
    email: EmailStr
    password: constr(min_length=8)
    confirm_password: constr(min_length=8)
    role: Optional[UserRole] = UserRole.BUYER