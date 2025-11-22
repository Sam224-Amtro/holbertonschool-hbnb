import unittest
import json
from app import create_app

class TestAmenities(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_amenity(self):
        response = self.client.post('/api/v1/amenities/', json={"name": "WiFi"})
        self.assertEqual(response.status_code, 201)

    def test_get_amenities(self):
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)

    def test_get_amenity(self):
        response = self.client.get('/api/v1/amenities/1')
        self.assertEqual(response.status_code, 200)

    def test_update_amenity(self):
        response = self.client.put('/api/v1/amenities/1', json={"name": "Swimming Pool"})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
