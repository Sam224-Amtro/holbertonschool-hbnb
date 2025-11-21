import unittest
import json
from app import create_app

class TestPlaces(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_place(self):
        response = self.client.post('/api/v1/places/', json={"name": "Beach House", "location": "Miami"})
        self.assertEqual(response.status_code, 201)

    def test_get_places(self):
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)

    def test_get_place(self):
        response = self.client.get('/api/v1/places/1')
        self.assertEqual(response.status_code, 200)

    def test_update_place(self):
        response = self.client.put('/api/v1/places/1', json={"name": "Mountain Cabin"})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
