from repositories import ArtworkRepository

class ArtworkService:
    def __init__(self, artist_id: int):
        self.artwork_repo = ArtworkRepository()
        self.artist_id = artist_id

    def upload_artwork(self, artwork_data):
        return self.artwork_repo.create_artwork(
            name=artwork_data.name,
            description=artwork_data.description,
            image_url=artwork_data.image_url,
            price=artwork_data.price,
            category=artwork_data.category,
            artist_id=artwork_data.artist_id
        )

    def get_my_artworks(self):
        return self.artwork_repo.find_by_artist_id(self.artist_id)