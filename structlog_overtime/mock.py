import functools
from typing import Any, Callable, List, Tuple, Type

import structlog
from dataclasses import dataclass, field

__all__ = ["MockLogRecord", "MockLoggerFactory"]


@dataclass(frozen=True)
class MockLogRecord:
    """
    A record of a log event observed by a MockLoggerFactory.

    For example, this call:

        structlog.get_logger("my_logger_name").info("hello world", a=1, b=2)

    would typically result in the following MockLogRecord:

        MockLogRecord(
            method_name = "info",
            event = {"event": "hello world", "a": 1, "b": 2},
            get_logger_args = ("my_logger_name",),
        )

    The underlying_logger_args field is relevent if a renderer-style
    processor is applied to the log event before it is passed to the
    MockLoggerFactory. For example, this snippet:

        structlog.configure(
            processors=[structlog.dev.ConsoleRenderer()],
            logger_factory=MockLoggerFactory(),
        )
        structlog.get_logger("my_logger_name").info("hello world", a=1, b=2)

    would result in the following MockLogRecord:

        MockLogRecord(
            method_name = "info",
            get_logger_args = ("my_logger_name",),
            underlying_logger_args = ("hello world                    a=1 b=2\n",),
        )
    """

    method_name: str
    event: structlog.types.EventDict = field(default_factory=dict)
    get_logger_args: Tuple[Any, ...] = ()
    underlying_logger_args: Tuple[Any, ...] = ()


@dataclass
class MockLogger:
    records: List[MockLogRecord]
    get_logger_args: Tuple[Any, ...]

    def __getattr__(self, method_name: str) -> Any:
        return functools.partial(self._emit, method_name)

    def _emit(self, method_name: str, *underlying_logger_args: Any, **event: Any) -> None:
        self.records.append(
            MockLogRecord(
                method_name=method_name,
                event=event,
                get_logger_args=self.get_logger_args,
                underlying_logger_args=underlying_logger_args,
            )
        )


@dataclass
class MockLoggerFactory:
    """
    A logger factory that accumulates log events in a list. Useful for tests.
    """

    records: List[MockLogRecord] = field(default_factory=list)

    def __call__(self, *args: Any) -> structlog.types.WrappedLogger:
        return MockLogger(records=self.records, get_logger_args=args)


_ensure_logger_factory_implements_protocol: Type[
    Callable[..., structlog.types.WrappedLogger]
] = MockLoggerFactory
