from sqlalchemy.exc import SQLAlchemyError

from config.config import db
from models.artwork import ArtWork
from models.cart import Cart
from models.cart_item import CartItem


class CartRepository:

    @staticmethod
    def get_cart_or_create_cart(buyer_id: int):
        cart = Cart.query.filter_by(buyer_id=buyer_id).first()
        if not cart:
            cart = Cart(buyer_id=buyer_id)
            db.session.add(cart)
            db.session.commit()
        return cart

    @staticmethod
    def add_to_cart(buyer_id: int, artwork_id: int, quantity: int = 1):
        try:
            cart = CartRepository.get_cart_or_create_cart(buyer_id)
            artwork = ArtWork.query.get(artwork_id)
            if not artwork:
                raise ValueError("Artwork not found")
            cart_item = CartItem.query.filter_by(cart_id=cart.id, artwork_id=artwork_id).first()
            if cart_item:
                cart_item.quantity += quantity
                cart_item.subtotal = cart_item.quantity * artwork.price
            else:
                subtotal = artwork.price * quantity
                new_item = CartItem(cart_id=cart.id, artwork_id=artwork_id, quantity=quantity, subtotal=subtotal)
                db.session.add(new_item)
            db.session.commit()
            db.session.refresh(cart)
            return cart
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Database error: {str(e)}")

    @staticmethod
    def get_cart_by_buyer(buyer_id: int):
        return Cart.query.filter_by(buyer_id=buyer_id).first()

    @staticmethod
    def delete_from_cart(card_id: int, artwork_id: int):
        try:
            cart_item = Cart.query.filter_by(cart_id=card_id, artwork_id=artwork_id).first()
            if not cart_item:
                raise ValueError("Cart-item not found")
            db.session.delete(cart_item)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Database error: {str(e)}")

    @staticmethod
    def clear_cart(cart_id: int):
        try:
            Cart.query.filter_by(cart_id=cart_id).delete()
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Database error: {str(e)}")