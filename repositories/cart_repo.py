from typing import Optional
from sqlalchemy.exc import SQLAlchemyError
from config.config import db
from models.artwork import ArtWork
from models.cart import Cart
from models.cart_item import CartItem


class CartRepository:

    @staticmethod
    def get_cart_or_create_cart(buyer_id: int):
        cart = db.session.query(Cart).filter_by(buyer_id=buyer_id).first()
        if not cart:
            cart = Cart(buyer_id=buyer_id)
            db.session.add(cart)
            db.session.commit()
            db.session.refresh(cart)
        return cart

    @staticmethod
    def add_to_cart(buyer_id: int, artwork_id: int, quantity: int = 1) -> Cart:
        try:
            cart = CartRepository.get_cart_or_create_cart(buyer_id)
            artwork = db.session.get(ArtWork, artwork_id)
            if not artwork:
                raise ValueError("Artwork not found")

            # FIXED: Changed cart.id to cart.cart_id
            cart_item = db.session.query(CartItem).filter_by(
                cart_id=cart.cart_id,
                artwork_id=artwork_id
            ).first()

            if cart_item:
                cart_item.quantity += quantity
                cart_item.subtotal = cart_item.quantity * artwork.price
            else:
                subtotal = artwork.price * quantity
                new_item = CartItem(
                    cart_id=cart.cart_id,
                    artwork_id=artwork_id,
                    quantity=quantity,
                    subtotal=subtotal
                )
                db.session.add(new_item)

            db.session.commit()
            db.session.refresh(cart)
            return cart
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RuntimeError(f"Database error {e.__class__.__name__} - {str(e)}") from e

    @staticmethod
    def get_cart_by_buyer(buyer_id: int) -> Optional[Cart]:
        return db.session.query(Cart).filter_by(buyer_id=buyer_id).first()

    @staticmethod
    def remove_from_cart(cart_id: int, artwork_id: int) -> bool:
        try:
            item = db.session.query(CartItem).filter_by(
                cart_id=cart_id,
                artwork_id=artwork_id
            ).first()
            if not item:
                return False
            db.session.delete(item)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RuntimeError(f"Database error: {e.__class__.__name__} - {str(e)}") from e

    @staticmethod
    def clear_cart(cart_id: int):
        try:
            db.session.query(CartItem).filter_by(cart_id=cart_id).delete()
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RuntimeError(f"Database error: {e.__class__.__name__} - {str(e)}") from e