from setuptools import find_packages, setup

setup(
    name="structlog-overtime",
    version="0.1",
    # description="...",
    author="Kier Davis",
    author_email="me@kierdavis.com",
    # url="...",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Typing :: Typed",
        # ...
    ],
    packages=find_packages(exclude=["tests", "stubs"]),
    include_package_data=True,
    python_requires=">= 3.6",
    install_requires=[
        "dataclasses; python_version < '3.7'",
        "structlog",
        # ...
    ],
    extras_require={
        "dev": [
            "black",
            "devpi",
            "flake8",
            "isort",
            "mypy",
            "pytest",
            "pytest-cov",
            "testfixtures",
            "wheel",
            # ...
        ],
    },
)
