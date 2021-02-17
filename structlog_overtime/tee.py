from typing import Any, Callable, List, Sequence, Type, cast

import structlog
from dataclasses import dataclass, field

__all__ = ["TeeOutput", "TeeLoggerFactory", "ConfigurationError"]


@dataclass
class TeeOutput:
    """
    A specification of a destination that a TeeLoggerFactory should send
    log events to. A chain of destination-specific processors can be
    applied before the log event ultimately makes it way to a logger created
    from the underlying factory.
    """

    logger_factory: Callable[..., structlog.types.WrappedLogger]
    processors: Sequence[structlog.types.Processor] = field(default_factory=list)

    def _construct_bound_logger(self, *args: Any) -> structlog.BoundLogger:
        return cast(
            structlog.BoundLogger,
            structlog.wrap_logger(
                logger=self.logger_factory(*args),
                processors=self.processors,
            ),
        )


class TeeLogger:
    def __init__(self, destinations: List[structlog.BoundLogger]):
        self.destinations = destinations

    def __getattr__(self, method_name: str) -> Any:
        def f(*args_from_renderer: Any, **event_dict: Any) -> None:
            if len(args_from_renderer):
                raise ConfigurationError(
                    "TeeLoggerFactory cannot operate on events that have "
                    "already been processed by a Renderer. Please place "
                    "the Renderer in the per-output processor lists instead "
                    "of the top-level list passed to structlog.configure."
                )
            for destination in self.destinations:
                getattr(destination, method_name)(**event_dict.copy())

        return f


_ensure_logger_implements_protocol: Type[structlog.types.WrappedLogger] = TeeLogger


class TeeLoggerFactory:
    """
    A logger factory that duplicates events to multiple destinations.

    For example, the following code sets up structlog to send events to both
    the console and a JSON file:

        import structlog, structlog_overtime, sys

        structlog.configure(
          # The default list of processors contains a ConsoleRenderer, but
          # TeeLoggerFactory cannot operate on rendered events so we must
          # remove it.
          processors=[
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.format_exc_info,
            structlog.processors.TimeStamper(),
          ],

          logger_factory=structlog_overtime.TeeLoggerFactory(
            structlog_overtime.TeeOutput(
              processors=[structlog.dev.ConsoleRenderer(colors=sys.stderr.isatty())],
              logger_factory=structlog.PrintLoggerFactory(sys.stderr),
            ),
            structlog_overtime.TeeOutput(
              processors=[structlog.processors.JSONRenderer()],
              logger_factory=structlog.PrintLoggerFactory(open("test.log", "a")),
            ),
          ),
        )
    """

    def __init__(self, *outputs: TeeOutput):
        self.outputs = outputs

    def __call__(self, *args: Any) -> TeeLogger:
        return TeeLogger(
            [output._construct_bound_logger(*args) for output in self.outputs]
        )


_ensure_logger_factory_implements_protocol: Type[
    Callable[..., structlog.types.WrappedLogger]
] = TeeLoggerFactory


class ConfigurationError(Exception):
    pass
