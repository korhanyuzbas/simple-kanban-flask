## Comment

### Create comment

`Authentication token is required in this endpoint`

Description: Creates new comment. 

Endpoint `POST /card/<Card ObjectId>/comment`

Payload:

```
{
    "content": "string"
}
```

Response: Comment object, 201

### List Card's Comments

Description: Return list of comments of card

Endpoint `GET /card/<Card ObjectId>/comment`

Response: Comment object|list, 200

### Delete Comment

`Authentication token is required in this endpoint`

Description: Delete comment (By comment owner and/or board owner) 

Endpoint `DELETE /card/<ObjectId>`

Response: 204