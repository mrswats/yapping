import re
import subprocess
import tomllib
from typing import Any
from typing import Callable
from typing import NamedTuple

import tomli_w

from yapping import exceptions

type PyprojectData = dict[str, Any]
type CommandCallable = Callable[[PyprojectData, *tuple[str]], PyprojectData]


class Version(NamedTuple):
    major: str
    minor: str
    patch: str


def _read_write_toml_file(
    func: CommandCallable,
    pyproject_filename: str,
    *args: str,
) -> None:
    with open(pyproject_filename, "rb") as f:
        data = tomllib.load(f)

    new_data = func(data, *args)

    with open(pyproject_filename, "wb") as f:
        tomli_w.dump(new_data, f)


def compile_dependencies(pyproject_filename: str) -> None:
    cmd = ("pip-compile", "--generate-hashes", pyproject_filename)
    subprocess.run(cmd, check=True)


def remove_dependency(pyproject_filename: str, package: str) -> None:
    def _(pyproject_data: PyprojectData, package: str) -> PyprojectData:
        dependencies = list(pyproject_data["project"]["dependencies"])

        if package in dependencies:
            dependencies.remove(package)
            dependencies.sort()

        pyproject_data["project"]["dependencies"] = dependencies

        return pyproject_data

    _read_write_toml_file(_, pyproject_filename, package)


def add_dependency(pyproject_filename: str, package: str) -> None:
    def _(pyproject_data: PyprojectData, package: str) -> PyprojectData:
        dependencies = list(pyproject_data["project"]["dependencies"])

        if package not in dependencies:
            dependencies.append(package)
            dependencies.sort()

        pyproject_data["project"]["dependencies"] = dependencies

        return pyproject_data

    _read_write_toml_file(_, pyproject_filename, package)


def update_version(pyproject_filename: str, version_type: str) -> None:
    def _(pyproject_data: PyprojectData, version_type: str) -> PyprojectData:
        version = pyproject_data["project"]["version"]

        if not re.match(r"\d\.\d\.\d", version):
            raise exceptions.YappingException("Version does not match semver: X.Y.Z")

        current_version = Version(*version.split("."))

        new_version: Version | None = None
        if version_type == "patch":
            new_version = Version(
                current_version.major,
                current_version.minor,
                str(int(current_version.patch) + 1),
            )
        elif version_type == "minor":
            new_version = Version(
                current_version.major,
                str(int(current_version.minor) + 1),
                "0",
            )
        else:
            new_version = Version(
                str(int(current_version.major) + 1),
                "0",
                "0",
            )

        pyproject_data["project"]["version"] = ".".join(new_version)

        return pyproject_data

    _read_write_toml_file(_, pyproject_filename, version_type)
