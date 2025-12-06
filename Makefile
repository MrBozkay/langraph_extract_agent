.PHONY: help install test lint format clean build publish

help:
	@echo "Available commands:"
	@echo "  install    Install package in development mode"
	@echo "  test       Run tests"
	@echo "  lint       Run linting"
	@echo "  format     Format code"
	@echo "  clean      Clean build artifacts"
	@echo "  build      Build package"
	@echo "  publish    Publish to PyPI"

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term

lint:
	flake8 src tests
	mypy src

format:
	black src tests
	isort src tests

clean:
	rm -rf build/ dist/ *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

publish: build
	python -m twine upload dist/*