# Considering making a proper script to do a lot of this stuff for
# people...

import argparse
import sys
import platform


def create_local_file(name: str, contents: str):
    ...


def truncate(s: str, maxwidth: int, indent: str = "") -> str:
    """
    Truncate some human-readable text to be at most `maxwidth`. If words
    are too long, overflow `maxwidth`. `indent` is placed before every
    line.
    """
    maxwidth -= len(indent)
    ts = indent
    words = s.split(" ")
    line: list[str] = []
    linelen = 0
    for word in words:
        if word == "":
            continue
        newlen = linelen + len(word)
        if newlen < maxwidth:
            linelen = newlen + 1
            line.append(word)
        else:
            ts += " ".join(line) + "\n"
            line = [indent + word]
            linelen = len(word) + 1
    ts += " ".join(line)
    return ts


class UsageError(Exception):
    """
    Unrecoverable usage error
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

    def display(self):
        """
        Print to stderr
        """
        truncated = truncate(self.message, 72, indent="ERROR: ")
        print(truncated, file=sys.stderr)


def validate_knum(knum: str):
    """
    throws `UsageError` on failure. At the moment, we just accept any
    old shit.
    """


def validate_platform(system: str):
    """
    throws `UsageError` on failure. Validates the platform running this
    process
    """
    match system:
        case "Linux" | "Darwin":
            ...
        case _:
            raise UsageError(
                f"Only works for Linux or Darwin, " + "but you have '{system}'"
            )


def main():
    parser = argparse.ArgumentParser(
        prog="GenerateOSCShellScripts",
        description=truncate(
            "Generate a bunch of shell scripts to make your OSC life a bit easier", 72
        ),
    )
    parser.add_argument("knum")

    args = parser.parse_args()
    validate_knum(args.knum)
    validate_platform(platform.system())


if __name__ == "__main__":
    try:
        main()
    except UsageError as e:
        e.display()
