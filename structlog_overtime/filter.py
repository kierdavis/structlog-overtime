from typing import Any, Collection, Dict

import structlog

__all__ = ["FilterMethodName", "FilterKeys"]


class FilterMethodName:
    def __init__(
        self,
        *,
        include_only: Collection[str] = frozenset(),
        exclude: Collection[str] = frozenset(),
    ):
        self.include_only = include_only
        self.exclude = exclude

    def __call__(
        self,
        logger: "structlog._UnderlyingLogger",
        method_name: str,
        event_dict: Dict[str, Any],
    ) -> "structlog._ProcessorReturnType":
        if self.include_only and method_name not in self.include_only:
            raise structlog.DropEvent
        if method_name in self.exclude:
            raise structlog.DropEvent
        return event_dict


class FilterKeys:
    def __init__(
        self,
        *,
        include_only: Collection[str] = frozenset(),
        exclude: Collection[str] = frozenset(),
    ):
        self.include_only = include_only
        self.exclude = exclude

    def __call__(
        self,
        logger: "structlog._UnderlyingLogger",
        method_name: str,
        event_dict: Dict[str, Any],
    ) -> "structlog._ProcessorReturnType":
        keys_to_delete = set(event_dict.keys()) & set(self.exclude)
        if self.include_only:
            keys_to_delete |= set(event_dict.keys()) - set(self.include_only)
        for key in keys_to_delete:
            del event_dict[key]
        return event_dict
