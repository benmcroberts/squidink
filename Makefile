.PHONY: help install-dev install-examples test lint fmt build clean

PY := .venv/bin/python
PIP := .venv/bin/pip

help:
	@echo "make install-dev   - install the package (editable) + dev deps into .venv"
	@echo "make install-examples - install the package + examples deps (jupyter, dotenv)"
	@echo "make test          - run pytest"
	@echo "make lint          - run ruff check + ruff format --check"
	@echo "make fmt           - run ruff format + ruff check --fix"
	@echo "make build         - build sdist + wheel into dist/"
	@echo "make clean         - remove build artifacts and caches"

install-dev:
	$(PIP) install --upgrade pip
	$(PIP) install -e .
	$(PIP) install --group dev

install-examples:
	$(PIP) install -e .
	$(PIP) install --group examples

test:
	$(PY) -m pytest

lint:
	$(PY) -m ruff check .
	$(PY) -m ruff format --check .

fmt:
	$(PY) -m ruff format .
	$(PY) -m ruff check --fix .

build:
	$(PY) -m build

clean:
	rm -rf build dist *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name .ruff_cache -exec rm -rf {} +
