from io import StringIO

import structlog
from testfixtures import compare  # type: ignore

import structlog_overtime


def test_mock() -> None:
    factory1 = structlog_overtime.MockLoggerFactory()
    factory2 = structlog_overtime.MockLoggerFactory()
    structlog.configure(
        processors=[],
        logger_factory=structlog_overtime.TeeLoggerFactory(
            structlog_overtime.TeeOutput(logger_factory=factory1),
            structlog_overtime.TeeOutput(logger_factory=factory2),
        ),
    )
    structlog.get_logger("myloggername").info("hello world", foo="bar")
    for factory in factory1, factory2:
        compare(
            factory.records,
            expected=[
                structlog_overtime.MockLogRecord(
                    method_name="info",
                    event={"event": "hello world", "foo": "bar"},
                    get_logger_args=("myloggername",),
                ),
            ],
        )


def test_print_to_buffer() -> None:
    text_buffer = StringIO()
    json_buffer = StringIO()
    structlog.configure(
        processors=[],
        logger_factory=structlog_overtime.TeeLoggerFactory(
            structlog_overtime.TeeOutput(
                processors=[structlog.dev.ConsoleRenderer(colors=False)],
                logger_factory=structlog.PrintLoggerFactory(text_buffer),
            ),
            structlog_overtime.TeeOutput(
                processors=[structlog.processors.JSONRenderer()],
                logger_factory=structlog.PrintLoggerFactory(json_buffer),
            ),
        ),
    )
    structlog.get_logger().info("hello world", foo="bar")
    compare(text_buffer.getvalue(), expected="hello world                    foo=bar\n")
    compare(
        json_buffer.getvalue(), expected="""{"foo": "bar", "event": "hello world"}\n"""
    )
    structlog.configure(
        processors=[],
        logger_factory=structlog_overtime.TeeLoggerFactory(
            structlog_overtime.TeeOutput(
                processors=[structlog.dev.ConsoleRenderer(colors=False)],
                logger_factory=structlog.PrintLoggerFactory(text_buffer),
            ),
            structlog_overtime.TeeOutput(
                processors=[structlog.processors.JSONRenderer()],
                logger_factory=structlog.PrintLoggerFactory(json_buffer),
            ),
        ),
    )
