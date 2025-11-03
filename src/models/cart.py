from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime
from config.config import db
from sqlalchemy.orm import relationship

class Cart(db.model):
    __tablename__ = 'cart'

    cart_id = Column(Integer, primary_key=True)
    buyer_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    buyer = relationship("User", "carts")
    item = relationship("CartItem", "carts", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Cart {self.cart_id}>"