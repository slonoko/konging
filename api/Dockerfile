ARG APP_IMAGE=python:3.8.1-alpine

FROM $APP_IMAGE AS base

FROM base as builder

ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt
EXPOSE 8080

CMD ["python", "-m", "main"]