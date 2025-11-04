from repositories.artwork_repo import ArtworkRepository
from repositories.order_repo import OrderRepository


class BuyerService:
    def __init__(self, db, user_id):
        self.artwork_repo = ArtworkRepository(db)
        self.order_repo = OrderRepository(db)
        self.user_id = user_id

    def browse_artwork(self):
        return self.artwork_repo.find_all_available()

    def place_order(self, artwork_id, quantity):
        artwork = self.artwork_repo.find_by_artwork_id(artwork_id)
        if not artwork or not artwork.is_available:
            raise ValueError('Artwork not found')

        total_price = artwork.price * quantity
        return self.order_repo.create_order(self.user_id, artwork_id, total_price, quantity)
