import datetime
from typing import Callable

import structlog

__all__ = ["TimezoneAwareTimeStamper"]


def _default_now() -> datetime.datetime:
    return datetime.datetime.now().astimezone()  # pragma: no cover


class TimezoneAwareTimeStamper:
    """
    A workaround for the fact that structlog.processors.TimeStamper only
    supports UTC or naive (timezone-less) timestamps. Use this if you
    want to make the timezone explicit in the formatted log message.
    Full datetime.strftime syntax is supported.
    """

    def __init__(
        self,
        *,
        format: str = "%Y-%m-%dT%H:%M:%S%z",
        key: str = "timestamp",
        now: Callable[[], datetime.datetime] = _default_now,
    ):
        self.format = format
        self.key = key
        self.now = now

    def __call__(
        self,
        logger: structlog.types.WrappedLogger,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        event_dict[self.key] = self.now().strftime(self.format)
        return event_dict
