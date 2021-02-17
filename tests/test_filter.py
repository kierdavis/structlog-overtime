import structlog
from testfixtures import compare  # type: ignore

import structlog_overtime


def test_only_methods() -> None:
    dest = structlog_overtime.MockLoggerFactory()
    structlog.configure(
        processors=[structlog_overtime.only_methods("error", "critical")],
        logger_factory=dest,
    )
    logger = structlog.get_logger()
    logger.info("hello world")
    logger.error("hello world")
    logger.warning("hello world")
    logger.critical("hello world")
    compare(
        dest.records,
        expected=[
            structlog_overtime.MockLogRecord(
                method_name="error", event={"event": "hello world"}
            ),
            structlog_overtime.MockLogRecord(
                method_name="critical", event={"event": "hello world"}
            ),
        ],
    )


def test_exclude_methods() -> None:
    dest = structlog_overtime.MockLoggerFactory()
    structlog.configure(
        processors=[structlog_overtime.exclude_methods("error", "critical")],
        logger_factory=dest,
    )
    logger = structlog.get_logger()
    logger.info("hello world")
    logger.error("hello world")
    logger.warning("hello world")
    logger.critical("hello world")
    compare(
        dest.records,
        expected=[
            structlog_overtime.MockLogRecord(
                method_name="info", event={"event": "hello world"}
            ),
            structlog_overtime.MockLogRecord(
                method_name="warning", event={"event": "hello world"}
            ),
        ],
    )


def test_only_keys() -> None:
    dest = structlog_overtime.MockLoggerFactory()
    structlog.configure(
        processors=[structlog_overtime.only_keys("a", "b")],
        logger_factory=dest,
    )
    structlog.get_logger().info("hello world", a=1, b=2, c=3)
    compare(
        dest.records,
        expected=[
            structlog_overtime.MockLogRecord(method_name="info", event={"a": 1, "b": 2})
        ],
    )


def test_exclude_keys() -> None:
    dest = structlog_overtime.MockLoggerFactory()
    structlog.configure(
        processors=[structlog_overtime.exclude_keys("a", "b")],
        logger_factory=dest,
    )
    structlog.get_logger().info("hello world", a=1, b=2, c=3)
    compare(
        dest.records,
        expected=[
            structlog_overtime.MockLogRecord(
                method_name="info", event={"event": "hello world", "c": 3}
            )
        ],
    )
