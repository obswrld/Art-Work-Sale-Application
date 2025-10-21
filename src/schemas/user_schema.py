import secrets
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, constr, EmailStr, model_validator

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

    @model_validator(mode="after")
    def check_password_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords don't match")
        return self

    @staticmethod
    def generate_token():
        return secrets.token_urlsafe(10)

class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str

class UserResponseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    role: UserRole
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True