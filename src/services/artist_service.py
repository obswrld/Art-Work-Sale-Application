from repositories.artwork_repo import ArtworkRepository


class ArtworkService:
    def __init__(self, db, artist_id):
        self.repo = ArtworkRepository(db)
        self.artist_id = artist_id

    def upload_artwork(self, artwork_data):
        return self.repo.create_artwork(artist_id=self.artist_id, **artwork_data.dict())

    def get_my_artworks(self):
        return self.repo.find_by_artist_id(self.artist_id)