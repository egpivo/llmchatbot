SHELL := /bin/bash
EXECUTABLE := poetry run

.PHONY: serve clean install clean-pyc clean-build clean-test

serve:
	$(EXECUTABLE) bentoml serve chatbot/app/app.py

clean: clean-pyc clean-build clean-test
clean-pyc:
	$(EXECUTABLE) find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
clean-build:
	$(EXECUTABLE) rm -fr build/ dist/ .eggs/
	$(EXECUTABLE) find . -name '*.egg-info' -o -name '*.egg' -exec rm -fr {} +
clean-test:
	$(EXECUTABLE) rm -fr .tox/ .coverage coverage.* htmlcov/ .pytest_cache

install: clean ## install the package to the active Python's site-packages
	$(EXECUTABLE) poetry install
	$(EXECUTABLE) poetry lock
