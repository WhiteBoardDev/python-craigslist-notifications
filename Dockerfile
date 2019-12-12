FROM python:3.7-buster
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
# Assuming you have placed the config file as config.json
COPY config.json ./
COPY python_craigslist_notifications python_craigslist_notifications
COPY pyproject.toml ./
RUN $HOME/.poetry/bin/poetry install

ENTRYPOINT $HOME/.poetry/bin/poetry run python python_craigslist_notifications/main.py config.json