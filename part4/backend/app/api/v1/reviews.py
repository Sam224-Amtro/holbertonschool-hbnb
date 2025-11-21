from flask_restx import Namespace, Resource, fields, abort
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging
from flask import request

# Configuration du logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

api = Namespace('places', description='Place operations')

# Modèles
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
    try:
        return {
            "id": str(place_obj.id),
            "title": place_obj.title,
            "description": place_obj.description,
            "price": place_obj.price,
            "latitude": place_obj.latitude,
            "longitude": place_obj.longitude,
            "owner_id": str(place_obj.owner.id),
            "amenities": [a.name for a in place_obj.amenities]
        }
    except Exception as e:
        logger.error(f"Error formatting place: {str(e)}")
        raise


@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """ Register a new place """
        place_data = api.payload
        place_obj = facade.create_place(place_data)
        return format_place(place_obj), 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """ Retrieve all places """
        places = facade.get_all_places()
        return [format_place(p) for p in places], 200


@api.route('/<string:place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        try:
            place = facade.get_place(place_id)
            return format_place(place), 200
        except ValueError as e:
            return {'error': str(e)}, 404
        except Exception as e:
            return {'error': str(e)}, 500

    @jwt_required()
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    def put(self, place_id):
        """Update a place's information"""
        try:
            place_data = request.get_json()
            updated_place = facade.update_place(place_id, place_data)
            return format_place(updated_place), 200
        except ValueError as e:
            return {'error': str(e)}, 404
        except Exception as e:
            return {'error': str(e)}, 500

    @jwt_required()
    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    def delete(self, place_id):
        """Delete a place"""
        try:
            facade.delete_place(place_id)
            return {'message': 'Place deleted successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 404
        except Exception as e:
            return {'error': str(e)}, 500
