import datetime

import structlog
from testfixtures import compare  # type: ignore

import structlog_overtime


def mock_now() -> datetime.datetime:
    return datetime.datetime(
        2020, 11, 9, 12, 34, 56, tzinfo=datetime.timezone(datetime.timedelta(hours=3))
    )


def test_timestamper() -> None:
    dest = structlog_overtime.MockLoggerFactory()
    structlog.configure(
        processors=[structlog_overtime.TimezoneAwareTimeStamper(now=mock_now)],
        logger_factory=dest,
    )
    structlog.get_logger().info("hello world")
    compare(
        dest.records,
        expected=[
            structlog_overtime.MockLogRecord(
                method_name="info",
                event={"event": "hello world", "timestamp": "2020-11-09T12:34:56+0300"},
            )
        ],
    )
