FROM python:3.11-alpine

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev


RUN pip install --upgrade pip

COPY ./mqtt_site/requirements.txt .
RUN pip install -r requirements.txt
