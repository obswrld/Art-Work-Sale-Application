from typing import List, Dict, Any, Optional
from sqlalchemy.exc import IntegrityError
from config.config import db
from src.models.order import Order

class OrderRepository:
    @staticmethod
    def create_order(buyer_id: int, artwork_id: int, quantity: int, total_price: float, payment_status: str = "pending") -> Order:
        try:
            order = Order(
                buyer_id=buyer_id,
                artwork_id=artwork_id,
                quantity=quantity,
                total_price=total_price,
                payment_status=payment_status
            )
            db.session.add(order)
            db.session.commit()
            db.session.refresh(order)
            return order
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError("Failed to create order. Invalid buyer_id or artwork_id.")from e

    @staticmethod
    def get_all_orders() -> List[Order]:
        return db.session.query(Order).all()

    @staticmethod
    def get_orders_by_id(order_id: int) -> Optional[Order]:
        order = db.session.get(Order, order_id)
        return order

    @staticmethod
    def get_orders_by_buyer_id(buyer_id: int) -> List[Order]:
        return db.session.query(Order).filter_by(buyer_id=buyer_id).all()

    @staticmethod
    def get_orders_by_artwork_id(artwork_id: int) -> List[Order]:
        return db.session.query(Order).filter_by(artwork_id=artwork_id).all()

    @staticmethod
    def get_order_by_payment_status(payment_status: str) -> List[Order]:
        return db.session.query(Order).filter_by(payment_status=payment_status).all()

    @staticmethod
    def update_order(order_id: int, updated_data: Dict[str, Any]) -> list[Order] | None:
        order = OrderRepository.get_orders_by_id(order_id)
        if not order:
            return None
        allowed_fields = {"payment_status", "total_price", "quantity"}
        for key, value in updated_data.items():
            if key in allowed_fields:
                setattr(order, key, value)
        try:
            db.session.commit()
            db.session.refresh(order)
            return order
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError("Failed to update order.") from e

    @staticmethod
    def delete_order(order_id: int) -> bool:
        order = OrderRepository.get_orders_by_id(order_id)
        if not order:
            return False
        db.session.delete(order)
        db.session.commit()
        return True