from typing import Optional, List, Dict, Any
from sqlalchemy.exc import IntegrityError
from config.config import db
from models.artwork import ArtWork

class ArtworkRepository:
    @staticmethod
    def create_artwork(name: str, description: str, image_url: str,
                       price: float, category: str, artist_id: int, is_available: bool = True) -> ArtWork:
        try:
            artwork = ArtWork(
                name=name,
                description=description,
                image_url=image_url,
                price=price,
                category=category,
                artist_id=artist_id,
                is_available=is_available
            )
            db.session.add(artwork)
            db.session.commit()
            return artwork
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError("Unable to create new Artwork. Probably invalid artist id or duplicate error.") from e

    @staticmethod
    def find_by_artwork_id(artwork_id: int) -> Optional[ArtWork]:
        return db.session.query(ArtWork).get(artwork_id)

    @staticmethod
    def find_by_artist_id(artist_id: int) -> List[ArtWork]:
        return db.session.query(ArtWork).filter_by(artist_id=artist_id).all()

    @staticmethod
    def find_all_available() -> List[ArtWork]:
        return db.session.query(ArtWork).filter(ArtWork.is_available == True).all()

    @staticmethod
    def update_artwork(artwork_id: int, updated_data: Dict[str, Any]) -> Optional[ArtWork]:
        artwork = ArtworkRepository.find_by_artwork_id(artwork_id)
        if not artwork:
            return None
        allowed_fields = ['name', 'description', 'image_url', 'price', 'category', 'artist_id', 'is_available']
        for key, value in updated_data.items():
            if key in allowed_fields:
                setattr(artwork, key, value)
        try:
            db.session.commit()
            return artwork
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError("Unable to update Artwork. Probably invalid artist id or duplicate error.") from e

    @staticmethod
    def delete_artwork(artwork_id: int) -> bool:
        artwork = ArtworkRepository.find_by_artwork_id(artwork_id)
        if not artwork:
            return False
        db.session.delete(artwork)
        db.session.commit()
        return True

    def find_all_available(self):
        pass