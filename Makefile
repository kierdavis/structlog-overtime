# Path containing source code of the Python package:
PACKAGE_PATH := structlog_overtime
# All paths containing Python code:
PYTHON_PATHS := $(PACKAGE_PATH) stubs tests setup.py

all: typecheck test format lint

typecheck:
	mypy $(PACKAGE_PATH)

test:
	pytest --junit-xml=pytest_report.xml --cov=$(PACKAGE_PATH)

format: isort black

isort:
	isort $(PYTHON_PATHS)

black:
	black --config=black.toml $(PYTHON_PATHS)

lint:
	flake8 $(PYTHON_PATHS)
