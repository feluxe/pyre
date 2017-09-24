import sys
from typing import Callable
from pyre import cli


def except_handler(func: Callable) -> None:
    try:
        func()
        sys.exit(0)

    except KeyboardInterrupt:
        sys.stderr('\nScript aborted by user. (KeyboardInterrupt)')
        sys.exit(1)


def execute() -> None:
    except_handler(cli.render)


if __name__ == '__main__':
    execute()
