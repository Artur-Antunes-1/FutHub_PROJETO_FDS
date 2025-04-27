#!/bin/bash

echo "== Applying migrations =="
python manage.py migrate --noinput

echo "== Collecting static files =="
python manage.py collectstatic --noinput

echo "== Starting Gunicorn =="
exec gunicorn project.wsgi --log-file -
