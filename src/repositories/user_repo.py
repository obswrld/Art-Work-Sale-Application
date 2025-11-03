from typing import Optional, Dict, Any

from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError
from config.config import db
from models.user import User

class UserRepository:
    @staticmethod
    def create_user(first_name: str, last_name: str, email: EmailStr, role: str, password: str, verification_code: Optional[str] = None) -> User:
        try:
            user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                role=role,
                password=password,
                verification_code=verification_code,
            )
            if hasattr(user, "set_password"):
                user.set_password(password)
            else:
                user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return user
        except IntegrityError:
            db.session.rollback()
            raise ValueError("A user already exists")

    @staticmethod
    def find_by_email(email: EmailStr) -> User | None:
        return db.session.query(User).filter_by(email=email).first()

    @staticmethod
    def find_by_user_id(user_id: int) -> User | None:
        return db.session.get(User, user_id)

    @staticmethod
    def verify_user(email:EmailStr) -> Optional[User] | None:
        user = UserRepository.find_by_email(email)
        if not user:
            return None
        user.is_verified = True
        user.verification_code = None
        db.session.commit()
        return user

    @staticmethod
    def find_by_verification(code: str) -> Optional[User] | None:
        return db.session.query(User).filter_by(verification_code=code).first()

    @staticmethod
    def update_user(user_id: int, updated_data: Dict[str, Any])-> Optional[User]:
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            return None
        allowed_fields = ["first_name", "last_name", "email", "role", "password", "verification_code"]
        if "password" in updated_data:
            if hasattr(user, "set_password"):
                user.set_password(updated_data["password"])
            else:
                user.set_password(updated_data["password"])
            updated_data.pop("password", None)
        for key, value in list(updated_data.items()):
            if key in allowed_fields:
                setattr(user, key, value)
        try:
            db.session.commit()
            return user
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError("Update failed due to data constraint") from e

    @staticmethod
    def delete_user(user_id: int) -> bool:
        user = UserRepository.find_by_user_id(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False

    @staticmethod
    def save(user: User) -> User:
        db.session.add(user)
        db.session.commit()
        return user