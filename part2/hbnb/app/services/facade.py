from uuid import UUID
from datetime import datetime
import uuid
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
from app.persistence.repository import InMemoryRepository
from flask import jsonify, request


class HBnBFacade:
    def __init__(self):
        # Dépôts en mémoire pour chaque entité
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # --- Opérations sur les utilisateurs --- #
    def create_user(self, user_data):
        """Créer un nouvel utilisateur"""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute("email", email)

    def update_user(self, user_id, user_data):
        """Met à jour les informations de l'utilisateur"""
        user = self.user_repo.get(user_id)
        if not user:
            return None

        if 'first_name' in user_data:
            user.first_name = user_data['first_name']
        if 'last_name' in user_data:
            user.last_name = user_data['last_name']
        if 'email' in user_data:
            user.email = user_data['email']

        self.user_repo.update(user)
        return user
    def get_all_users(self):
        """Récupère tous les utilisateurs"""
        return self.user_repo.get_all()

    # --- Opérations sur les amenities --- #
    def create_amenity(self, amenity_data):
        """Créer une nouvelle amenity"""
        try:
            amenity = Amenity(**amenity_data)  # Utiliser la classe Amenity
            self.amenity_repo.add(amenity)  # Ajouter l'amenity au dépôt
            return amenity
        except Exception as e:
            return {'error': f"An error occurred while creating the amenity: {str(e)}"}, 500

    def get_all_amenities(self):
        """Retourne toutes les amenities"""
        try:
            return self.amenity_repo.get_all()
        except Exception as e:
            return {'error': f"An error occurred while fetching amenities: {str(e)}"}, 500

    def get_amenity(self, amenity_id):
        """Retourne une amenity par ID"""
        try:
            return self.amenity_repo.get(amenity_id)
        except Exception as e:
            return {'error': f"An error occurred while fetching the amenity: {str(e)}"}, 500

    def get_amenity_by_name(self, name):
        """Retourne une amenity par nom"""
        try:
            return self.amenity_repo.get_by_attribute('name', name)
        except Exception as e:
            return {'error': f"An error occurred while fetching amenity by name: {str(e)}"}, 500

    def update_amenity(self, amenity_id, amenity_data):
        """Met à jour une amenity par ID"""
        try:
            if not amenity_data:
                return {'error': 'No data provided'}, 400

            amenity = self.get_amenity(amenity_id)
            if not amenity:
                return {'error': 'Amenity not found'}, 404

            # Mise à jour des données de l'amenity
            for key, value in amenity_data.items():
                setattr(amenity, key, value)

            # Retourner l'amenity mis à jour sous forme de dictionnaire
            return amenity.to_dict()

        except Exception as e:
            return {'error': f"An error occurred while updating the amenity: {str(e)}"}, 500

    # --- Opérations sur les lieux --- #
    def create_place(self, place_data):
        if place_data["price"] < 0:
            raise ValueError("Price must be a non-negative value.")
        if not (-90 <= place_data["latitude"] <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        if not (-180 <= place_data["longitude"] <= 180):
            raise ValueError("Longitude must be between -180 and 180.")

        owner = self.user_repo.get(place_data["owner_id"])
        if not owner:
            raise ValueError("Owner not found.")

        place_obj = Place(
            title=place_data["title"],
            description=place_data.get("description", ""),
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner=owner
        )
        place_obj.amenities = [] if not hasattr(place_obj, "amenities") else place_obj.amenities

        if "amenities" in place_data:
            amenities = []
            for amenity_id in place_data["amenities"]:
                amenity_obj = self.amenity_repo.get(amenity_id)
                if amenity_obj:
                    amenities.append(amenity_obj)
            place_obj.amenities = amenities

        self.place_repo.add(place_obj)
        return place_obj

    def get_place(self, place_id):
        try:
            # Vérifier si l'UUID est valide
            uuid_obj = uuid.UUID(place_id, version=4)
        except ValueError:
            raise ValueError(f"❌ UUID invalide : {place_id}")


        place = self.place_repo.get(place_id)

        if not place:
            raise ValueError(f"❌ Place not found for UUID: {place_id}")

        print(f"✅ Lieu trouvé : {place}")  # Affichage pour debug

        return place

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        # Validation si de nouveaux attributs sont fournis
        if 'price' in place_data:
            if place_data['price'] < 0:
                raise ValueError("Le prix doit être positif ou nul.")
        if 'latitude' in place_data:
            if not (-90 <= place_data['latitude'] <= 90):
                raise ValueError("La latitude doit être comprise entre -90 et 90.")
        if 'longitude' in place_data:
            if not (-180 <= place_data['longitude'] <= 180):
                raise ValueError("La longitude doit être comprise entre -180 et 180.")
        # Si l'identifiant du propriétaire est mis à jour, vérifiez-le et remplacez-le par l'objet owner
        if 'owner_id' in place_data:
            owner = self.user_repo.get(place_data['owner_id'])
            if not owner:
                raise ValueError("Propriétaire non trouvé.")
            place_data['owner'] = owner
            del place_data['owner_id']
        place.update(place_data)
        return place




    # --- Opérations sur les reviews --- #
    def is_valid_uuid(self, uuid_to_test):
        """Check if a string is a valid UUID."""
        try:
            UUID(uuid_to_test)
            return True
        except ValueError:
            return False

    def create_review(self, review_data):
        """Create a new review with validation"""
        # Validation des champs obligatoires
        if not all(key in review_data for key in ['text', 'rating', 'user_id', 'place_id']):
            return {'error': 'Missing required fields'}, 400

        # Validation du texte
        if not review_data['text'].strip():
            return {'error': 'Review text cannot be empty'}, 400

        # Validation de la note
        if not isinstance(review_data['rating'], int) or review_data['rating'] < 1 or review_data['rating'] > 5:
            return {'error': 'Rating must be an integer between 1 and 5'}, 400

        # Validation des UUID
        if not self.is_valid_uuid(review_data['user_id']) or not self.is_valid_uuid(review_data['place_id']):
            return {'error': 'Invalid user_id or place_id'}, 400

        # Création de l'avis
        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            user_id=review_data['user_id'],
            place_id=review_data['place_id']
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Retrieve a review by ID"""
        # Validation de l'ID
        if not self.is_valid_uuid(review_id):
            return {'error': 'Invalid review ID'}, 400

        review = self.review_repo.get(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review

    def update_review(self, review_id, review_data):
        """Update a review by ID"""
        # Validation de l'ID
        if not self.is_valid_uuid(review_id):
            return {'error': 'Invalid review ID'}, 400

        review = self.review_repo.get(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        # Validation des données de mise à jour
        if 'text' in review_data and not review_data['text'].strip():
            return {'error': 'Review text cannot be empty'}, 400

        if 'rating' in review_data and (not isinstance(review_data['rating'], int) or review_data['rating'] < 1 or review_data['rating'] > 5):
            return {'error': 'Rating must be an integer between 1 and 5'}, 400

        # Mise à jour des champs
        for key, value in review_data.items():
            if hasattr(review, key):
                setattr(review, key, value)
        review.updated_at = datetime.utcnow()
        self.review_repo.update(review)
        return review

    def get_reviews_by_place(self, place_id):
        """Retrieve all reviews for a specific place"""
        # Validation de l'ID du lieu
        if not self.is_valid_uuid(place_id):
            return {'error': 'Invalid place ID'}, 400

        reviews = [review for review in self.review_repo.get_all() if review.place_id == place_id]
        if not reviews:
            return {'error': 'No reviews found for this place'}, 404
        return reviews
