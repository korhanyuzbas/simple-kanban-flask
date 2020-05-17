from datetime import datetime

from pytz import utc


def now():
    return datetime.utcnow().replace(tzinfo=utc)


def send_mail(msg):
    return msg
