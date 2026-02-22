import functools
import os
import re
import site
import subprocess
import sys
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


TEMPLATE_DIR = os.path.abspath(
    os.path.join(__file__, "../templates/pyproject.toml"),
)

PYTHON_VERSION = (
    f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
)


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


@functools.cache
def find_pip_compile_bin() -> str:
    yap_site = os.path.join("/", *site.getsitepackages()[0].split("/")[:-3])
    return os.path.join(yap_site, "bin", "pip-compile")


def compile_dependencies(pyproject_filename: str) -> None:
    cmd = (
        find_pip_compile_bin(),
        "--quiet",
        "--generate-hashes",
        pyproject_filename,
    )
    subprocess.run(cmd, check=True, capture_output=True)


def compile_test_dependencies(
    pyproject_filename: str, test_extra: str, test_requirements_output_file: str
) -> None:
    cmd = (
        find_pip_compile_bin(),
        "--quiet",
        "--generate-hashes",
        f"--extra={test_extra}",
        "-o",
        test_requirements_output_file,
        pyproject_filename,
    )
    subprocess.run(cmd, check=True, capture_output=True)


def remove_dependency(pyproject_filename: str, package: str) -> None:
    def _(pyproject_data: PyprojectData, package: str) -> PyprojectData:
        dependencies = list(pyproject_data["project"]["dependencies"])

        if package in dependencies:
            dependencies.remove(package)
            dependencies.sort()

        pyproject_data["project"]["dependencies"] = dependencies

        return pyproject_data

    _read_write_toml_file(_, pyproject_filename, package)


def remove_optional_dependency(
    pyproject_filename: str, extra: str, package: str
) -> None:
    def _(pyproject_data: PyprojectData, package: str) -> PyprojectData:
        dependencies = list(pyproject_data["project"]["optional-dependencies"][extra])

        if package in dependencies:
            dependencies.remove(package)
            dependencies.sort()

        pyproject_data["project"]["optional-dependencies"][extra] = dependencies

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


def add_optional_dependency(pyproject_filename: str, extra: str, package: str) -> None:
    def _(pyproject_data: PyprojectData, package: str) -> PyprojectData:
        dependencies = list(pyproject_data["project"]["optional-dependencies"][extra])

        if package not in dependencies:
            dependencies.append(package)
            dependencies.sort()

        pyproject_data["project"]["optional-dependencies"][extra] = dependencies

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


def init(project_name: str, output_dir: str) -> None:
    with open(TEMPLATE_DIR, "rb") as f:
        template_data = tomllib.load(f)

    template_data["project"]["name"] = project_name
    template_data["project"]["requires-python"] = f">={PYTHON_VERSION}"

    output_filename = os.path.join(output_dir, "pyproject.toml")

    if os.path.exists(output_filename):
        raise exceptions.YappingException(
            "Will not overwrite existing `pyproject.toml` file."
        )

    with open(output_filename, "wb") as f:
        tomli_w.dump(template_data, f)
