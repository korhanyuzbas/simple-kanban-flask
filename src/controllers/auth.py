import datetime

from flask import Response, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import NotUniqueError, DoesNotExist

from controllers.errors import SchemaValidationError, EmailAlreadyExist, UnauthorizedError, \
    PasswordsDoNotMatch, InvalidPassword
from database.models import User
from database.schemas import user_schema


class SignupApi(Resource):
    def post(self):
        body = request.get_json()
        user = User(**body)
        try:
            user.save()
        except NotUniqueError:
            raise EmailAlreadyExist

        return user_schema.dump(user, many=False).data, 201


class LoginApi(Resource):
    def post(self):
        body = request.get_json()
        try:
            user = User.objects.get(email=body.get('email'))
        except DoesNotExist:
            raise UnauthorizedError

        authorized = user.check_password(body.get('password'))
        if not authorized:
            raise UnauthorizedError

        access_token = create_access_token(identity=str(user.id), expires_delta=datetime.timedelta(days=1))
        return {'token': access_token}, 200


class UserApi(Resource):
    def get(self, pk):
        try:
            user = User.objects.exclude('password').get(id=pk)
        except DoesNotExist:
            raise DoesNotExist

        return user_schema.dump(user, many=False).data, 200


class ChangePassword(Resource):
    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        body = request.get_json()
        old_password = body.get('old_password')
        new_password = body.get('new_password')
        new_password_repeat = body.get('new_password_repeat')

        if not old_password or not new_password or not new_password_repeat:
            raise SchemaValidationError

        if new_password != new_password_repeat:
            raise PasswordsDoNotMatch

        user = User.objects.get(id=user_id)
        if not user.check_password(old_password):
            raise InvalidPassword

        user.modify(password=new_password)
        user.save()
        return user_schema.dump(user, many=False).data, 200
