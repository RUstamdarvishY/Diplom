FROM python:3.8.5-alpine
WORKDIR /Diplom/
RUN apk update && apk add \
    python3-dev \
  

RUN python -m pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD python manage.py runserver 0.0.0.0:8000
