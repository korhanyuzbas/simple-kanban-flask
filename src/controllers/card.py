import datetime

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine import DoesNotExist

from controllers.errors import UnauthorizedError
from database.models import Board, Card
from database.schemas import cards_schema, CardSchema


class CardsApi(Resource):
    def get(self, pk):
        cards = Card.objects.filter(board=pk)
        return cards_schema.dump(cards).data, 200

    @jwt_required
    def post(self, pk):
        user_id = get_jwt_identity()
        try:
            board = Board.objects.get(id=pk)
        except DoesNotExist:
            raise DoesNotExist

        if str(board.created_by.id) != user_id:
            raise UnauthorizedError

        body = request.get_json()

        if body.get('planned_start_time'):
            body.update(planned_start_time=datetime.datetime.strptime(body.get('planned_start_time'), "%d/%m/%Y %H:%M"))

        if body.get('planned_end_time'):
            body.update(planned_end_time=datetime.datetime.strptime(body.get('planned_end_time'), "%d/%m/%Y %H:%M"))

        if body.get('completed_at'):
            body.update(completed_at=datetime.datetime.strptime(body.get('completed_at'), "%d/%m/%Y %H:%M"))

        card = Card(**body, board=board)
        card.save()
        board.cards.append(card)
        board.save()

        return cards_schema.dump(card, many=False).data, 201


class CardApi(Resource):
    def get(self, pk):
        try:
            card = Card.objects.get(id=pk)
        except DoesNotExist:
            raise DoesNotExist
        return cards_schema.dump(card, many=False).data, 200

    @jwt_required
    def patch(self, pk):
        user_id = get_jwt_identity()
        try:
            card = Card.objects.get(id=pk)
        except DoesNotExist:
            raise DoesNotExist

        if str(card.board.created_by.id) != user_id:
            raise UnauthorizedError

        updated_instance = CardSchema().update(card, request.get_json()).data
        updated_instance.save()
        return cards_schema.dump(updated_instance, many=False).data, 200

    @jwt_required
    def delete(self, pk):
        user_id = get_jwt_identity()
        try:
            card = Card.objects.get(id=pk)
        except DoesNotExist:
            raise DoesNotExist

        if str(card.board.created_by.id) != user_id:
            raise UnauthorizedError

        card.delete()

        return {}, 204
