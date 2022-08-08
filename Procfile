release: python manage.py migrate
web: gunicorn blog.wsgi
worker: celery -A storefront worker --loglevel=info