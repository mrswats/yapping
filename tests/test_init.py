import os
import tomllib

import pytest

from yapping.commands import init
from yapping.exceptions import YappingException


@pytest.fixture
def call_init(tmp_path):
    def _():
        init("foo", tmp_path)

        return tmp_path

    return _


def test_init_command_creates_pyproject_file(call_init):
    tmp_path = call_init()

    assert os.path.exists(tmp_path / "pyproject.toml")


def test_init_command_contains_correct_project_name(call_init):
    tmp_path = call_init()

    with open(tmp_path / "pyproject.toml", "rb") as f:
        data = tomllib.load(f)

    assert data["project"]["name"] == "foo"


def test_init_command_raises_exception_if_file_exists(call_init, tmp_path):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.touch()

    with pytest.raises(YappingException) as exc:
        call_init()

    assert exc.value.args == ("Will not overwrite existing `pyproject.toml` file.",)
