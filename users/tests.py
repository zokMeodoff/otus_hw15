from django.test import TestCase, Client
from django.contrib.auth.models import User
import json

client = Client()


class TestUser:

    @staticmethod
    def create_test_user(username='TestUser',
                         email='testuser@email.com',
                         first_name='Test',
                         last_name='User',
                         password='12345'):

        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save()
        return user


class RegisterTestCase(TestCase):

    def test_register_view_get(self):
        response_from_url = client.get('/users/')
        self.assertEqual(405, response_from_url.status_code)

    def test_register_success(self):
        request = {
            'username': 'NewTestUser',
            'password': 123456,
            'email': 'newtestuser@email.com',
            'first_name': 'Newtest',
            'last_name': 'User'
        }

        request_json = json.dumps(request)
        response_from_url = client.post('/users/', data=request_json, content_type='application/json')

        user = User.objects.first()

        self.assertEqual(201, response_from_url.status_code)
        self.assertEqual(user.username, request['username'])
        self.assertEqual(user.email, request['email'])
        self.assertEqual(user.first_name, request['first_name'])
        self.assertEqual(user.last_name, request['last_name'])
        self.assertEqual(user.is_staff, False)

    def test_register_fail_without_password(self):
        request = {
            'username': 'NewTestUser',
            'email': 'newtestuser@email.com'
        }

        request_json = json.dumps(request)
        response_from_url = client.post('/users/', data=request_json, content_type='application/json')

        self.assertEqual(400, response_from_url.status_code)

    def test_register_fail_without_username(self):
        request = {
            'password': 123456,
            'email': 'newtestuser@email.com'
        }

        request_json = json.dumps(request)
        response_from_url = client.post('/users/', data=request_json, content_type='application/json')

        self.assertEqual(400, response_from_url.status_code)


class LoginTestCase(TestCase):
    def setUp(self):
        TestUser.create_test_user()

    def test_login_success(self):
        request = {
            'username': 'TestUser',
            'password': 12345
        }

        user = User.objects.get(username='TestUser')

        request_json = json.dumps(request)
        response_from_url = client.post('/users/login/', data=request_json, content_type='application/json')

        self.assertEqual(200, response_from_url.status_code)
        self.assertTrue(user.is_authenticated)

    def test_login_wrong_password(self):
            request = {
                'username': 'TestUser',
                'password': 1234
            }

            request_json = json.dumps(request)
            response_from_url = client.post('/users/login/', data=request_json, content_type='application/json')

            self.assertEqual(400, response_from_url.status_code)

    def test_login_wrong_username(self):
        request = {
            'username': 'Test',
            'password': 12345
        }

        request_json = json.dumps(request)
        response_from_url = client.post('/users/login/', data=request_json, content_type='application/json')

        self.assertEqual(400, response_from_url.status_code)

    def test_login_without_password(self):
        request = {
            'username': 'TestUser'
        }

        request_json = json.dumps(request)
        response_from_url = client.post('/users/login/', data=request_json, content_type='application/json')

        self.assertEqual(400, response_from_url.status_code)

    def test_login_without_username(self):
        request = {
            'password': 12345
        }

        request_json = json.dumps(request)
        response_from_url = client.post('/users/login/', data=request_json, content_type='application/json')

        self.assertEqual(400, response_from_url.status_code)

