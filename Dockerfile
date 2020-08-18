FROM python:3.8-buster

RUN mkdir /app
WORKDIR /app

RUN apt-get update
RUN apt-get install -y pipenv
# Assuming you have placed the config file as config.json
COPY config.json ./
COPY Pipfile.lock Pipfile.lock
COPY Pipfile Pipfile
COPY python_craigslist_notifications python_craigslist_notifications

RUN pipenv install  --deploy

ENTRYPOINT pipenv run python python_craigslist_notifications/main.py config.json