SHELL := /bin/bash
EXECUTABLE := $(shell poetry env info --path)

.PHONY: serve clean

serve:
	bentoml serve chatbot/service.py

clean:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
