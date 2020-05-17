import json

from mongoengine import DoesNotExist

from controllers.errors import UnauthorizedError, EmailAlreadyExist, PasswordsDoNotMatch, \
    InvalidPassword, SchemaValidationError
from database.models import User
from tests import BaseTestCase


class TestBaseUser(BaseTestCase):
    def test_retrieve_user(self):
        user = self.create_dummy_user()

        response = self.app.get('/user/{}/profile'.format(user.id))

        self.assertEqual(response.status_code, 200)

    def test_retrieve_user__notexist(self):
        with self.assertRaises(DoesNotExist):
            response = self.app.get('/user/{}/profile'.format(self.get_random_bson_id()))
            self.assertEqual(response.json.get('message'), 'Object not found')

    def test_user_change_password__success(self):
        current_password = "123456"
        user, token = self.login_and_generate_jwt_token(password=current_password)
        new_password = "654321"
        self.assertTrue(user.check_password(current_password))
        self.app.post('/user/change_password',
                      headers=self.auth_header(token),
                      data=json.dumps({"old_password": current_password, "new_password": new_password,
                                       "new_password_repeat": new_password})
                      )

        user = User.objects.get(id=str(user.id))
        self.assertTrue(user.check_password(new_password))

    def test_user_change_password__failure(self):
        current_password = "123456"
        user, token = self.login_and_generate_jwt_token(password=current_password)

        # New passwords not matching
        with self.assertRaises(PasswordsDoNotMatch):
            response = self.app.post(
                '/user/change_password',
                headers=self.auth_header(token),
                data=json.dumps({"old_password": current_password, "new_password": "123123",
                                 "new_password_repeat": "12312s3"}))

            self.assertEqual(response.json.get('message'), 'Passwords do not match')

        # Old password is wrong
        with self.assertRaises(InvalidPassword):
            response = self.app.post(
                '/user/change_password',
                headers=self.auth_header(token),
                data=json.dumps({"old_password": "asd", "new_password": "123123",
                                 "new_password_repeat": "123123"}))

            self.assertEqual(response.json.get('message'), 'Invalid password')

        # Missing fields
        with self.assertRaises(SchemaValidationError):
            response = self.app.post(
                '/user/change_password',
                headers=self.auth_header(token),
                data=json.dumps({"old_password": current_password,
                                 "new_password_repeat": "123123"}))

            self.assertEqual(response.json.get('message'), 'Request is missing required fields')

    def test_login__successful(self):
        email = self.get_random_email()
        password = self.get_random_string()
        self.create_dummy_user(email=email, password=password)

        response = self.app.post(
            '/login',
            headers={"Content-Type": "application/json"},
            data=json.dumps({"email": email, "password": password})
        )

        self.assertTrue(response.json["token"])

    def test_login__nonexist_email(self):
        with self.assertRaises(UnauthorizedError):
            response = self.app.post(
                '/login',
                headers={"Content-Type": "application/json"},
                data=json.dumps({"email": "wrongemail@example.com", "password": self.get_random_string()})
            )
            self.assertEqual(response.json.get("message"), 'Invalid email or password')

    def test_login__wrong_password(self):
        email = self.get_random_email()
        password = self.get_random_string()
        self.create_dummy_user(email=email, password=password)

        with self.assertRaises(UnauthorizedError):
            response = self.app.post(
                '/login',
                headers={"Content-Type": "application/json"},
                data=json.dumps({"email": email, "password": "wrongpassword"})
            )
            self.assertEqual(response.json.get("message"), 'Invalid email or password')

    def test_login__invalid_params(self):
        payload = json.dumps({"email": "1", "password": "1"})

        with self.assertRaises(UnauthorizedError):
            response = self.app.post('/login', headers={"Content-Type": "application/json"}, data=payload)
            self.assertEqual(response.json["message"], 'Invalid email or password')
            self.assertIsNone(response.json.get('token'))

    def test_register__successful(self):
        email = self.get_random_email()
        password = self.get_random_string()
        payload = json.dumps({
            "email": email,
            "password": password,
            "first_name": "John",
            "last_name": "Doe"
        })

        response = self.app.post('/register', headers={"Content-Type": "application/json"}, data=payload)

        user_id = response.json["id"]
        user = User.objects.get(id=user_id)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.email, email)
        self.assertEqual(response.status_code, 201)

    def test_register_duplicate_email(self):
        email = self.get_random_email()
        payload = json.dumps({
            "email": email,
            "password": self.get_random_string(),
            "first_name": self.get_random_string(),
            "last_name": self.get_random_string()
        })

        self.app.post('/register', headers={"Content-Type": "application/json"}, data=payload)

        with self.assertRaises(EmailAlreadyExist):
            response = self.app.post('/register', headers={"Content-Type": "application/json"}, data=payload)

            self.assertEqual('User with given email/email already exists', response.json['message'])
            self.assertEqual(400, response.status_code)
