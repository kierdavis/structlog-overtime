import structlog
from testfixtures import compare  # type: ignore

import structlog_overtime


def test_noop() -> None:
    dest = structlog_overtime.MockLoggerFactory()
    structlog.configure(
        processors=[],
        logger_factory=dest,
    )
    logger = structlog.get_logger()
    logger = structlog_overtime.bind(logger, a=1, b=2)
    logger.info("hello world")
    compare(
        dest.records,
        expected=[
            structlog_overtime.MockLogRecord(
                method_name="info",
                event={"event": "hello world", "a": 1, "b": 2},
            )
        ],
    )
