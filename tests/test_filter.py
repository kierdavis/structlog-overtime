from typing import Dict, List, Set

import pytest
import structlog
from testfixtures import compare  # type: ignore

import structlog_overtime


@pytest.mark.parametrize(
    "kwargs,expected",
    [
        ({}, ["info", "error", "warning", "critical"]),
        ({"include_only": {"error", "critical"}}, ["error", "critical"]),
        ({"exclude": {"error"}}, ["info", "warning", "critical"]),
    ],
)
def test_filter_method_name(kwargs: Dict[str, Set[str]], expected: List[str]) -> None:
    dest = structlog_overtime.MockLoggerFactory()
    structlog.configure(
        processors=[structlog_overtime.FilterMethodName(**kwargs)],
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
                method_name=method_name,
                event={"event": "hello world"},
            )
            for method_name in expected
        ],
    )


@pytest.mark.parametrize(
    "kwargs,expected",
    [
        ({}, {"event", "a", "b", "c"}),
        ({"include_only": {"a", "b"}}, {"a", "b"}),
        ({"exclude": {"b"}}, {"event", "a", "c"}),
    ],
)
def test_filter_keys(kwargs: Dict[str, Set[str]], expected: Set[str]) -> None:
    dest = structlog_overtime.MockLoggerFactory()
    structlog.configure(
        processors=[structlog_overtime.FilterKeys(**kwargs)],
        logger_factory=dest,
    )
    structlog.get_logger().info("hello world", a=1, b=2, c=3)
    [record] = dest.records
    compare(set(record.event.keys()), expected=expected)
