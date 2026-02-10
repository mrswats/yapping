#! /usr/bin/env python
from __future__ import annotations

import argparse
import functools
import subprocess
import tomllib
from typing import Any
from typing import Callable
from typing import Sequence

import tomli_w

type PyprojectData = dict[str, Any]

PYPROJECT_FILENAME = "pyproject.toml"


def read_change_write(
    func: Callable[[PyprojectData, str], PyprojectData],
) -> Callable[[str, str], None]:

    @functools.wraps(func)
    def _read_write_toml_file(pyproject_filename: str, package: str) -> None:
        with open(pyproject_filename, "rb") as f:
            data = tomllib.load(f)

        new_data = func(data, package)

        with open(pyproject_filename, "wb") as f:
            tomli_w.dump(new_data, f)

    return _read_write_toml_file


def compile_dependencies(pyproject_filename: str) -> None:
    cmd = ("pip-compile", "--generate-hashes", pyproject_filename)
    subprocess.run(cmd, check=True)


@read_change_write
def remove_dependency(pyproject_data: PyprojectData, package: str) -> PyprojectData:
    dependencies = list(pyproject_data["project"]["dependencies"])

    if package in dependencies:
        dependencies.remove(package)
        dependencies.sort()

    pyproject_data["project"]["dependencies"] = dependencies

    return pyproject_data


@read_change_write
def add_dependency(pyproject_data: PyprojectData, package: str) -> PyprojectData:
    dependencies = list(pyproject_data["project"]["dependencies"])

    if package not in dependencies:
        dependencies.append(package)
        dependencies.sort()

    pyproject_data["project"]["dependencies"] = dependencies

    return pyproject_data


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()

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
        add_dependency(PYPROJECT_FILENAME, parsed_args.package)
        do_compile = True
    elif parsed_args.command == "rm":
        remove_dependency(PYPROJECT_FILENAME, parsed_args.package)
        do_compile = True
    elif parsed_args.command == "compile":
        do_compile = True
    else:
        parser.print_help()

    if do_compile:
        compile_dependencies(PYPROJECT_FILENAME)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
