import unittest
import json
from app import create_app

class TestReviews(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
    def test_create_review(self):
        response = self.client.post('/api/v1/reviews/', json={"user_id": 1, "place_id": 1, "rating": 5, "comment": "Great place!"})
        self.assertEqual(response.status_code, 201)

    def test_get_reviews(self):
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)

    def test_get_review(self):
        response = self.client.get('/api/v1/reviews/1')
        self.assertEqual(response.status_code, 200)

    def test_update_review(self):
        response = self.client.put('/api/v1/reviews/1', json={"comment": "Updated comment!"})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
