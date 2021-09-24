#!/bin/sh

cd /usr/src/app

# prepare init migration
python manage.py makemigrations portal_api
echo "Created migrations"
# migrate db, so we have the latest db schema
python manage.py migrate
echo "Migrated DB to latest version"
# start development server on public ip interface, on port 8080
# python manage.py runserver 0.0.0.0:8080
# start server on port 888
gunicorn --chdir api --bind :8888 --workers 1 --timeout 360 api.wsgi:application