from .common import *
from decouple import config


DEBUG = True


SECRET_KEY = config('SECRET_KEY')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mysql',
        'HOST': '127.0.0.1',
        'USER': 'root',
        'PASSWORD': 'root',
        'PORT': '3306',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 2525


CELERY_BROKER_URL = 'redis://0.0.0.0:6379'


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True
}

MIDDLEWARE += ['silk.middleware.SilkyMiddleware']
