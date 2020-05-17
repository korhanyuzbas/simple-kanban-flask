### Simple Kanban System with Flask

#
### How to run
- Install Docker and Docker Compose
- Create new environment variable named `KANBAN_ENV_FILE` and give full path of .env file (you can check `.env.example`)
- Docker containers can be created with `docker-compose up -d` 

### TODOs
 See [TODO](https://github.com/korhanyuzbas/simple-kanban-flask/blob/master/docs/todo.md)
### Test

Run tests while in src folder with following command: `export KANBAN_ENV_FILE=../.env && python -m unittest discover`

### Documentation

#### User

- [Signup](https://github.com/korhanyuzbas/simple-kanban-flask/blob/master/docs/user.md#signup)
- [Login](https://github.com/korhanyuzbas/simple-kanban-flask/blob/master/docs/user.md#login)
- [Profile](https://github.com/korhanyuzbas/simple-kanban-flask/blob/master/docs/user.md#profile)
- [Change Password](https://github.com/korhanyuzbas/simple-kanban-flask/blob/master/docs/user.md#change-password)

#### Board

- [Create board](https://github.com/korhanyuzbas/simple-kanban-flask/blob/master/docs/board.md#create-board)
- [List boards](https://github.com/korhanyuzbas/simple-kanban-flask/blob/master/docs/board.md#list-boards)
- [Get board](https://github.com/korhanyuzbas/simple-kanban-flask/blob/master/docs/board.md#get-board)
- [Delete board](https://github.com/korhanyuzbas/simple-kanban-flask/blob/master/docs/board.md#delete-board)

#### Card

- [Create card](https://github.com/korhanyuzbas/simple-kanban-flask/blob/master/docs/card.md#create-card)
- [List board's cards](https://github.com/korhanyuzbas/simple-kanban-flask/blob/master/docs/card.md#list-boards-cards)
- [Get card](https://github.com/korhanyuzbas/simple-kanban-flask/blob/master/docs/card.md#get-card)
- [Update card](https://github.com/korhanyuzbas/simple-kanban-flask/blob/master/docs/card.md#update-card)
- [Delete card](https://github.com/korhanyuzbas/simple-kanban-flask/blob/master/docs/card.md#delete-card)

#### Comment

- [Create comment](https://github.com/korhanyuzbas/simple-kanban-flask/blob/master/docs/comment.md#create-comment)
- [List card's comments](https://github.com/korhanyuzbas/simple-kanban-flask/blob/master/docs/comment.md#list-cards-comments)
- [Delete comment](https://github.com/korhanyuzbas/simple-kanban-flask/blob/master/docs/comment.md#delete-comment)

#### Error Responses
Check `src/controllers/errors.py` for more detail