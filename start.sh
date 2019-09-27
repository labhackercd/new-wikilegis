#!/bin/bash

while true; do
    PG_STATUS=`PGPASSWORD=$DATABASE_PASSWORD psql -U $DATABASE_USER  -w -h $DATABASE_HOST -c '\l \q' | grep postgres | wc -l`
    if ! [ "$PG_STATUS" -eq "0" ]; then
       break
    fi
    echo "Waiting Database Setup"
    sleep 10
done

PGPASSWORD=$DATABASE_PASSWORD psql -U $DATABASE_USER -w -h $DATABASE_HOST -c "CREATE DATABASE ${DATABASE_NAME} OWNER ${DATABASE_USER}"

python3 src/manage.py migrate
python3 src/create_admin.py
python3 src/manage.py compress --force
python3 src/manage.py collectstatic --no-input
python3 src/manage.py collectstatic_js_reverse
python3 src/manage.py compilemessages

NAME="wikilegis"
[[ -z "${WORKERS}" ]] && NUM_WORKERS=2 || NUM_WORKERS="${WORKERS}"
DJANGO_WSGI_MODULE=wikilegis.wsgi

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn --chdir src ${DJANGO_WSGI_MODULE}:application --name $NAME --workers $NUM_WORKERS --bind=0.0.0.0:8000