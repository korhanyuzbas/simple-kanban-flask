## Objects

#### User object

```
{
    "id": "<User ObjectId>",
    "email": "string",
    "first_name": "string",
    "last_name": "string"
}
```

#### Board object
```
{
    "created_at": "1970-01-01T00:00:00.000000+00:00", 
    "id": "<Board ObjectId>",
    "created_by": "<User ObjectId>",
    "name": "string",
    "status": "active|archived",
    "cards": [<Card object|list>],
}
```

#### Card object
```
{
    "id": <Card ObjectId>",
    "created_at": "1970-01-01T00:00:00.000000+00:00",
    "board": "<Board ObjectId>",
    "title": "string",
    "content": "string",
    "planned_start_time": "1970-01-01T00:00:00.000000+00:00", 
    "planned_end_time": "1970-01-01T00:00:00.000000+00:00",
    "completed_at": "1970-01-01T00:00:00.000000+00:00",
    "status": "todo|in_progress|in_review|done",
    "comments": [<Comment object|list>]
}
```

#### Comment object
```
{
    "id": <Comment ObjectId>",
    "created_at": "1970-01-01T00:00:00.000000+00:00",
    "created_by": "<User ObjectId>",
    "content": "string",
    "card": "<Card ObjectId>"
}
```
