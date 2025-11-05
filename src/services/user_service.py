from typing import Optional
from pydantic import EmailStr
from repositories.user_repo import UserRepository
from schemas.user_schema import CreateUserSchema, UserResponseSchema, LoginUserSchema
from passlib.hash import bcrypt


class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def register(self, user_data: CreateUserSchema) -> UserResponseSchema:
        existing_user = self.repo.find_by_email(user_data.email)
        if existing_user:
            raise ValueError("Email already exists")
        hashed_password = bcrypt.hash(user_data.password)
        verification_token = user_data.generate_token()
        new_user = self.repo.create_user(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            role=user_data.role,
            password=hashed_password,
            verification_code=verification_token,
        )
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
        if not user or not bcrypt.verify(login_data.password, user.password):
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
        updated_user = self.repo.update_user(user_id, update_data)
        if not updated_user:
            raise ValueError("User does not exist or updates failed")
        return UserResponseSchema.model_validate(updated_user)

    def delete_user(self, user_id: int)-> bool:
        return self.repo.delete_user(user_id)