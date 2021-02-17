from typing import Callable

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
    """
    A processor that filters log events based on the name of the method that
    was called on the BoundLogger.
    """

    def __init__(
        self,
        predicate: Callable[[str], bool],
    ):
        self.predicate = predicate

    def __call__(
        self,
        logger: structlog.types.WrappedLogger,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        if self.predicate(method_name):
            return event_dict
        else:
            raise structlog.DropEvent


def only_methods(*names: str) -> FilterMethods:
    """
    A specialisation of FilterMethods that only passes log events through if
    the method name is contained in 'names'.
    """
    return FilterMethods(lambda name: name in names)


def exclude_methods(*names: str) -> FilterMethods:
    """
    A specialisation of FilterMethods that drops log events if the method name
    is contained in 'names'.
    """
    return FilterMethods(lambda name: name not in names)


class FilterKeys:
    """
    A processor that filters the keys included in the event dictionary.
    """

    def __init__(
        self,
        predicate: Callable[[str], bool],
    ):
        self.predicate = predicate

    def __call__(
        self,
        logger: structlog.types.WrappedLogger,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        for key in set(event_dict.keys()):
            if not self.predicate(key):
                del event_dict[key]
        return event_dict


def only_keys(*keys: str) -> FilterKeys:
    """
    A specialisation of FilterKeys that only keeps the keys contained in 'keys'.
    """
    return FilterKeys(lambda key: key in keys)


def exclude_keys(*keys: str) -> FilterKeys:
    """
    A specialisation of FilterKeys that removes the keys contained in 'keys'.
    """
    return FilterKeys(lambda key: key not in keys)
