#!/bin/bash

echo "-----> Running django-compressor"
python src/manage.py collectstatic --noinput
python src/manage.py collectstatic_js_reverse
python src/manage.py compress --force

echo "-----> Running migrations"
python src/manage.py migrate

echo "-----> Processing translations"
python src/manage.py compilemessages