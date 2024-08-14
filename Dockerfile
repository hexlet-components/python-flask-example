FROM python:3.12-slim

RUN apt-get update && apt-get install make -yqq \
    make \
    postgresql-15 \
    sudo

RUN pip install poetry

ENV POETRY_VIRTUALENVS_IN_PROJECT=true

COPY ./pg_hba.conf /etc/postgresql/15/main/pg_hba.conf

WORKDIR /app

COPY . .

RUN poetry install

#USER postgres

#COPY ./run.sh .
#CMD ./run.sh
