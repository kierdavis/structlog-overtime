import logging
from typing import Any, ClassVar, Dict, Optional

from . import _LoggerFactory, _Processor

class LoggerFactory(_LoggerFactory): ...

class ProcessorFormatter(logging.Formatter):
    wrap_for_formatter: ClassVar[_Processor]

add_log_level: _Processor
filter_by_level: _Processor
