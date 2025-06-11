#!/bin/sh

python manage.py migrate

python manage.py collectstatic --no-input

exec gunicorn api_server.configs.wsgi:application --bind 0.0.0.0:8000