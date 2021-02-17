from typing import Any, Dict, Optional, Sequence, TextIO, Tuple, Union

from typing_extensions import Protocol, TypedDict

class _UnderlyingLogger(Protocol): ...

class _LoggerFactory(Protocol):
    def __call__(self, *args: Any) -> _UnderlyingLogger: ...

class PrintLoggerFactory(_LoggerFactory):
    def __init__(self, file: Optional[TextIO] = None): ...

_ProcessorReturnType = Union[str, Tuple[Sequence[Any], Dict[str, Any]], Dict[str, Any]]

class _Processor(Protocol):
    def __call__(
        self,
        logger: _UnderlyingLogger,
        method_name: str,
        event_dict: Dict[str, Any],
    ) -> _ProcessorReturnType: ...

class BoundLogger:
    def bind(self, **new_values: Any) -> BoundLogger: ...
    def msg(self, method_name: Optional[str] = None, **event_dict: Any) -> None: ...
    log = debug = info = warn = warning = msg
    fatal = failure = err = error = critical = exception = msg

class _ConfigDict(TypedDict):
    processors: Sequence[_Processor]
    # context_class
    # wrapper_class
    logger_factory: _LoggerFactory
    # cache_logger_on_first_use

def configure(
    processors: Optional[Sequence[_Processor]] = None,
    logger_factory: Optional[_LoggerFactory] = None,
) -> None: ...
def get_config() -> _ConfigDict: ...
def get_logger(*logger_factory_args: Any, **initial_values: Any) -> BoundLogger: ...
def wrap_logger(
    logger: Optional[_UnderlyingLogger],
    processors: Optional[Sequence[_Processor]] = None,
    # wrapper_class
    # context_class
    # cache_logger_on_first_use
    # logger_factory_args
    **initial_values: Any,
) -> BoundLogger: ...

class DropEvent(Exception): ...

from . import dev, processors, stdlib
