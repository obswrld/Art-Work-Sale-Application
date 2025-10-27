from enum import Enum
from datetime import datetime
from config.config import db
from sqlalchemy import Column, Integer, ForeignKey, Float, Enum as SqlEnum, DateTime
from sqlalchemy.orm import relationship

class PaymentStatus(Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

class PaymentMethod(Enum):
    CARD = "CARD"
    TRANSFER = "TRANSFER"

class Payment(db.Model):
    __tablename__ = "payment"

    payment_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(SqlEnum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    payment_method = Column(SqlEnum(PaymentMethod), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    order = relationship("Order", backref="payments")

    def __repr__(self):
        return f"<Payment {self.payment_id}>"