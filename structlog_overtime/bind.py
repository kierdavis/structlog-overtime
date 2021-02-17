from typing import Any, TypeVar, cast

import structlog

__all__ = ["bind"]

BL = TypeVar("BL", bound=structlog.types.BindableLogger)


def bind(logger: BL, **new_values: Any) -> BL:
    """
    A plain wrapper around logger.bind(**new_values) that preserves the type
    annotation of the logger. Does not check at runtime that the return value
    is indeed the assumed type.

    Hopefully this will no longer be needed in a future version of structlog
    (see https://www.structlog.org/en/stable/types.html).
    """
    return cast(BL, logger.bind(**new_values))
