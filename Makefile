SHELL := /bin/bash
EXECUTABLE := poetry run
APPLICATION_NAME ?= chatbot

.PHONY: serve clean install test build prune

serve:
	$(SHELL) scripts/run_app_service.sh

clean: clean-pyc clean-build clean-test

clean-pyc:
	$(EXECUTABLE) find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

clean-build:
	$(EXECUTABLE) rm -fr build/ dist/ .eggs/
	$(EXECUTABLE) find . -name '*.egg-info' -o -name '*.egg' -exec rm -fr {} +

clean-test:
	$(EXECUTABLE) rm -fr .tox/ .coverage coverage.* htmlcov/ .pytest_cache

install: clean
	$(EXECUTABLE) poetry install --sync
	$(EXECUTABLE) poetry lock

test:
	$(EXECUTABLE) pytest

build:
	docker build --tag $(APPLICATION_NAME) .

prune:
	docker image prune -f
