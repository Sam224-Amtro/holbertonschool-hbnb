from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Amenity model
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'description': fields.String(required=False, description='Description of the amenity')
})

# Endpoint to manage the list of amenities


@api.route('/')
class AmenityList(Resource):
    @api.response(200, 'List of amenities retrieved successfully')
    @api.response(404, 'No amenities found')
    def get(self):
        """Retrieve a list of all amenities"""
        try:
            amenities = facade.get_all_amenities()
            if not amenities:
                return {'error': 'No amenities found'}, 404
            return [{'id': amenity.id, 'name': amenity.name, 'description': amenity.description} for amenity in amenities], 200
        except Exception as e:
            return {'error': f"An unexpected error occurred: {str(e)}"}, 500

    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new amenity"""
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


# Endpoint to manage individual amenities by ID
@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @api.response(404, 'Amenity not found')
    @api.response(200, 'Amenity details retrieved successfully')
    def get(self, amenity_id):
        """Retrieve amenity details by ID"""
        try:
            amenity = facade.get_amenity(amenity_id)

            if not amenity:
                return {'error': 'Amenity not found'}, 404

            return {
                'id': amenity.id,
                'name': amenity.name,
                'description': amenity.description
            }, 200

        except ValueError:
            # Invalid ID format
            return {'error': 'Invalid amenity ID format'}, 400
        except Exception as e:
            return {'error': f"An unexpected error occurred: {str(e)}"}, 500

    @api.expect(amenity_model)
    @api.response(200, 'User details updated successfully')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update user by ID"""
        amenities_data = request.get_json()
        return facade.update_amenity(amenity_id, amenities_data)
