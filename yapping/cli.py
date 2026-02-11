#! /usr/bin/env python
from __future__ import annotations

import argparse
from importlib.metadata import version
from typing import Sequence

from yapping import commands

PYPROJECT_FILENAME = "pyproject.toml"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"v{version("yapping")}",
        help="Print version of the tool.",
    )

    subparser = parser.add_subparsers(title="command", dest="command")

    add_dependency_parser = subparser.add_parser(
        "add",
        help="Add a new dependency",
    )
    add_dependency_parser.add_argument(
        "package",
        help="Name of the package to add.",
    )

    rm_parser = subparser.add_parser(
        "rm",
        help="Remove an existing dependency",
    )
    rm_parser.add_argument(
        "package",
        help="Name of the package to add.",
    )

    subparser.add_parser(
        "compile",
        help="compile dependencies with pip-tools' `pip-compile`",
    )

    parsed_args = parser.parse_args(argv)

    do_compile = False

    if parsed_args.command == "add":
        commands.add_dependency(PYPROJECT_FILENAME, parsed_args.package)
        do_compile = True
    elif parsed_args.command == "rm":
        commands.remove_dependency(PYPROJECT_FILENAME, parsed_args.package)
        do_compile = True
    elif parsed_args.command == "compile":
        do_compile = True
    else:
        parser.print_help()

    if do_compile:
        commands.compile_dependencies(PYPROJECT_FILENAME)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
