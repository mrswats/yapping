#! /usr/bin/env python
from __future__ import annotations

import argparse
from importlib.metadata import version
from typing import Sequence

from yapping import commands

PYPROJECT_FILENAME = "pyproject.toml"


class Commands:
    ADD = "add"
    REMOVE = "rm"
    COMPILE = "compile"
    VERSION = "version"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"v{version("yapping")}",
        help="Print version of the tool.",
    )

    subparser = parser.add_subparsers(
        title="command",
        dest="command",
    )

    add_dependency_parser = subparser.add_parser(
        Commands.ADD,
        help="Add a new dependency",
    )
    add_dependency_parser.add_argument(
        "package",
        help="Name of the package to add.",
    )
    add_dependency_parser.add_argument(
        "--optional-dependencies",
        help="Name of the optional dependencies list",
        default="test",
    )
    add_dependency_parser.add_argument(
        "--test-requirements",
        help="Name of the test requirements file.",
        default="test-requirements.txt",
    )

    rm_parser = subparser.add_parser(
        Commands.REMOVE,
        help="Remove an existing dependency",
    )
    rm_parser.add_argument(
        "package",
        help="Name of the package to add.",
    )
    rm_parser.add_argument(
        "--optional-dependencies",
        help="Name of the optional dependencies list",
        default="test",
    )
    rm_parser.add_argument(
        "--test-requirements",
        help="Name of the test requirements file.",
        default="test-requirements.txt",
    )

    compile_parser = subparser.add_parser(
        Commands.COMPILE,
        help="compile dependencies with pip-tools' `pip-compile`",
    )
    compile_parser.add_argument(
        "--optional-dependencies",
        help="Name of the optional dependencies list",
        default="test",
    )
    compile_parser.add_argument(
        "--test-requirements",
        help="Name of the test requirements file.",
        default="test-requirements.txt",
    )

    version_parser = subparser.add_parser(
        Commands.VERSION,
        help="Updatea project version in pyproject.toml",
    )
    version_parser.add_argument(
        "version_type",
        help="What kind of version update to do.",
        choices=["patch", "minor", "major"],
        default="minor",
    )

    parsed_args = parser.parse_args(argv)

    do_compile = False

    if parsed_args.command == Commands.ADD:
        commands.add_dependency(PYPROJECT_FILENAME, parsed_args.package)
        do_compile = True
    elif parsed_args.command == Commands.REMOVE:
        commands.remove_dependency(PYPROJECT_FILENAME, parsed_args.package)
        do_compile = True
    elif parsed_args.command == Commands.COMPILE:
        do_compile = True
    elif parsed_args.command == Commands.VERSION:
        commands.update_version(PYPROJECT_FILENAME, parsed_args.version_type)
    else:
        parser.print_help()

    if do_compile:
        commands.compile_dependencies(PYPROJECT_FILENAME)
        commands.compile_test_dependencies(
            PYPROJECT_FILENAME,
            parsed_args.optional_dependencies,
            parsed_args.test_requirements,
        )

    return 0
