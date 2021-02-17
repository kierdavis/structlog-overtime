# structlog-overtime

Utilities for structlog.

## Features

### Tee

`TeeLoggerFactory` lets you send events to multiple underlying loggers.
For example, you may want to send log events both to the console and to a file:

```python
import structlog, structlog_overtime, sys  # noqa: E401

structlog.configure(
  # The default list of processors contains a ConsoleRenderer, but
  # TeeLoggerFactory cannot operate on rendered events so we need to
  # override it.
  processors=[
    structlog.processors.StackInfoRenderer(),
    structlog.dev.set_exc_info,
    structlog.processors.format_exc_info,
    structlog.processors.TimeStamper(),
  ],

  logger_factory=structlog_overtime.TeeLoggerFactory(
    structlog_overtime.TeeOutput(
      processors=[structlog.dev.ConsoleRenderer(colors=sys.stderr.isatty())],
      logger_factory=structlog.PrintLoggerFactory(sys.stderr),
    ),
    structlog_overtime.TeeOutput(
      processors=[structlog.processors.JSONRenderer()],
      logger_factory=structlog.PrintLoggerFactory(open("test.log", "a")),
    ),
  ),
)
structlog.get_logger().info("Hello, world!", data=123)
```

## Development

### Running the tests

```sh
git clone git@git:kdavis/structlog-overtime.git
cd structlog-overtime
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
```
