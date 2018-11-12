FROM labhackercd/alpine-python3-nodejs

ENV BUILD_PACKAGES postgresql-dev postgresql-client gettext

RUN apk add --update --no-cache $BUILD_PACKAGES
RUN mkdir -p /var/labhacker/wiki-legis

ADD . /var/labhacker/wiki-legis
WORKDIR /var/labhacker/wiki-legis

RUN pip install 'pipenv==8.1.2' psycopg2 gunicorn && \
    pipenv install --system && \
    rm -r /root/.cache

RUN npm install

RUN python3 src/manage.py compress --force && \
    python3 src/manage.py collectstatic --no-input && \
    python3 src/manage.py compilemessages

EXPOSE 8000
CMD ["python3", "src/manage.py", "runserver", "0.0.0.0:8000"]
