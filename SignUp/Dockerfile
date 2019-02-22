FROM python:3.6-alpine3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps
ADD requirements.txt /code/
RUN pip install -r requirements.txt
COPY ./docker-entrypoint.sh /code/docker-entrypoint.sh
COPY . /code/
ENTRYPOINT ["/code/docker-entrypoint.sh"]
