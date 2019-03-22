FROM labhackercd/alpine-python3-nodejs

ENV BUILD_PACKAGES postgresql-dev postgresql-client gettext

RUN apk add --update --no-cache $BUILD_PACKAGES
RUN mkdir -p /var/labhacker/new-wikilegis

ADD . /var/labhacker/new-wikilegis
WORKDIR /var/labhacker/new-wikilegis

RUN pip3 install -U pipenv psycopg2 gunicorn

RUN pipenv install --system

RUN npm install && \
    python3 src/manage.py build_mkdocs && \
    python3 src/manage.py collectstatic --no-input && \
    python3 src/manage.py compilemessages

EXPOSE 8000
CMD ["python3", "src/manage.py", "runserver", "0.0.0.0:8000"]
