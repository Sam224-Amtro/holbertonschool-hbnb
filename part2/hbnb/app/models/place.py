from uuid import uuid4
from datetime import datetime

class Place:
    def __init__(self, title, description, price, latitude, longitude, owner):
        self.id = str(uuid4())
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []

    def add_review(self, review):
        """Add a review to the place"""
        self.reviews.append(review)


    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner,
            'reviews': [review.to_dict() for review in self.reviews]
        }
