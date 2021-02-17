# structlog-overtime

Utilities for structlog with the goal of enabling complex use cases without
having to defer to standard library logging.

## Features

* [TeeLoggerFactory](./structlog_overtime/tee.py): copy events to multiple destinations (e.g. console and file)
* [MockLoggerFactory](./structlog_overtime/mock.py): accumulates events in a list (useful for tests)
* [FilterMethods](./structlog_overtime/filter.py): filter events based on the method that was called (i.e. filter by log level)
* [FilterKeys](./structlog_overtime/filter.py): adjust which fields are included in your event dicts
* [TimezoneAwareTimeStamper](./structlog_overtime/timestamper.py): make your timestamps explicitly include a timezone
* [bind](./structlog_overtime/bind.py): type-preserving wrapper around BoundLogger.bind
* [noop](./structlog_overtime/noop.py): a processor that gloriously does nothing

## The name?

https://www.youtube.com/watch?v=GnEmD17kYsE

## Development

### Running the tests

```sh
git clone git@github.com:kierdavis/structlog-overtime.git
cd structlog-overtime
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

### Making a release

1.  Bump the version number in `setup.py`
2.  Commit the version nummber change: `git commit`
3.  Publish to PyPI and create git tag: `carthorse --config carthorse.yaml`
