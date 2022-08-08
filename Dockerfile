FROM python:3.8.5-alpine

ENV PYTHONBUFFERED=1
WORKDIR /django_app

RUN apk update && apk add \
    gcc\
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev cargo \
    cargo \
    postgresql-dev \
    jpeg-dev \
    zlib-dev \
    gettext

RUN python -m pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /django_app/

RUN sleep 5
RUN python manage.py makemigrations && python manage.py migrate
CMD python manage.py runserver 0.0.0.0:8000

EXPOSE 8000