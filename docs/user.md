## Users

### Signup

Description: Creates a new user

Endpoint `POST /user/register/`

Payload:

```
{
    "email": "string",
    "password": "string",
    "first_name": "string",
    "last_name": "string"
}
```

Response: User object, 201

### Login

Description: Authenticates user

Endpoint `POST /user/login/`

Payload:

```
{
    "email": "string",
    "password": "string"
}
```

Response: `{"token": <JWT|string>}`, 200

### Profile

Description: Returns the information about user

Endpoint `GET /user/<ObjectId>/profile`

Response: User object, 200

### Change password

`Authentication token is required in this endpoint`

Description: Changes the password of authenticated user

Endpoint `POST /user/change_password/`

Payload

```
{
    "old_password": "string",
    "new_password": "string",
    "new_password_repeat": "string",
}
```

Response: User object, 200
