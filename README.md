

```
 ╔══════════╗
 ║   pyre   ║
 ╚══════════╝

Get 'Universal Regex Matches' from Python's regex engines.

Usage:
    pyre [options] [PATTERN] [INPUT]...
    pyre -h | --help

    [PATTERN]           A regular expression.
    [INPUT]...          Can be file (default) or string. Reads from STDIN if
                        left empty.
Options:

Input Options:


      --str             Process.
      --json-in         Set INPUT/STDIN to JSON encoded 'universal regex match
                        obj'
                        # TODO: Is this needed?
      --encoding STR    Must be python compatible. (default: utf-8).
                        List of encodings that can be used:
                          https://docs.python.org/3/library/codecs.html#standard-encodings

Output Options:

        *Add reprint interface here.*

      --json-out        Return 'universal regex match objects' JSON encoded.
      --clines          Set --cb and --ca to count lines instead of chars.
      --cb NUM          Define NUM of lines or chars for the 'before-context'.
      --ca NUM          Define NUM of lines or chars for the 'after-context'.
      --cba NUM         Define NUM of lines or chars for both --ca and --cb.

Search Options:

      --regex           Use Python's newer 'regex' engine. (default)
      --re              Use Python's *old* 're' engine for your search.
      --dotall          Make the '.' special character match any character at
                        all, including a newline; without this flag, '.' will
                        match anything except a newline.
      --multiline       When specified, the pattern character '^' matches at the
                        beginning of the string and at the beginning of each
                        line (immediately following each newline); and the
                        pattern character '$' matches at the end of the string
                        and at the end of each line (immediately preceding each
                        newline).
      --ignorecase      Perform case-insensitive matching

Misc Options:

      --debug           Print even more info to the console.
      --version         Show version.
  -h, --help            Show (this) help screen.


Escaping:

    Use backslashes to escape Regex-Special-Chars. E.g.:
      \.hello

Examples:

    #TODO: This





```

# pyre



### Description

Get 'universal regex match objects' from Python's regex engines.
