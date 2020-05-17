from marshmallow_mongoengine import ModelSchema

from database.models import Board, Card, Comment, User


class UserSchema(ModelSchema):
    class Meta:
        exclude = ('password',)
        model = User


class BoardSchema(ModelSchema):
    class Meta:
        model = Board


class CardSchema(ModelSchema):
    class Meta:
        fields = (
            'id', 'content', 'title', 'board', 'created_at', 'planned_start_time', 'planned_end_time', 'completed_at',
            'status'
        )
        model = Card


class CommentSchema(ModelSchema):
    class Meta:
        model = Comment


user_schema = UserSchema(many=True)
boards_schema = BoardSchema(many=True)
cards_schema = CardSchema(many=True)
comments_schema = CommentSchema(many=True)
