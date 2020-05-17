import json

from bson import ObjectId
from mongoengine import NotUniqueError, FieldDoesNotExist, ValidationError, DoesNotExist

from controllers.errors import UnauthorizedError
from tests import BaseTestCase


class TestComment(BaseTestCase):
    def test_create_comment(self):
        user, token = self.login_and_generate_jwt_token()
        card = self.create_dummy_card()

        response = self.app.post('/card/{}/comment'.format(card.id),
                                 headers=self.auth_header(token),
                                 data=json.dumps({
                                     "content": "Test"
                                 }))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json.get('content'), "Test")
        self.assertEqual(response.json.get('card'), str(card.id))

    def test_create_comment_failures(self):
        user, token = self.login_and_generate_jwt_token()
        card = self.create_dummy_card(board=self.create_dummy_board(created_by=user))

        # Invalid payload parameters
        with self.assertRaises(FieldDoesNotExist):
            self.app.post('/card/{}/comment'.format(card.id),
                          headers=self.auth_header(token),
                          data=json.dumps({
                              "name": "Test",
                          }))

        # Missing payload parameters
        with self.assertRaises(ValidationError):
            self.app.post('/card/{}/comment'.format(card.id),
                          headers=self.auth_header(token),
                          data=json.dumps({}))

    def test_get_card_comments(self):
        card = self.create_dummy_card()

        self.create_dummy_comment(card=card)
        self.create_dummy_comment(card=card)
        self.create_dummy_comment(card=card)

        response = self.app.get('/card/{}/comment'.format(card.id))
        self.assertEqual(len(response.json), 3)

    def test_delete_comment(self):
        user, token = self.login_and_generate_jwt_token()
        user2, token2 = self.login_and_generate_jwt_token()
        user3, token3 = self.login_and_generate_jwt_token()

        board = self.create_dummy_board(created_by=user)
        card = self.create_dummy_card(board=board)
        comment = self.create_dummy_comment(card=card)
        comment1_user2 = self.create_dummy_comment(card=card, created_by=user2)
        comment2_user2 = self.create_dummy_comment(card=card, created_by=user2)

        # DoesNotExist
        with self.assertRaises(DoesNotExist):
            self.app.delete('/comment/{}'.format(str(ObjectId())), headers=self.auth_header(token3))

        # Random user can't delete comment
        with self.assertRaises(UnauthorizedError):
            self.app.delete('/comment/{}'.format(comment.id), headers=self.auth_header(token3))

        # Board owner deletes own comment
        response = self.app.delete('/comment/{}'.format(comment.id), headers=self.auth_header(token))
        self.assertEqual(response.status_code, 204)

        # Comment owner can delete own comment
        response = self.app.delete('/comment/{}'.format(comment1_user2.id), headers=self.auth_header(token2))
        self.assertEqual(response.status_code, 204)

        # Board owner can delete any comment
        response = self.app.delete('/comment/{}'.format(comment2_user2.id), headers=self.auth_header(token))
        self.assertEqual(response.status_code, 204)
