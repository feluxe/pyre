"""
The 'cli' package defines the Command Line Interface for subs.
It reads and parses the user input from the commandline and calls the
equivalent function from the 'api' package.
"""
import sys
import os
from docopt import docopt
from pyre import api
import pyre.constants as const


def _is_interactive() -> bool:
    return any(
        item
        in sys.argv
        for item
        in ['-i', '--interactive']
    )


def _get_docopt_interface() -> str:
    interface: str = open(
        file='{}/interface.txt'.format(os.path.dirname(__file__)),
        mode='r'
    ).read()

    return interface \
        .replace('(', '[') \
        .replace(')', ']') \
        if _is_interactive() else interface


def _get_user_input() -> dict:
    return docopt(
        doc=_get_docopt_interface(),
        version=const.VERSION
    )


def render(
    uinput: dict = _get_user_input()
) -> None:
    """
    Execute command depending on user input.
    """
    if uinput['--debug']:
        const.set_debug(True)
        print('\nUINPUT', uinput)

    api.search(
        input_data=uinput['INPUT'],
        search=uinput['PATTERN'],
        file_input=not uinput['--str'],
        string_input=uinput['--str'],
    )

    # from subs.ag import _isearch_paths
    # from subs.api import replace_contents
    # replace_contents(
    #     search=uinput['--search'],
    #     paths=_isearch_paths(uinput['--search']),
    #     dry_run=True,
    #     confirm=True,
    # )
