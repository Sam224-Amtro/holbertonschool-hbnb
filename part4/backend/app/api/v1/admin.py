from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('admin', description='Endpoints réservés aux administrateurs')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')  # Ajout du champ password
})


amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})


def format_place(place_obj):
    """ Helper function to format place data """
    return {
        "id": place_obj.id,
        "title": place_obj.title,
        "description": place_obj.description,
        "price": place_obj.price,
        "latitude": place_obj.latitude,
        "longitude": place_obj.longitude,
        "owner_id": place_obj.owner.id,
        "amenities": [a.name for a in place_obj.amenities]
    }

@api.route('/')
class AdminResource(Resource):
    @api.doc(security='Bearer Auth')  # Indique que cet endpoint est protégé
    @jwt_required()  # Protège l'endpoint avec JWT
    def get(self):
        """Un endpoint réservé aux administrateurs"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        # Vérifie si l'utilisateur est un administrateur
        if not claims.get('is_admin'):
            return {'error': 'Accès refusé. Réservé aux administrateurs.'}, 403

        return {'message': f'Bienvenue, administrateur {current_user_id}'}, 200

@api.route('/users/<user_id>')
class AdminUserResource(Resource):
    @jwt_required()
    def put(self, user_id):
        current_user = get_jwt_identity()

        # If 'is_admin' is part of the identity payload
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        email = data.get('email')

        if email:
            # Check if email is already in use
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email is already in use'}, 400

        # Logic to update user details, including email and password
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200
        pass

@api.route('/users/')
class AdminUserCreate(Resource):
    @api.doc(security='Bearer Auth')
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new user"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        try:
            user_data = request.get_json()

            # Vérifier si l'email existe déjà
            existing_user = facade.get_user_by_email(user_data.get('email'))
            if existing_user:
                return {'error': 'Email already exists'}, 400

            # Hacher le mot de passe avant de créer l'utilisateur
            if 'password' in user_data:
                password = user_data.pop('password')  # Retirer le mot de passe des données utilisateur
                user_data['password'] = facade.hash_password(password)  # Hacher le mot de passe

            # Définir is_admin (par défaut à False si non fourni)
            is_admin = user_data.pop('is_admin', False)  # Retirer is_admin des données utilisateur
            user_data['is_admin'] = is_admin  # Ajouter is_admin aux données de l'utilisateur

            # Créer l'utilisateur
            user = facade.create_user(user_data)
            if not user:
                return {'error': 'User creation failed'}, 500

            # Retourner les détails de l'utilisateur sans le mot de passe
            if hasattr(user, 'to_dict'):
                return user.to_dict(), 201
            else:
                return {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'is_admin': user.is_admin  # Inclure le statut administrateur dans la réponse
                }, 201

        except Exception as e:
            return {'error': f"An error occurred while creating the user: {str(e)}"}, 500

@api.route('/users/<user_id>')
class AdminUserModify(Resource):
    @jwt_required()
    def put(self, user_id):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        email = data.get('email')

        # Ensure email uniqueness
        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        # Logic to update user details
        user_data = request.get_json()

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Hacher le mot de passe si fourni
        if 'password' in user_data:
            password = user_data.pop('password')  # Retirer le mot de passe des données utilisateur
            user_data['password'] = facade.hash_password(password)  # Hacher le mot de passe

        updated_user = facade.update_user(user_id, user_data)
        if not updated_user:
            return {'error': 'User update failed'}, 500

        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }, 200
        pass


@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        try:
            amenity_data = request.get_json()

            # Check if the amenity already exists by name
            existing_amenity = facade.get_amenity_by_name(
                amenity_data.get('name'))
            if existing_amenity:
                return {'error': 'Amenity already exists'}, 400

            amenity = facade.create_amenity(amenity_data)
            if not amenity:
                return {'error': 'Amenity creation failed'}, 500

            # Check if 'amenity' has the 'to_dict' method or return basic attributes
            if hasattr(amenity, 'to_dict'):
                return amenity.to_dict(), 201
            else:
                return {
                    'id': amenity.id,
                    'name': amenity.name,
                    'description': amenity.description
                }, 201

        except Exception as e:
            return {'error': f"An error occurred while creating the amenity: {str(e)}"}, 500

@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @jwt_required()
    def put(self, amenity_id):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        amenities_data = request.get_json()
        return facade.update_amenity(amenity_id, amenities_data)

@api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @jwt_required()
    def put(self, place_id):
        current_user = get_jwt_identity()

        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place = facade.get_place(place_id)
        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403
        if place.owner != current_user:
            return {'error': 'Unauthorized action'}, 403

        # Mettre à jour les attributs du lieu
        data = api.payload
        for key, value in data.items():
            setattr(place, key, value)

        # Mettre à jour le lieu dans le repository
        facade.update_place(place)
        return format_place(place), 200


        # Logic to update the place
        pass
