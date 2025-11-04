from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, ForeignKey, Enum as SqlEnum, Float, DateTime
from sqlalchemy.orm import relationship
from config.config import db

class OrderStatus(Enum):
    PAID = "PAID"
    DELIVERED = "DELIVERED"
    SHIPPED = "SHIPPED"
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"

class Order(db.Model):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    artwork_id = Column(Integer, ForeignKey("artwork.id"), nullable=False)
    total_price = Column(Float, nullable=False)
    quantity = Column(Integer, default=1)
    status = Column(SqlEnum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)

    buyer = relationship("User", backref="orders")
    artwork = relationship("Artwork", backref="orders")

    def __repr__(self):
        return f"<Order {self.id}>"
