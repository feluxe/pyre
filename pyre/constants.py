"""
Package Level Constants.
"""
from pkg_resources import get_distribution, DistributionNotFound, \
    VersionConflict


def get_version() -> str:
    try:
        version: str = get_distribution('pyre').version or 'none'

    except DistributionNotFound or VersionConflict:
        version: str = 'none'

    return version


def set_debug(
    debug: bool = False
):
    global DEBUG, VERBOSE

    DEBUG = debug

    if debug:
        VERBOSE = debug


def set_verbose(
    verbose: bool = False
):
    global VERBOSE

    VERBOSE = verbose


# Default constants
VERSION = None

# Configurable constants
VERBOSE = False
DEBUG = False
