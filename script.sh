#! /bin/sh

python3 manage.py migrate
python manage.py collectstatic --no-input
waitress-server --listen=*:8000 config. wsgi:application