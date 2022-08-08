from .common import *
from decouple import config
import dj_database_url


DEBUG = False


ALLOWED_HOSTS = ['diplom-blog-prod.herokuapp']


SECRET_KEY = config('SECRET_KEY')


DATABASES = {
    'default': dj_database_url.config()
}

EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = config('EMAIL_PORT')


CELERY_BROKER_URL = config('REDIS_URL')
