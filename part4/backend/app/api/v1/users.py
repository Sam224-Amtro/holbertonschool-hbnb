from uuid import UUID
from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models.user import User

api = Namespace('users', description='User operations')

# Mettre à jour le modèle pour inclure le champ password
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')  # Ajout du champ password
})


@api.route('/')
class UserList(Resource):
    @api.response(200, 'List of users retrieved successfully')
    @api.response(404, 'No users found')
    def get(self):
        """Retrieve a list of all users"""
        try:
            users = facade.get_all_users()
            if not users:
                return {'error': 'No users found'}, 404
            return [{'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email} for user in users], 200
        except Exception as e:
            return {'error': f"An unexpected error occurred: {str(e)}"}, 500

    @api.expect(user_model)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new user"""
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


@api.route('/<string:user_id>')
class UserResource(Resource):
    @api.response(404, 'User not found')
    @api.response(200, 'User details retrieved successfully')
    def get(self, user_id):
        """Retrieve user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @api.expect(user_model)
    @api.response(200, 'User details updated successfully')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update user by ID"""
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
