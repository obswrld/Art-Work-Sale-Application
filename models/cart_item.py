from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from config.config import db

class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey('carts.cart.id'), nullable=False)
    artwork_id = Column(Integer, ForeignKey('artwork.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    subtotal = Column(Float, nullable=False)

    cart = relationship("Cart", backref="cart_items")
    artwork = relationship("Artwork", backref="cart_items")

    def __repr__(self):
        return f"<Cart-items={self.id}>"