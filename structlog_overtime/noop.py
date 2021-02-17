from typing import Any, Dict

import structlog

__all__ = ["noop"]


def noop(
    logger: "structlog._UnderlyingLogger",
    method_name: str,
    event_dict: Dict[str, Any],
) -> "structlog._ProcessorReturnType":
    """
    No operation (a processor that returns the event dictionary unchanged).
    """
    return event_dict
