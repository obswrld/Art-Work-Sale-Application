from sqlalchemy.exc import IntegrityError

from config.config import db
from models.user import User


class UserRepository:

    @staticmethod
    def create_user(first_name: str, last_name: str, email: str, role: str, password: str, verification_code: str):
        try:
            user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                role=role,
                password=password,
                verification_code=verification_code,
            )
            db.session.add(user)
            db.session.commit()
            return user
        except IntegrityError:
            db.session.rollback()
            raise ValueError("A user already exists")

    @staticmethod
    def get_user_by_email(email: str) -> User | None:
        return db.session.query(User).filter_by(email=email).first()

    @staticmethod
    def get_user_by_id(user_id: int) -> User | None:
        return db.session.query(User).get(user_id)

    @staticmethod
    def verify_user(email:str):
        user = UserRepository.get_user_by_email(email)
        if user:
            user.is_verified = True
            db.session.commit()
            return user
        return None

    @staticmethod
    def delete_user(user_id: int) -> bool:
        user = UserRepository.get_user_by_id(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False