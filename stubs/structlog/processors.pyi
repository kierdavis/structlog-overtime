from typing import Any, Dict, Optional, Union

from . import _Processor

class TimeStamper(_Processor):
    def __init__(
        self, fmt: Union[None, str] = None, utc: bool = True, key: str = "timestamp"
    ): ...

class JSONRenderer(_Processor): ...

format_exc_info: _Processor
