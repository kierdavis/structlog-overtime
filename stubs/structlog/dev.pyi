from typing import Any, Dict, Optional

from . import _Processor

class ConsoleRenderer(_Processor):
    def __init__(
        self,
        pad_event: int = 0,  # not the real default
        colors: bool = False,  # not the real default
        force_colors: bool = False,
        repr_native_str: bool = False,
        level_styles: Optional[
            Dict[str, Any]
        ] = None,  # value type is actually a colorama style, but cba to create stubs for that package too
    ): ...

set_exc_info: _Processor
