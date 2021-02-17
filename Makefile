# Path containing source code of the Python package:
PACKAGE_PATH := structlog_overtime
# All paths containing Python code to typecheck
TYPECHECKED_PYTHON_PATHS := $(PACKAGE_PATH) tests
# All paths containing Python code to format:
FORMATTED_PYTHON_PATHS := $(PACKAGE_PATH) tests setup.py
# All paths containing Python code to lint:
LINTED_PYTHON_PATHS := $(PACKAGE_PATH) tests setup.py

all: typecheck test format lint

typecheck:
	mypy $(TYPECHECKED_PYTHON_PATHS)

test:
	pytest --junit-xml=pytest_report.xml --cov=$(PACKAGE_PATH)

format: isort black

isort:
	isort $(FORMATTED_PYTHON_PATHS)

black:
	black --config=black.toml $(FORMATTED_PYTHON_PATHS)

lint:
	flake8 $(LINTED_PYTHON_PATHS)
