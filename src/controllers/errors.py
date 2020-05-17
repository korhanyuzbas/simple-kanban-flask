class SchemaValidationError(Exception):
    pass


class EmailAlreadyExist(Exception):
    pass


class UnauthorizedError(Exception):
    pass


class EmailDoesNotExist(Exception):
    pass


class BadTokenError(Exception):
    pass


class PasswordsDoNotMatch(Exception):
    pass


class InvalidPassword(Exception):
    pass


errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
    "DoesNotExist": {
        "message": "Object not found",
        "status": 400
    },
    "SchemaValidationError": {
        "message": "Request is missing required fields",
        "status": 400
    },
    "EmailAlreadyExist": {
        "message": "User with given email already exists",
        "status": 400
    },
    "UnauthorizedError": {
        "message": "Invalid email or password",
        "status": 401
    },
    "EmailDoesNotExist": {
        "message": "Couldn't find the user with given email address",
        "status": 400
    },
    "BadTokenError": {
        "message": "Invalid token",
        "status": 403
    },
    "ExpiredSignatureError": {
        "message": "Expired token",
        "status": 403
    },
    "PasswordsDoNotMatch": {
        "message": "Passwords do not match",
        "status": 400
    },
    "InvalidPassword": {
        "message": "Invalid password",
        "status": 400
    },
    "NoAuthorizationError": {
        "message": "Permission denied",
        "status": 403
    },
    "NotUniqueError": {
        "message": "Duplicate key",
        "status": 400
    },

}