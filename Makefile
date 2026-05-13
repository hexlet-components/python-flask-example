PORT ?= 8000

install:
	uv sync

lint:
	uv run ruff check .
	uv run ruff format --check .

test:
	uv run pytest -vv tests

check: test lint

run:
	uv run flask --app example --debug run --host 0.0.0.0 --port $(PORT)

prod:
	uv run gunicorn --workers=4 --bind 0.0.0.0:$(PORT) example:app --log-file -

compose-production-run:
	docker compose -p python_page_analyzer_ru-production down
	docker compose -p python_page_analyzer_ru-production build
	docker compose -p python_page_analyzer_ru-production up
