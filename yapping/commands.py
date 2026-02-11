import functools
import subprocess
import tomllib
from typing import Any
from typing import Callable

import tomli_w

type PyprojectData = dict[str, Any]


def _read_change_write(
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


@_read_change_write
def remove_dependency(pyproject_data: PyprojectData, package: str) -> PyprojectData:
    dependencies = list(pyproject_data["project"]["dependencies"])

    if package in dependencies:
        dependencies.remove(package)
        dependencies.sort()

    pyproject_data["project"]["dependencies"] = dependencies

    return pyproject_data


@_read_change_write
def add_dependency(pyproject_data: PyprojectData, package: str) -> PyprojectData:
    dependencies = list(pyproject_data["project"]["dependencies"])

    if package not in dependencies:
        dependencies.append(package)
        dependencies.sort()

    pyproject_data["project"]["dependencies"] = dependencies

    return pyproject_data
