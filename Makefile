PORT ?= 8000

install:
	poetry install

lint:
	poetry run flake8

test:
	poetry run pytest -vv tests

check: test lint

run:
	poetry run flask --app example --debug run --port 8000

prod:
	poetry run gunicorn --workers=4 --bind 0.0.0.0:$(PORT) hello_world:app --log-file -
