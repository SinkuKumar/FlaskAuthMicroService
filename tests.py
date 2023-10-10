import unittest
import json
from app import app, db, User


class AuthAPITestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_auth.db'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def register_user(self, username, password):
        return self.app.post('/register', json={'username': username, 'password': password})

    def login_user(self, username, password):
        return self.app.post('/login', json={'username': username, 'password': password})

    def test_register_user(self):
        response = self.register_user('testuser', 'testpassword')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['message'], 'User registered successfully!')

    def test_register_existing_user(self):
        self.register_user('testuser', 'testpassword')
        response = self.register_user('testuser', 'testpassword')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'User already exists!')

    def test_login_valid_user(self):
        self.register_user('testuser', 'testpassword')
        response = self.login_user('testuser', 'testpassword')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue('access_token' in data)

    def test_login_invalid_user(self):
        response = self.login_user('nonexistentuser', 'password')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message'], 'Invalid credentials')

    def test_protected_route_with_token(self):
        self.register_user('testuser', 'testpassword')
        login_response = self.login_user('testuser', 'testpassword')
        access_token = json.loads(login_response.data.decode())['access_token']

        response = self.app.get('/protected', headers={'Authorization': f'Bearer {access_token}'})
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['logged_in_as'], 'testuser')

    def test_protected_route_without_token(self):
        response = self.app.get('/protected')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['msg'], 'Missing Authorization Header')


if __name__ == '__main__':
    unittest.main()
