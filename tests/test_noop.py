import structlog
from testfixtures import compare  # type: ignore

import structlog_overtime


def test_noop() -> None:
    dest = structlog_overtime.MockLoggerFactory()
    structlog.configure(
        processors=[structlog_overtime.noop],
        logger_factory=dest,
    )
    structlog.get_logger().info("hello world")
    compare(
        dest.records,
        expected=[
            structlog_overtime.MockLogRecord(
                method_name="info",
                event={"event": "hello world"},
            )
        ],
    )
