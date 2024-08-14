PORT ?= 8000

install:
	poetry install

lint:
	poetry run flake8

test:
	poetry run pytest -vv tests

check: test lint

run:
	poetry run flask --app example --debug run --host 0.0.0.0 --port $(PORT)

prod:
	poetry run gunicorn --workers=4 --bind 0.0.0.0:$(PORT) example:app --log-file -

compose:
	docker compose up

compose-setup: compose-build
	docker compose run app make install

compose-build:
	docker compose build

compose-down:
	docker compose down -v

compose-dev:
	docker compose run app make run

compose-bash:
	docker compose run app bash
