from uuid import uuid4
from datetime import datetime

class Review:
    def __init__(self, text, rating, user_id, place_id):
        self.id = str(uuid4())
        self.text = text
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user_id,
            'place_id': self.place_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
