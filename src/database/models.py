from flask_bcrypt import generate_password_hash, check_password_hash
from pytz import utc

from database.db import db
from helpers import now


class User(db.Document):
    first_name = db.StringField(required=True)
    last_name = db.StringField(required=True)
    password = db.StringField(required=True)
    email = db.EmailField(required=True, unique=True)

    def save(self, *args, **kwargs):
        self.password = self.create_hashed_password(self.password)
        return super().save(*args, **kwargs)

    @staticmethod
    def create_hashed_password(password):
        return generate_password_hash(password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Comment(db.Document):
    content = db.StringField(required=True)
    created_at = db.DateTimeField(default=now())
    created_by = db.ReferenceField('User')
    card = db.ReferenceField('Card')


class Card(db.Document):
    STATUS_CHOICES = (
        ('todo', 'Todo'),
        ('in_progress', 'In progress'),
        ('in_review', 'In review'),
        ('done', 'Done'),
    )

    title = db.StringField(required=True, unique_with='board')
    content = db.StringField(required=True)
    created_at = db.DateTimeField(default=now())
    created_by = db.ReferenceField('User')
    completed_at = db.DateTimeField(required=False)
    planned_start_time = db.DateTimeField(required=False)
    planned_end_time = db.DateTimeField(required=False)
    status = db.StringField(choices=STATUS_CHOICES, default='todo')
    comments = db.ListField(db.ReferenceField('Comment'))
    board = db.ReferenceField('Board')

    def save(self, *args, **kwargs):
        instance = super(Card, self).save(*args, **kwargs)

        if self.planned_start_time and self.planned_start_time.replace(tzinfo=utc) > now():
            from app import schedule_card_start_time
            schedule_card_start_time.apply_async(kwargs={'card_id': str(self.id)}, eta=self.planned_start_time)

        if self.planned_end_time and self.planned_end_time.replace(tzinfo=utc) > now():
            from app import schedule_card_end_time
            schedule_card_end_time.apply_async(kwargs={'card_id': str(self.id)}, eta=self.planned_end_time)

        if self.completed_at:
            self.completed_at = now()
            instance.save()

        return instance


class Board(db.Document):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('archived', 'Archived'),
    )
    name = db.StringField(required=True, unique=True)
    status = db.StringField(choices=STATUS_CHOICES, default='active')
    created_at = db.DateTimeField(default=now())
    created_by = db.ReferenceField('User')
    cards = db.ListField(db.ReferenceField('Card'))
