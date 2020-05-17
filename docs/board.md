## Board

### Create board

`Authentication token is required in this endpoint`

Description: Creates new board

Endpoint `POST /board`

Payload:

```
{
    "name": "string"
}
```

Response: Board object, 201

### List Boards

Description: Return list of boards

Endpoint `GET /board`

Response: Board object|list, 200

### Get Board

Description: Return board

Endpoint `GET /board/<ObjectId>`

Response: Board object, 200

### Delete Board

`Authentication token is required in this endpoint`

Description: Delete board (By board owner) 

Endpoint `DELETE /board/<ObjectId>`

Response: 204