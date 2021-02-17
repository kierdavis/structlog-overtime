from typing import Any, Callable, Dict

import structlog

__all__ = [
    "FilterKeys",
    "FilterMethods",
    "exclude_keys",
    "exclude_methods",
    "only_keys",
    "only_methods",
]


class FilterMethods:
    def __init__(
        self,
        predicate: Callable[[str], bool],
    ):
        self.predicate = predicate

    def __call__(
        self,
        logger: "structlog._UnderlyingLogger",
        method_name: str,
        event_dict: Dict[str, Any],
    ) -> "structlog._ProcessorReturnType":
        if self.predicate(method_name):
            return event_dict
        else:
            raise structlog.DropEvent


def only_methods(*names: str) -> FilterMethods:
    return FilterMethods(lambda name: name in names)


def exclude_methods(*names: str) -> FilterMethods:
    return FilterMethods(lambda name: name not in names)


class FilterKeys:
    def __init__(
        self,
        predicate: Callable[[str], bool],
    ):
        self.predicate = predicate

    def __call__(
        self,
        logger: "structlog._UnderlyingLogger",
        method_name: str,
        event_dict: Dict[str, Any],
    ) -> "structlog._ProcessorReturnType":
        for key in set(event_dict.keys()):
            if not self.predicate(key):
                del event_dict[key]
        return event_dict


def only_keys(*names: str) -> FilterKeys:
    return FilterKeys(lambda name: name in names)


def exclude_keys(*names: str) -> FilterKeys:
    return FilterKeys(lambda name: name not in names)
