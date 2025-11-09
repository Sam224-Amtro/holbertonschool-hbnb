from app import db
from app.models import User, Place, Review, Amenity


user = User(first_name="John", last_name="Doe", email="john.doe@example.com", password="password")
db.session.add(user)
db.session.commit()


place = Place(title="Beautiful House", description="A lovely house in the countryside", price=150, latitude=48.8566, longitude=2.3522, owner_id=user.id)
db.session.add(place)
db.session.commit()


review = Review(text="Great place!", rating=5, user_id=user.id, place_id=place.id)
db.session.add(review)
db.session.commit()


amenity = Amenity(name="Pool", description="A luxurious swimming pool")
db.session.add(amenity)
db.session.commit()


place.amenities.append(amenity)
db.session.commit()


print(place.reviews)
print(place.amenities)
print(user.places)  
