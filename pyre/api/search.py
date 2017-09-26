# import re
import regex as re
import sys
import os
import io
import time
import mmap
import json
from typing import Optional, List, Pattern, NamedTuple, Union, Sequence
import pyre.constants as const
from pyre.utils import eprint
from multiprocessing import Pool


class Options(NamedTuple):
    search_bytes: Pattern
    search_expr: Pattern
    file_input: bool
    string_input: bool
    confirm: str
    encoding: str


class Match(NamedTuple):
    context: tuple
    match: str
    groups: list
    start: int
    end: int
    len: int
    line: int
    col: int


class Matches(NamedTuple):
    encoding: str
    source: str
    s_type: str
    matches: List[dict]


def get_line_num(source, m_start):
    if type(source) == str:
        source = io.StringIO(source[:m_start])
        i = 0
        for line in source:
            i += 1
        return i

    else:
        i = 0
        for line in source.readline():
            i += 1
        return i


def get_context(
    source,
    before: int,
    after: int,
    m_start: int,
    m_end: int,
    from_bytes: bool = False,
    encoding: Optional[str] = None,
):
    b_start = m_start - before
    b_start = b_start if b_start > 0 else 0
    a_end = m_end + after
    a_end = a_end if a_end > 0 else 0

    if from_bytes:
        return (
            source[b_start:m_start].decode(encoding),
            source[m_end:a_end].decode(encoding),
        )
    else:
        return (
            source[b_start:m_start],
            source[m_end:a_end],
        )


def _gen_urm(
    py_match_obj,
    source: Optional[str],
    encoding,
    from_bytes: bool
):
    m_start = py_match_obj.span()[0]
    m_end = py_match_obj.span()[1]
    context = get_context(source, 100, 10, m_start, m_end, from_bytes, encoding)

    if from_bytes:
        match = py_match_obj[0].decode(encoding)
        groups = tuple(g.decode(encoding) for g in py_match_obj.groups())
    else:
        match = py_match_obj[0]
        groups = tuple(g for g in py_match_obj.groups())

    match = Match(
        context=context,
        match=match,
        groups=groups,
        start=m_start,
        end=m_end,
        len=m_end - m_start,
        line=get_line_num(source, m_start),
        col=0,
    )

    return match._asdict()


def _process_file(
    source_file_obj,
    file_path: str,
    options: Options,
) -> None:
    """
    """
    source: mmap.mmap = mmap.mmap(
        source_file_obj.fileno(),
        0,
        access=mmap.ACCESS_READ,
    )

    matches: Sequence[Match] = options.search_bytes.finditer(source)

    urm_matches = [
        _gen_urm(m, source, encoding=options.encoding, from_bytes=True)
        for m
        in matches
    ]

    if urm_matches:
        urm = Matches(
            encoding=options.encoding,
            source=file_path,
            s_type='file',
            matches=urm_matches,
        )
        print(json.dumps(urm._asdict(), sort_keys=True, indent=4))
        # print(file_path)


def _try_process_file_input(
    file_path,
    options,
):
    """
    Validate current file and try to read it to search for matches and run
    substitutions.
    """

    try:
        with open(file_path, 'r', encoding=options.encoding) as source_file_obj:
            _process_file(
                source_file_obj=source_file_obj,
                file_path=file_path,
                options=options,
            )
    except IsADirectoryError:
        return


    except UnicodeDecodeError:
        const.DEBUG and eprint(
            'pyre: Skip file (UnicodeDecodeError): {}'.format(file_path)

        )
        return


def _process_string_input(string, options):
    if type(string) == bytes:
        string.encode(encoding=options.encoding)

    matches: Sequence[Match] = options.search_expr.finditer(string)

    urm_matches = [_gen_urm(m, string) for m in matches]

    if urm_matches:
        urm = Matches(
            encoding=options.encoding,
            source=string,
            s_type='str',
            matches=urm_matches,
        )

        print(json.dumps(urm._asdict(), sort_keys=True, indent=4))
        # print(string)


def _process_chunk(args):
    options = args[1]

    if options.file_input:
        for line in args[0]:
            _try_process_file_input(line, options)

    elif options.string_input:
        whole = ''
        for line in args[0]:
            whole += line
        _process_string_input(whole, options)


    elif options.string_input:
        for input_item in args[0]:
            _process_string_input(input_item, options)

    elif options.file_input:
        for input_item in args[0]:
            _try_process_file_input(input_item, options)


def _chunk_input(
    items: []
):
    chunk = []
    data_volume = 0
    flush_trigger = 1000
    trigger_max = 100000

    for item in items:
        if os.path.isdir(item):
            continue

        try:
            size = os.path.getsize(item)

        except FileNotFoundError:
            eprint(
                f'pyre: Skip file (FileNotFoundError): {item}'
            )
            continue

        except PermissionError:
            eprint(
                f'pyre: Skip file (PermissionError): {item}'
            )
            continue

        if size > 2147483647:
            eprint(
                f'pyre: Skip file (File larger than 2147483647 bytes): {item}'
            )
            continue

        chunk.append(item)
        data_volume += size

        if data_volume > flush_trigger:
            yield chunk
            chunk = []
            data_volume = 0
            if flush_trigger < trigger_max:
                flush_trigger += flush_trigger * 2

    yield chunk


def search(
    input_data: Optional[List[str]] = None,
    file_input: bool = True,
    string_input: bool = False,
    search: str = '',
    confirm: str = False,
    encoding: str = 'utf-8',
    dotall: str = False,
    ignorecase: bool = True,
) -> None:
    """
    The API function for replacing file contents.
    """
    # if const.DEBUG:
    start_time = time.time()

    if not input_data:
        input_data = (line.rstrip() for line in sys.stdin)

    flag_dotall = re.DOTALL if dotall else 0
    flag_ignorecase = re.IGNORECASE if ignorecase else 0
    flag_v = re.V0
    flags = flag_v | flag_dotall | flag_ignorecase

    search_bytes: Pattern = re.compile(bytes(search, encoding), flags)
    search_expr: Pattern = re.compile(search, flags)

    options = Options(
        search_bytes=search_bytes,
        search_expr=search_expr,
        file_input=file_input,
        string_input=string_input,
        confirm=confirm,
        encoding=encoding,
    )

    def _get_pool_args():
        return (
            (chunk, options,)
            for chunk
            in _chunk_input(input_data)
        )

    def run_async_pool():
        with Pool(os.cpu_count(), maxtasksperchild=1000) as pool:
            ps = pool.imap(_process_chunk, _get_pool_args(), chunksize=2)
            for p in ps:
                pass

    def run_sync():
        _process_chunk((
            input_data,
            options,
        ))

    if options.confirm:
        run_sync()

    else:
        run_async_pool()

    if const.DEBUG:
        end_time = time.time()
        elapsed = end_time - start_time
        print('source":', elapsed)
