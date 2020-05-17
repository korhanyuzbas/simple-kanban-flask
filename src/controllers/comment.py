from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine import DoesNotExist

from controllers.errors import UnauthorizedError
from database.models import Card, Comment
from database.schemas import comments_schema


class CommentsApi(Resource):
    def get(self, pk):
        comments = Comment.objects.filter(card=pk)
        return comments_schema.dump(comments).data, 200

    @jwt_required
    def post(self, pk):
        user_id = get_jwt_identity()
        card = Card.objects.get(id=pk)
        comment = Comment.objects.create(**request.get_json(), card=card, created_by=user_id)
        card.comments.append(comment)
        card.save()

        return comments_schema.dump(comment, many=False).data, 201


class CommentApi(Resource):
    @jwt_required
    def delete(self, pk):
        user_id = get_jwt_identity()
        try:
            comment = Comment.objects.get(id=pk)
        except DoesNotExist:
            raise DoesNotExist

        can_delete = False

        # Owner of comment can delete
        if str(comment.created_by.id) == user_id:
            can_delete = True
        # Owner of board can delete
        if str(comment.card.board.created_by.id) == user_id:
            can_delete = True

        if not can_delete:
            raise UnauthorizedError

        comment.delete()

        return {}, 204
