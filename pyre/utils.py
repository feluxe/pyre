"""
This module contains utility functions for the pyre
application.
"""
import sys
from typing import Optional, IO


def eprint(
    *objects,
    sep: str = ' ',
    end: str = '\n',
    file: Optional[IO[str]] = sys.stderr,
    flush: bool = False
) -> None:
    print(*objects, sep=sep, end=end, file=file, flush=flush)
