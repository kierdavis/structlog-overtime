from typing import Any, Dict, NewType

import structlog

__all__ = [
    "Level",
    "CRITICAL",
    "FATAL",
    "ERROR",
    "WARNING",
    "WARN",
    "INFO",
    "DEBUG",
    "NOTSET",
    "FilterByLevel",
]

Level = NewType("Level", int)

CRITICAL = Level(50)
FATAL = CRITICAL
ERROR = Level(40)
WARNING = Level(30)
WARN = WARNING
INFO = Level(20)
DEBUG = Level(10)
NOTSET = Level(0)

_NAME_TO_LEVEL = {
    "critical": CRITICAL,
    "exception": ERROR,
    "error": ERROR,
    "warn": WARNING,
    "warning": WARNING,
    "info": INFO,
    "debug": DEBUG,
    "notset": NOTSET,
}


class FilterByLevel:
    def __init__(self, min_level: Level):
        self.min_level = min_level

    def __call__(
        self,
        logger: "structlog._UnderlyingLogger",
        method_name: str,
        event_dict: Dict[str, Any],
    ) -> "structlog._ProcessorReturnType":
        if _NAME_TO_LEVEL[method_name] >= self.min_level:
            return event_dict
        else:
            raise structlog.DropEvent


_ensure_filter_by_level_implements_protocol: "structlog._Processor" = FilterByLevel(DEBUG)
