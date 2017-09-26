import sys
from typing import Callable
from pyre import cli
from pyre.utils import eprint


def except_handler(func: Callable) -> None:
    try:
        func()
        sys.exit(0)

    except KeyboardInterrupt:
        eprint('\nScript aborted by user. (KeyboardInterrupt)')
        sys.exit(1)


def execute() -> None:
    except_handler(cli.render)


if __name__ == '__main__':
    execute()
