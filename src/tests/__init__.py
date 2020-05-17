import json
import random
import string
from unittest import TestCase

from bson import ObjectId

from app import create_app, initialize_apps
from database.db import db
from database.models import User, Board, Card, Comment


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        app = create_app(
            MONGODB_SETTINGS={"DB": "iqvizyon-testing"},
            CELERY_ALWAYS_EAGER=True
        )
        app.testing = True

        self.app = app.test_client()

        initialize_apps(app)

        self.db = db.get_db()

    def tearDown(self) -> None:
        for collection in self.db.list_collection_names():
            self.db.drop_collection(collection)

    @staticmethod
    def get_random_string(length=8):
        return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(length)])

    def get_random_email(self):
        return self.get_random_string() + '@example.com'

    @staticmethod
    def get_random_bson_id():
        return ObjectId()

    def create_dummy_user(self, **kwargs):
        email = kwargs.get('email', self.get_random_email())
        password = kwargs.get('password', self.get_random_string())
        first_name = kwargs.get('first_name', self.get_random_string())
        last_name = kwargs.get('last_name', self.get_random_string())

        return User.objects.create(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

    def create_dummy_board(self, **kwargs):
        name = kwargs.get('name', self.get_random_string())
        user = kwargs.get('created_by', self.create_dummy_user())

        instance = Board(
            name=name,
            created_by=user
        )
        instance.save()
        return instance

    def create_dummy_card(self, **kwargs):
        board = kwargs.get('board', self.create_dummy_board())
        title = kwargs.get('title', self.get_random_string())
        content = kwargs.get('content', self.get_random_string(50))

        instance = Card(
            board=board,
            title=title,
            content=content
        )
        instance.save()

        board.cards.append(instance)
        board.save()
        return instance

    def create_dummy_comment(self, **kwargs):
        card = kwargs.get('card', self.create_dummy_card())
        content = kwargs.get('content', self.get_random_string(20))
        user = kwargs.get('created_by', self.create_dummy_user())

        instance = Comment(
            card=card,
            created_by=user,
            content=content
        )
        instance.save()
        card.comments.append(instance)
        card.save()
        return instance

    # TODO: instead of this method, patching jwt related methods will perform faster
    def login_and_generate_jwt_token(self, **kwargs):
        user_password = kwargs.get('password', "123456")
        user = kwargs.get('user', self.create_dummy_user(password=user_password))
        login_response = self.app.post('/login', headers={"Content-Type": "application/json"},
                                       data=json.dumps({"email": user.email, "password": user_password}))

        return user, login_response.json.get('token')

    @staticmethod
    def auth_header(token):
        return {"Content-Type": "application/json", "Authorization": "Bearer {}".format(token)}
