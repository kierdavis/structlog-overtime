from typing import Any, List, Sequence, Type

import structlog
from dataclasses import dataclass, field

__all__ = ["TeeOutput", "TeeLoggerFactory"]


@dataclass
class TeeOutput:
    logger_factory: "structlog._LoggerFactory"
    processors: Sequence["structlog._Processor"] = field(default_factory=list)

    def _construct_bound_logger(self, *args: Any) -> structlog.BoundLogger:
        return structlog.wrap_logger(
            logger=self.logger_factory(*args),
            processors=self.processors,
        )


class TeeLogger:
    def __init__(self, destinations: List[structlog.BoundLogger]):
        self.destinations = destinations

    def __getattr__(self, method_name: str) -> Any:
        def f(*args_from_renderer: Any, **event_dict: Any) -> None:
            if len(args_from_renderer):
                raise NotImplementedError(
                    "TeeLoggerFactory cannot operate on events that have "
                    "already been processed by a Renderer. Please place "
                    "the Renderer in the per-output processor lists instead "
                    "of the top-level list passed to structlog.configure."
                )
            for destination in self.destinations:
                getattr(destination, method_name)(**event_dict.copy())

        return f


_ensure_logger_implements_protocol: Type["structlog._UnderlyingLogger"] = TeeLogger


class TeeLoggerFactory:
    def __init__(self, *outputs: TeeOutput):
        self.outputs = outputs

    def __call__(self, *args: Any) -> TeeLogger:
        return TeeLogger(
            [output._construct_bound_logger(*args) for output in self.outputs]
        )


_ensure_logger_factory_implements_protocol: Type[
    "structlog._LoggerFactory"
] = TeeLoggerFactory
