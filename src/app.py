import os
import sys

from flask import Flask
from celery import Celery
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restful import Api
from mongoengine import DoesNotExist
from pytz import utc

from controllers.errors import errors
from database.db import initialize_db
from helpers import now, send_mail
from routes.base import initialize_routes


def create_app(**kwargs):
    app = Flask(__name__)
    app.config.from_pyfile(os.environ.get('KANBAN_ENV_FILE', '../.env'))
    app.config.update(**kwargs)
    return app


def initialize_apps(app):
    api = Api(app=app, errors=errors)
    Bcrypt(app=app)
    JWTManager(app=app)

    initialize_db(app=app)
    initialize_routes(api=api)
    api.init_app(app)


app = create_app()
celery = Celery(app.name, broker=app.config.get("CELERY_BROKER_URL"), backend=app.config.get("CELERY_RESULT_BACKEND"))
celery.conf.update(app.config)
celery.autodiscover_tasks(['app'])

if 'flask' in sys.argv[0]:
    initialize_apps(app)


@celery.task
def schedule_card_start_time(card_id):
    from database.models import Card
    try:
        card = Card.objects.get(id=card_id)
    except DoesNotExist:
        return

    if not card.planned_start_time:
        return

    if now() > card.planned_start_time.replace(tzinfo=utc):
        send_mail("Please start card")


@celery.task
def schedule_card_end_time(card_id):
    from database.models import Card
    try:
        card = Card.objects.get(id=card_id)
    except DoesNotExist:
        return

    if not card.planned_end_time:
        return

    if now() > card.planned_end_time.replace(tzinfo=utc):
        send_mail("Please end card")


if __name__ == '__main__':
    app.run()
