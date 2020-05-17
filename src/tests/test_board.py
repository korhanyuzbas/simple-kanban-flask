import json

from bson import ObjectId
from mongoengine import NotUniqueError, DoesNotExist

from controllers.errors import UnauthorizedError
from database.models import Board
from tests import BaseTestCase


class TestBoard(BaseTestCase):
    def test_create_board(self):
        user, token = self.login_and_generate_jwt_token()

        payload = json.dumps({
            "name": "Test",
        })
        response = self.app.post('/board', headers=self.auth_header(token), data=payload)

        self.assertEqual(response.status_code, 201)
        board = Board.objects.get(id=response.json.get('id'))
        self.assertEqual(board.created_by, user)

    def test_create_board_failures(self):
        # Post with empty body
        _, token = self.login_and_generate_jwt_token()
        response = self.app.post('/board', headers=self.auth_header(token), data=dict())
        self.assertEqual(response.status_code, 400)

        # Try unique field
        self.create_dummy_board(name="Unique")
        with self.assertRaises(NotUniqueError):
            self.app.post('/board', headers=self.auth_header(token), data=json.dumps(
                {
                    "name": "Unique",
                }
            ))

    def test_get_board_list(self):
        _, token = self.login_and_generate_jwt_token()

        self.create_dummy_board()
        self.create_dummy_board()
        self.create_dummy_board()

        response = self.app.get('/board', headers=self.auth_header(token))

        self.assertEqual(len(response.json), 3)
        self.assertEqual(response.status_code, 200)

    def test_get_board_retrieve(self):
        board = self.create_dummy_board()
        response = self.app.get('/board/{}'.format(board.id))
        self.assertEqual(len(response.json.get('cards')), 0)
        self.assertEqual(response.json.get('name'), board.name)

        self.create_dummy_card(board=board)
        self.create_dummy_card(board=board)
        response = self.app.get('/board/{}'.format(board.id))
        self.assertEqual(len(response.json.get('cards')), 2)
        self.assertEqual(response.json.get('name'), board.name)

    def test_delete_board(self):
        user, token = self.login_and_generate_jwt_token()
        user2, token2 = self.login_and_generate_jwt_token()
        board = self.create_dummy_board(created_by=user)

        with self.assertRaises(UnauthorizedError):
            self.app.delete('/board/{}'.format(board.id), headers=self.auth_header(token2))

        response = self.app.delete('/board/{}'.format(board.id), headers=self.auth_header(token))
        self.assertEqual(response.status_code, 204)

        # DoesNotExist
        with self.assertRaises(DoesNotExist):
            self.app.delete('/board/{}'.format(str(ObjectId())), headers=self.auth_header(token))
