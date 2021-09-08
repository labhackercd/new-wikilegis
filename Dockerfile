FROM labhackercd/alpine-python3-nodejs

ENV BUILD_PACKAGES postgresql-dev postgresql-client gettext freetype-dev libpng-dev openblas-dev

RUN apk add --update --no-cache $BUILD_PACKAGES
RUN mkdir -p /var/labhacker/new-wikilegis

ADD . /var/labhacker/new-wikilegis
WORKDIR /var/labhacker/new-wikilegis

RUN pip3 install --upgrade pip
RUN pip3 install -U pipenv psycopg2 gunicorn

RUN pipenv install --system

RUN npm install && \
    npm rebuild node-sass --force

RUN chmod 755 start.sh

EXPOSE 8000
CMD ["python3", "src/manage.py", "runserver", "0.0.0.0:8000"]
