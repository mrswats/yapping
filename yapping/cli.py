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
    INIT = "init"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

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

    add_parser = subparser.add_parser(
        Commands.ADD,
        help="Add a new dependency",
    )
    add_parser.add_argument(
        "package",
        help="Name of the package to add.",
    )
    add_parser.add_argument(
        "--extra",
        help="Add package to the optional dependencies list.",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    add_parser.add_argument(
        "--optional-dependencies",
        help="Name of the optional dependencies list",
        default="test",
    )
    add_parser.add_argument(
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
        "--extra",
        help="Add package to the optional dependencies list.",
        action=argparse.BooleanOptionalAction,
        default=False,
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
    compile_parser.add_argument(
        "--extra",
        help="Add package to the optional dependencies list.",
        action=argparse.BooleanOptionalAction,
        default=False,
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

    init_parser = subparser.add_parser(
        Commands.INIT,
        help="Create a pyproject.toml from a template.",
    )
    init_parser.add_argument(
        "project_name",
        help="Name of the project.",
    )
    init_parser.add_argument(
        "--output-dir",
        help="Output directory for the generated pyproject.toml file.",
        default=".",
    )
    init_parser.add_argument(
        "--optional-dependencies",
        help="Name of the optional dependencies list",
        default="test",
    )
    init_parser.add_argument(
        "--test-requirements",
        help="Name of the test requirements file.",
        default="test-requirements.txt",
    )
    init_parser.add_argument(
        "--compile",
        action=argparse.BooleanOptionalAction,
        default=False,
    )

    parsed_args = parser.parse_args(argv)

    do_compile = False
    do_compile_test = False

    if parsed_args.command == Commands.ADD:
        do_compile_test = True

        if parsed_args.extra is True:
            commands.add_optional_dependency(
                PYPROJECT_FILENAME,
                parsed_args.optional_dependencies,
                parsed_args.package,
            )
        else:
            do_compile = True
            commands.add_dependency(PYPROJECT_FILENAME, parsed_args.package)
    elif parsed_args.command == Commands.REMOVE:
        do_compile_test = True

        if parsed_args.extra is True:
            commands.remove_optional_dependency(
                PYPROJECT_FILENAME,
                parsed_args.optional_dependencies,
                parsed_args.package,
            )
        else:
            do_compile = True
            commands.remove_dependency(PYPROJECT_FILENAME, parsed_args.package)
    elif parsed_args.command == Commands.COMPILE:
        do_compile_test = True

        if not parsed_args.extra:
            do_compile = True
    elif parsed_args.command == Commands.VERSION:
        commands.update_version(PYPROJECT_FILENAME, parsed_args.version_type)
    elif parsed_args.command == Commands.INIT:
        commands.init(parsed_args.project_name, parsed_args.output_dir)

        if parsed_args.compile:
            do_compile = True
            do_compile_test = True
    else:
        parser.print_help()

    if do_compile:
        commands.compile_dependencies(PYPROJECT_FILENAME)

    if do_compile_test:
        commands.compile_test_dependencies(
            PYPROJECT_FILENAME,
            parsed_args.optional_dependencies,
            parsed_args.test_requirements,
        )

    return 0
