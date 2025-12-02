from repositories.artwork_repo import ArtworkRepository
from repositories.order_repo import OrderRepository

class BuyerService:
    def __init__(self, user_id: int):
        self.artwork_repo = ArtworkRepository()
        self.user_id = user_id

    def browse_artwork(self):
        return self.artwork_repo.find_all_available()

    def place_order(self, artwork_id: int, quantity: int):
        artwork = ArtworkRepository.find_by_artwork_id(artwork_id)
        if not artwork or not artwork.is_available:
            raise ValueError('Artwork not found')

        total_price = artwork.price * quantity
        return OrderRepository.create_order(
            buyer_id=self.user_id,
            artwork_id=artwork_id,
            quantity=quantity,
            total_price=total_price
        )
