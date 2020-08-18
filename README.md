# Python Craigslist Notifications

A simple, self-hosted, python daemon to scan craigslist and notify you of new listings via IFTTT

Main components used

- `python-craigslist` library
- `IFTTT` Maker Webhooks
- `TinyDB` for remembering which listings have been seen already

## Getting up and running

This app uses `pipenv` to manage dependencies. Install it and run `pipenv install` to get up and running

### IFTTT Config

Go to [IFTTT Maker Webhooks](https://ifttt.com/maker_webhooks) and configure a webhook URL.
Choose "Send Rich Notifications". Use `{{Value1}}` as the title parameter and `{{Value2}}` as the URL.

Note the URL you need to send to for triggering.

### Config.json file

Due to the number of options this script has for searching, a json file is used to configure the search arguments.

Take a look at `config.example.json` as an example of what the file should looks like. The easiest thing to do is copy
it as `config.json` and set your own search values.

### Running

    pipenv run python python_craigslist_notifications/main.py config.json

## Docker

You can also run this as a docker container. Use the normal `docker build .` and `docker run` to launch it.
Note the `dockerfile` assumes you have made a `config.json` in this directory