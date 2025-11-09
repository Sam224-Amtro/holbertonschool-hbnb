from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from config import Config

# Import des différents modules (endpoints)
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.ameneties import api as amenities_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.admin import api as admin_ns
from app.extensions import bcrypt
from app.extensions import jwt
from app.extensions import db

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)   # Création de l’application Flask

    # Clé secrète pour le JWT (à ne jamais mettre en clair en prod)
    app.config['JWT_SECRET_KEY'] = 'votre_cle_secrete_jwt'

    # Chargement de la configuration (mode dev, prod, etc.)
    app.config.from_object(config_class)
    app.config.from_object(Config)

    # 🔧 Initialisation des extensions
    bcrypt.init_app(app)  # pour hacher les mots de passe
    jwt.init_app(app)     # pour gérer les tokens JWT
    db.init_app(app)      # pour la base de données

    # Configuration Swagger pour l’authentification avec token
    authorizations = {
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Utilisez "Bearer <token>" pour vous authentifier.'
        }
    }

    # Création de l’API principale avec Flask-RESTx
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        authorizations=authorizations,
        security='Bearer Auth'  # active la protection JWT sur Swagger
    )

    # Enregistrement des routes des différents modules
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(admin_ns, path='/api/v1/admin')

    return app
