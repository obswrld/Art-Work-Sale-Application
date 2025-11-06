from repositories.order_repo import OrderRepository
from repositories import PaymentRepository
from repositories import UserRepository


class AdminService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.payment_repo = PaymentRepository()
        self.order_repo = OrderRepository()

    def get_all_users(self):
        return self.user_repo.find_all_users()

    def get_all_orders(self):
        return self.order_repo.get_all_orders()

    def get_all_payments(self):
        return self.payment_repo.get_all_payments()
