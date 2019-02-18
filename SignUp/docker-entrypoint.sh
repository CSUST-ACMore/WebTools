#!/bin/sh

python3 manage.py makemigrations

python3 manage.py migrate

python manage.py collectstatic --no-input

exec "$@"
