from typing import Optional
from pydantic import EmailStr
from models.user import User
from repositories.user_repo import UserRepository
from schemas.user_schema import CreateUserSchema, UserResponseSchema, LoginUserSchema
from passlib.hash import bcrypt


class UserService:
    def __init__(self, db):
        self.repo = UserRepository()

    def register(self, user_data: CreateUserSchema) -> UserResponseSchema:
        existing_user = self.repo.find_by_email(user_data.email)
        if existing_user:
            raise ValueError("Email already exists")
        hashed_password = bcrypt.hash(user_data.password)
        verification_token = user_data.generate_token()
        new_user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            password=hashed_password,
            verification_code=verification_token,
        )
        self.repo.create_user(new_user)
        return UserResponseSchema.model_validate(new_user)

    def verify_user(self, token: str)-> bool:
        user = self.repo.find_by_verification_code(token)
        if not user:
            raise ValueError("Invalid verification Code")
        user.is_verified = True
        user.verification_code = None
        self.repo.save(user)
        return True

    def login_user(self, login_data: LoginUserSchema) -> UserResponseSchema:
        user = self.repo.find_by_email(login_data.email)
        if not user:
            raise ValueError("Invalid email or password")
        if not bcrypt.verify(login_data.password, user.password):
            raise ValueError("Invalid email or password")
        if not user.is_verified:
            raise ValueError("Please verify your email")
        return UserResponseSchema.model_validate(user)

    def get_user_by_id(self, user_id: int)-> Optional[UserResponseSchema]:
        user = self.repo.find_by_user_id(user_id)
        if not user:
            return None
        return UserResponseSchema.model_validate(user)

    def get_user_by_email(self, email: EmailStr)-> Optional[UserResponseSchema]:
        user = self.repo.find_by_email(email)
        if not user:
            return None
        return UserResponseSchema.model_validate(user)

    def update_user(self, user_id: int, update_data: dict)-> UserResponseSchema:
        user = self.repo.find_by_user_id(user_id)
        if not user:
            raise ValueError("User does not exist")

        for key, value in update_data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        self.repo.save(user)
        return UserResponseSchema.model_validate(user)

    def delete_user(self, user_id: int)-> bool:
        user = self.repo.find_by_user_id(user_id)
        if not user:
            raise ValueError("User does not exist")
        self.repo.delete_user(user)
        return True