import structlog

__all__ = ["noop"]


def noop(
    logger: structlog.types.WrappedLogger,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict:
    """
    No operation (a processor that returns the event dictionary unchanged).
    """
    return event_dict
