## Card

### Create card

`Authentication token is required in this endpoint`

Description: Creates new card. 

    If planned_start_time and/or planned_end_time is given, also creates scheduled task to send email to user

Endpoint `POST /board/<Board ObjectId>/card`

Payload:

```
{
    "title": "string",
    "content": "string",
    "planned_start_time": "datetime string|format:31/12/1970 00:00",
    "planned_end_time": "datetime string|format:31/12/1970 00:00",
    "completed_at": "datetime string|format:31/12/1970 00:00",
    "status": "todo|in_progress|in_review|done"
}
```

Response: Card object, 201

### List Board's Cards

Description: Return list of cards of board

Endpoint `GET /board/<Board ObjectId>/card`

Response: Card object|list, 200

### Get Card

Description: Return card

Endpoint `GET /card/<ObjectId>`

Response: Card object, 200

### Update Card

Description: Updates given fields of card

Endpoint `PATCH /card/<ObjectId>`

Example Payload:

```
{
    "title": "string"
}
```

Response: Card object, 200

### Delete Card

`Authentication token is required in this endpoint`

Description: Delete card (By board owner) 

Endpoint `DELETE /card/<ObjectId>`

Response: 204