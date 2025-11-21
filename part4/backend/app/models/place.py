from uuid import uuid4
from sqlalchemy import Column, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import db
from .base_model import BaseModel

# Table d'association pour la relation plusieurs-à-plusieurs entre Place et Amenity
place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(db.Model):
    __tablename__ = 'places'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Relations
    owner = db.relationship("User", back_populates="places")  # Relation avec User
    reviews = db.relationship("Review", back_populates="place", cascade="all, delete-orphan")  # Relation avec Review
    amenities = db.relationship("Amenity", secondary=place_amenity, backref="places")  # Relation avec Amenity via table d'association

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'reviews': [review.to_dict() for review in self.reviews],
            'amenities': [amenity.name for amenity in self.amenities]
        }
