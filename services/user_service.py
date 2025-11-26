from typing import Optional
from pydantic import EmailStr, validate_email
from repositories.user_repo import UserRepository
from schemas.user_schema import CreateUserSchema, UserResponseSchema, LoginUserSchema
from passlib.hash import bcrypt
import re

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    @staticmethod
    def validate_password_strength(password: str) -> None:
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', password):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', password):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', password):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValueError('Password must contain at least one special character')

    def register(self, user_data: CreateUserSchema) -> UserResponseSchema:
        if not user_data.email:
            raise ValueError('Email address required')
        if not user_data.password:
            raise ValueError('Password required')
        try:
            validate_email(user_data.email)
        except Exception:
            raise ValueError(f'Invalid email address: {user_data.email}')

        existing_user = self.repo.find_by_email(user_data.email)
        if existing_user:
            raise ValueError(f'User with email {user_data.email} already exists')

        self.validate_password_strength(user_data.password)
        hashed_password = bcrypt.hash(user_data.password)
        verification_token = user_data.generate_token()

        new_user = self.repo.create_user(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            role=user_data.role,
            password=hashed_password,
            verification_code=verification_token
        )
        return UserResponseSchema.model_validate(new_user)

    def verify_user(self, token: str) -> bool:
        user = self.repo.find_by_verification_code(token)
        if not user:
            raise ValueError('Invalid verification code')
        user.is_verified = True
        user.verification_code = None
        self.repo.save(user)
        return True

    def login_user(self, login_data: LoginUserSchema) -> UserResponseSchema:
        try:
            validate_email(login_data.email)
        except Exception:
            raise ValueError(f'Invalid email address format: {login_data.email}')

        user = self.repo.find_by_email(login_data.email)
        if not user:
            raise ValueError(f'User with email {login_data.email} not found')
        if not bcrypt.verify(login_data.password, user.password):
            raise ValueError(f'Incorrect password')
        if not user.is_verified:
            raise ValueError(f'Email {login_data.email} has not been verified yet')  # FIXED: message was backwards
        return UserResponseSchema.model_validate(user)

    def get_user_by_id(self, user_id: int) -> Optional[UserResponseSchema]:
        user = self.repo.find_by_user_id(user_id)
        if not user:
            return None
        return UserResponseSchema.model_validate(user)

    def get_user_by_email(self, email: EmailStr) -> Optional[UserResponseSchema]:
        try:
            validate_email(email)
        except Exception:
            raise ValueError(f'Invalid email address format: {email}')
        user = self.repo.find_by_email(email)
        if not user:
            return None
        return UserResponseSchema.model_validate(user)

    def update_user(self, user_id: int, update_data: dict) -> UserResponseSchema:
        updated_user = self.repo.update_user(user_id, update_data)
        if not updated_user:
            raise ValueError(f'User with id {user_id} not found')
        return UserResponseSchema.model_validate(updated_user)

    def delete_user(self, user_id: int) -> bool:
        result = self.repo.delete_user(user_id)
        if not result:
            raise ValueError(f'User with id {user_id} not found')
        return result