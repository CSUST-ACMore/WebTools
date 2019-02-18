FROM python:3.6-alpine3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
COPY ./docker-entrypoint.sh /code/docker-entrypoint.sh
COPY . /code/
ENTRYPOINT ["/code/docker-entrypoint.sh"]
