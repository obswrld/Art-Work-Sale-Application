from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Float
from sqlalchemy.orm import relationship
from config.config import db

class ArtWork(db.Model):
    __tablename__ = 'artwork'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    image_url = Column(String(225), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(100), nullable=False)
    category = Column(String(30), nullable=False)
    is_available = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    artist_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    artist = relationship("User", backref="artworks")

    def __repr__(self):
        return f"<ArtWork {self.id}>"
