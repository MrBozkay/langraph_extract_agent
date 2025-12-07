.PHONY: help install format clean build publish ci

help:
	@echo "Available commands:"
	@echo "  install    Install package in development mode"
	@echo "  format     Format code"
	@echo "  clean      Clean build artifacts"
	@echo "  build      Build package"
	@echo "  publish    Publish to PyPI"
	@echo "  ci         Run full CI pipeline locally"

install:
	pip install -e ".[dev]"

format:
	ruff format src tests

clean:
	rm -rf build/ dist/ *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

publish: build
	python -m twine upload dist/*

ci: install format
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term
	ruff check src tests
	mypy src