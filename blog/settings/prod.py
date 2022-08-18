from .common import *
from decouple import config
import dj_database_url


DEBUG = False


ALLOWED_HOSTS = ['diplom-blog-prod.herokuapp']


SECRET_KEY = config('SECRET_KEY')


DATABASES = {
    'default': dj_database_url.config()
}

EMAIL_HOST = config('MAILGUN_SMTP_SERVER')
EMAIL_HOST_USER = config('MAILGUN_SMTP_LOGIN')
EMAIL_HOST_PASSWORD = config('MAILGUN_SMTP_PASSWORD')
EMAIL_PORT = config('MAILGUN_SMTP_PORT')


CELERY_BROKER_URL = config('REDIS_URL')
