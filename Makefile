SHELL := /bin/bash

init:
	source .venv/bin/activate
	pip install -r requirements.txt

dev:init
	fastapi dev main.py

test:
	py.test tests

.PHONY: init test