from flask import Flask, render_template, send_from_directory
from flask_restx import Api
from flask_cors import CORS

from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.ameneties import api as amenities_ns   # ✔ correction ici
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.admin import api as admin_ns


from app.extensions import bcrypt, jwt, db
from config import DevelopmentConfig


def create_app(config_class=DevelopmentConfig):
    """Création et configuration de l'application Flask."""

    # Initialisation de Flask
    app = Flask(
        __name__,
        static_folder='../../frontend/static',
        template_folder='../../frontend/templates'
    )

    # Configuration générale
    app.config.from_object(config_class)

    # Clé secrète JWT
    app.config['JWT_SECRET_KEY'] = config_class.SECRET_KEY

    # Initialisation des extensions
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    # CORS (autoriser le frontend)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5500"}})

    # Swagger / Flask-RESTX configuration
    authorizations = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": 'Utilisez "Bearer <token>" pour vous authentifier.'
        }
    }

    api = Api(
        app,
        version="1.0",
        title="HBnB API",
        description="HBnB Application API",
        authorizations=authorizations,
        security="Bearer Auth"
    )

    # =========================
    # API Namespaces
    # =========================
    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(places_ns, path="/api/v1/places")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(reviews_ns, path="/api/v1/reviews")
    api.add_namespace(auth_ns, path="/api/v1/auth")
    api.add_namespace(admin_ns, path="/api/v1/admin")

    # =========================
    # Routes Frontend
    # =========================
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/login")
    def login():
        return render_template("login.html")

    @app.route("/add_review")
    def add_review():
        return render_template("add_review.html")

    @app.route("/place")
    def place():
        return render_template("place.html")

    # =========================
    # Fichiers statiques
    # =========================
    @app.route("/static/<path:filename>")
    def static_files(filename):
        return send_from_directory(app.static_folder, filename)

    return app
