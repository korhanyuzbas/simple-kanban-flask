from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine import DoesNotExist

from controllers.errors import UnauthorizedError
from database.models import Board
from database.schemas import cards_schema, boards_schema


class BoardApi(Resource):
    def get(self, pk):
        board = Board.objects.get(id=pk)
        board_s = boards_schema.dump(board, many=False)
        cards_s = cards_schema.dump(board.cards)
        board_s.data.update(cards=cards_s.data)
        return board_s.data, 201

    @jwt_required
    def delete(self, pk):
        user_id = get_jwt_identity()
        try:
            board = Board.objects.get(id=pk)
        except DoesNotExist:
            raise DoesNotExist

        if str(board.created_by.id) != user_id:
            raise UnauthorizedError

        board.delete()

        return {}, 204


class BoardsApi(Resource):
    def get(self):
        dump_data = boards_schema.dump(Board.objects, many=True)
        return dump_data.data, 200

    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        body = request.get_json()
        board = Board(**body, created_by=user_id)
        board.save()

        return boards_schema.dump(board, many=False).data, 201
