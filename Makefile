install:
		poetry install --no-root

dev:
	  poetry run fastapi dev src/main.py

lint:
		poetry run flake8 .

test: lint
	  poetry run python src/tests.py


.PHONY: install dev lint test
