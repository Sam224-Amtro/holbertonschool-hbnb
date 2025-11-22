import unittest
import json
from app import create_app

class TestUsers(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user(self):
        response = self.client.post('/api/v1/users/', json={"name": "John Doe", "email": "john@example.com"})
        self.assertEqual(response.status_code, 201)

    def test_get_users(self):
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)

    def test_get_user(self):
        response = self.client.get('/api/v1/users/1')
        self.assertEqual(response.status_code, 200)

    def test_update_user(self):
        response = self.client.put('/api/v1/users/1', json={"name": "Jane Doe"})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
