import re
from contextlib import suppress
from unittest.mock import patch

import pytest

from yapping.cli import main


def test_main_add_command():
    with (
        patch("yapping.cli.commands.add_dependency") as m_add_dep,
        patch("yapping.cli.commands.compile_dependencies"),
    ):
        main(["add", "foo"])

    m_add_dep.assert_called_with("pyproject.toml", "foo")


def test_main_rm_command():
    with (
        patch("yapping.cli.commands.remove_dependency") as m_rm_dep,
        patch("yapping.cli.commands.compile_dependencies"),
    ):
        main(["rm", "foo"])

    m_rm_dep.assert_called_with("pyproject.toml", "foo")


@pytest.mark.parametrize("command", ("add", "rm"))
def test_main_commands_call_compile(command, setup_file):
    with (
        patch("yapping.cli.commands.add_dependency"),
        patch("yapping.cli.commands.remove_dependency"),
        patch("yapping.cli.commands.compile_dependencies") as m_pip_compile,
    ):
        main([command, "foo"])

    m_pip_compile.assert_called_once()


def test_main_compile_calls_compile():
    with patch("yapping.cli.commands.compile_dependencies") as m_pip_compile:
        main(["compile"])

    m_pip_compile.assert_called_once()


def test_main_version(capsys):
    with suppress(SystemExit):
        main(["--version"])

    out, err = capsys.readouterr()

    assert re.match(r"v\d\.\d\.\d", out) is not None
    assert err == ""


def test_main_no_args_prints_help(capsys):
    main([])

    out, err = capsys.readouterr()

    assert len(out) > 0
    assert err == ""
