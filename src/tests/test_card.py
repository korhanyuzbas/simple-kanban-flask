import json
from datetime import timedelta, datetime
from unittest.mock import patch

from bson import ObjectId
from mongoengine import NotUniqueError, FieldDoesNotExist, ValidationError, DoesNotExist

from controllers.errors import UnauthorizedError
from database.models import Card
from helpers import now
from tests import BaseTestCase


class TestCard(BaseTestCase):
    @patch('app.schedule_card_start_time', return_value='Start Email Sent')
    @patch('app.schedule_card_end_time', return_value='End Email Sent')
    def test_create_card(self, email_end_celery_task, email_start_celery_task):
        user, token = self.login_and_generate_jwt_token()
        board = self.create_dummy_board(created_by=user)

        response = self.app.post('/board/{}/card'.format(board.id),
                                 headers=self.auth_header(token),
                                 data=json.dumps({
                                     "title": "Test",
                                     "content": "Test"
                                 }))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json.get('title'), "Test")
        self.assertEqual(response.json.get('board'), str(board.id))

        # Create card with planned start and end time
        start_time = now() + timedelta(days=1)
        end_time = now() + timedelta(days=7)
        response = self.app.post('/board/{}/card'.format(board.id),
                                 headers=self.auth_header(token),
                                 data=json.dumps({
                                     "title": self.get_random_string(),
                                     "content": self.get_random_string(),
                                     "planned_start_time": start_time.strftime("%d/%m/%Y %H:%M"),
                                     "planned_end_time": end_time.strftime("%d/%m/%Y %H:%M"),
                                 }))
        card = Card.objects.get(id=response.json.get('id'))
        self.assertEqual(start_time.strftime("%d/%m/%Y %H:%M"), card.planned_start_time.strftime("%d/%m/%Y %H:%M"))
        self.assertEqual(end_time.strftime("%d/%m/%Y %H:%M"), card.planned_end_time.strftime("%d/%m/%Y %H:%M"))

        email_start_celery_task.apply_async.assert_called_once_with(
            kwargs={'card_id': str(card.id)},
            eta=datetime.strptime(start_time.strftime("%d/%m/%Y %H:%M"), "%d/%m/%Y %H:%M")
        )
        email_end_celery_task.apply_async.assert_called_once_with(
            kwargs={'card_id': str(card.id)},
            eta=datetime.strptime(end_time.strftime("%d/%m/%Y %H:%M"), "%d/%m/%Y %H:%M")
        )

    def test_patch_card(self):
        user, token = self.login_and_generate_jwt_token()
        board = self.create_dummy_board(created_by=user)

        card = self.create_dummy_card(board=board, title="Test")
        self.app.patch('/card/{}'.format(card.id),
                       headers=self.auth_header(token),
                       data=json.dumps({
                           "title": "New Title",
                       }))

        get_card_instance = Card.objects.get(id=card.id)
        self.assertEqual("New Title", get_card_instance.title)

    def test_create_card_failures(self):
        user, token = self.login_and_generate_jwt_token()
        board = self.create_dummy_board(created_by=user)

        # Not unique
        self.create_dummy_card(board=board, title="Test")
        with self.assertRaises(NotUniqueError):
            self.app.post('/board/{}/card'.format(board.id),
                          headers=self.auth_header(token),
                          data=json.dumps({
                              "title": "Test",
                              "content": "Test"
                          }))

        # Invalid payload parameters
        with self.assertRaises(FieldDoesNotExist):
            self.app.post('/board/{}/card'.format(board.id),
                          headers=self.auth_header(token),
                          data=json.dumps({
                              "name": "Test",
                              "content": "Test"
                          }))

        # Missing payload parameters
        with self.assertRaises(ValidationError):
            self.app.post('/board/{}/card'.format(board.id),
                          headers=self.auth_header(token),
                          data=json.dumps({
                              "title": "Test",
                          }))

        # Not owner of board
        with self.assertRaises(UnauthorizedError):
            board = self.create_dummy_board()
            self.app.post('/board/{}/card'.format(board.id),
                          headers=self.auth_header(token),
                          data=json.dumps({
                              "title": "Test",
                          }))

    def test_get_board_cards(self):
        board = self.create_dummy_board()

        self.create_dummy_card(board=board)
        self.create_dummy_card(board=board)
        self.create_dummy_card(board=board)

        response = self.app.get('/board/{}/card'.format(board.id))
        self.assertEqual(len(response.json), 3)

    def test_retrieve_card(self):
        user, token = self.login_and_generate_jwt_token()
        board = self.create_dummy_board(created_by=user)

        card = self.create_dummy_card(board=board)

        response = self.app.get('/card/{}'.format(card.id))
        self.assertEqual(response.json.get('title'), card.title)
        self.assertEqual(response.status_code, 200)

        with self.assertRaises(DoesNotExist):
            self.app.get('/card/{}'.format(str(ObjectId())))

    def test_delete_card(self):
        user, token = self.login_and_generate_jwt_token()
        user2, token2 = self.login_and_generate_jwt_token()
        board = self.create_dummy_board(created_by=user)
        card = self.create_dummy_card(board=board)

        with self.assertRaises(UnauthorizedError):
            self.app.delete('/card/{}'.format(card.id), headers=self.auth_header(token2))

        response = self.app.delete('/card/{}'.format(card.id), headers=self.auth_header(token))
        self.assertEqual(response.status_code, 204)

        with self.assertRaises(DoesNotExist):
            self.app.delete('/card/{}'.format(str(ObjectId())), headers=self.auth_header(token))
