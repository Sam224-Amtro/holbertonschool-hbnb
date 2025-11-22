from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        review_data = request.get_json()

        # Validation des données
        if not all(key in review_data for key in ['text', 'rating', 'user_id', 'place_id']):
            return {'error': 'Missing required fields'}, 400

        if not isinstance(review_data['rating'], int) or review_data['rating'] < 1 or review_data['rating'] > 5:
            return {'error': 'Rating must be an integer between 1 and 5'}, 400

        # Création de l'avis via la façade
        review = facade.create_review(review_data)
        if not review:
            return {'error': 'Failed to create review'}, 500

        return review.to_dict(), 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews], 200

@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        review_data = request.get_json()

        if 'rating' in review_data and (not isinstance(review_data['rating'], int) or review_data['rating'] < 1 or review_data['rating'] > 5):
            return {'error': 'Rating must be an integer between 1 and 5'}, 400

        updated_review = facade.update_review(review_id, review_data)
        if not updated_review:
            return {'error': 'Review not found'}, 404

        return updated_review.to_dict(), 200

@api.route('/places/<string:place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        if not reviews:
            return {'error': 'No reviews found for this place'}, 404
        return [review.to_dict() for review in reviews], 200
