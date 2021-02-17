from pathlib import Path

from setuptools import find_packages, setup

setup(
    name="structlog-overtime",
    version="1.0",
    description="Miscellaneous utilities for structlog",
    long_description=Path(__file__).resolve().parent.joinpath("README.md").read_text(),
    long_description_content_type="text/markdown",
    author="Kier Davis",
    author_email="me@kierdavis.com",
    url="https://github.com/kierdavis/structlog-overtime",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Typing :: Typed",
    ],
    packages=find_packages(exclude=["tests", "stubs"]),
    include_package_data=True,
    python_requires=">= 3.6",
    install_requires=[
        "dataclasses; python_version < '3.7'",
        "structlog >= 20.2.0",
        # ...
    ],
    extras_require={
        "dev": [
            "black",
            "carthorse",
            "flake8",
            "isort",
            "mypy",
            "pytest",
            "pytest-cov",
            "setuptools>=38.6.0",  # for long_description_content_type support
            "testfixtures",
            "twine",
            "wheel",
        ],
    },
    package_data={
        "structlog_overtime": ["py.typed"],
    },
)
