import functools
from typing import Any, Dict, List, Tuple, Type

import structlog
from dataclasses import dataclass, field

__all__ = ["MockLogRecord", "MockLogger", "MockLoggerFactory"]


@dataclass(frozen=True)
class MockLogRecord:
    method_name: str
    event: Dict[str, Any] = field(default_factory=dict)
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
    records: List[MockLogRecord] = field(default_factory=list)

    def __call__(self, *args: Any) -> "structlog._UnderlyingLogger":
        return MockLogger(records=self.records, get_logger_args=args)


_ensure_logger_factory_implements_protocol: Type[
    "structlog._LoggerFactory"
] = MockLoggerFactory
