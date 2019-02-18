FROM python:3.6-alpine3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN apk add --update --no-cache build-base nginx && \
    pip install -r requirements.txt && \
    apk del build-base --purge
COPY ./docker-entrypoint.sh /code/docker-entrypoint.sh
COPY . /code/
ENTRYPOINT ["/code/docker-entrypoint.sh"]
