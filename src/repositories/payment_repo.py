from typing import Optional, List, Dict, Any

from sqlalchemy.exc import IntegrityError

from config.config import db
from models.payment import Payment

class PaymentRepository:
    @staticmethod
    def create_payment(order_id: int, amount: float, payment_method: str="pending", payment_status: str="pending") -> Payment:
        try:
            payment = Payment(
                order_id=order_id,
                amount=amount,
                payment_method=payment_method,
                payment_status=payment_status
            )
            db.session.add(payment)
            db.session.commit()
            return payment
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError("Unable to make payment. Or Invalid Order Id or data.") from e

    @staticmethod
    def get_payment_by_id(payment_id: int) -> Optional[Payment]:
        return db.session.query(Payment).get(payment_id)

    @staticmethod
    def get_payment_by_order(order_id: int) -> Optional[Payment]:
        return db.session.query(Payment).filter_by(order_id=order_id).all()

    @staticmethod
    def get_all_payments() -> List[Payment]:
        return db.session.query(Payment).all()

    @staticmethod
    def get_payment_by_status(payment_status: str) -> List[Payment]:
        return db.session.query(Payment).filter_by(payment_status=payment_status).all()

    @staticmethod
    def update_payment(payment_id: int, updated_data: Dict[str, Any])-> Optional[Payment]:
        payment = PaymentRepository.get_payment_by_id(payment_id)
        if not payment:
            return None
        allowed_fields = ["order_id", "amount", "payment_method", "payment_status"]
        for key, value in updated_data.items():
            if key in allowed_fields:
                setattr(payment, key, value)
        try:
            db.session.commit()
            return payment
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError("Unable to make payment. Or Invalid Order Id or data.") from e

    @staticmethod
    def delete_payment(payment_id: int) -> bool:
        payment = PaymentRepository.get_payment_by_id(payment_id)
        if not payment:
            return False
        db.session.delete(payment)
        db.session.commit()
        return True