FROM python:3.12-slim

RUN apt-get update && apt-get install make -yq

RUN pip install poetry

WORKDIR /app

COPY poetry.lock .

RUN poetry install

COPY . .

CMD ["bash", "-c", "make prod"]
