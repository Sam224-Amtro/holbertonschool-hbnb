from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask import current_app
from app.services import facade

api = Namespace('auth', description='Authentication operations')

# Modèle pour la validation des entrées
login_model = api.model('Login', {
    'email': fields.String(required=True, description='Email de l\'utilisateur'),
    'password': fields.String(required=True, description='Mot de passe de l\'utilisateur'),
    'admin_code': fields.String(required=False, description='Code secret pour obtenir le rôle administrateur')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authentifie l'utilisateur et retourne un token JWT"""
        credentials = api.payload

        user = facade.get_user_by_email(credentials['email'])

        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Identifiants invalides'}, 401

        is_admin = False
        if 'admin_code' in credentials and credentials['admin_code'] == current_app.config['ADMIN_SECRET_CODE']:
            is_admin = True

        additional_claims = {"is_admin": is_admin}
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims=additional_claims
        )
        return {'access_token': access_token}, 200

@api.route('/protected')
class UserInfo(Resource):
    @api.doc(security='Bearer Auth')
    @jwt_required()
    def get(self):
        """Récupère les informations de l'utilisateur connecté"""
        current_user_id = get_jwt_identity()  # Récupère l'ID de l'utilisateur (sujet du token)
        claims = get_jwt()  # Récupère les claims personnalisés

        # Vérifie si l'utilisateur est un administrateur (si nécessaire)
        is_admin = claims.get('is_admin', False)

        return {
            'message': f'Bonjour, utilisateur {current_user_id}',
            'is_admin': is_admin
        }, 200
