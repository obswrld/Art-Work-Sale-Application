from datetime import datetime
from enum import Enum
from passlib.handlers.bcrypt import bcrypt
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SqlEnum
from config.config import db

class Role(Enum):
    BUYER = "buyer"
    ARTIST = "artist"
    ADMIN = "admin"

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(120), nullable=False)
    role = Column(SqlEnum(Role), default=Role.BUYER,  nullable=False)
    is_verified = Column(Boolean, nullable=False, default=False)
    verification_code = Column(String(120), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def set_password(self, password: str):
        self.password = bcrypt.hash(password)

    def check_password(self, password: str) -> bool:
        return bcrypt.verify(password, self.password)

    def __repr__(self):
        return f"<User {self.email}>"