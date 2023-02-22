full-test:
	poetry run pytest --show-capture=stdout --showlocals -vv
light-test:
	poetry run pytest --no-summary --disable-pytest-warnings
lint:
	poetry run flake8 page_analyzer tests
check: light-test lint
push: check
	git push


install:
	poetry install
build:
	poetry build
publish:
	poetry publish --dry-run
package-install:
	python3 -m pip install --user dist/*.whl --force
test-coverage:
	poetry run pytest --cov=page_analyzer --cov-report xml


# DEV

dev:
	poetry run flask --app page_analyzer:app --debug run


#  PROD
PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
