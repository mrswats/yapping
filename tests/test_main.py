import re
from contextlib import suppress
from unittest.mock import patch

import pytest

from yapping.cli import main


def test_main_add_command():
    with (
        patch("yapping.cli.commands.add_dependency") as m_add_dep,
        patch("yapping.cli.commands.compile_dependencies"),
        patch("yapping.cli.commands.compile_test_dependencies"),
    ):
        main(["add", "foo"])

    m_add_dep.assert_called_with("pyproject.toml", "foo")


def test_main_add_extra_command():
    with (
        patch("yapping.cli.commands.add_optional_dependency") as m_add_dep,
        patch("yapping.cli.commands.compile_dependencies"),
        patch("yapping.cli.commands.compile_test_dependencies"),
    ):
        main(["add", "foo", "--extra"])

    m_add_dep.assert_called_with("pyproject.toml", "test", "foo")


def test_main_rm_command():
    with (
        patch("yapping.cli.commands.remove_dependency") as m_rm_dep,
        patch("yapping.cli.commands.compile_dependencies"),
        patch("yapping.cli.commands.compile_test_dependencies"),
    ):
        main(["rm", "foo"])

    m_rm_dep.assert_called_with("pyproject.toml", "foo")


def test_main_rm_extra_command():
    with (
        patch("yapping.cli.commands.remove_optional_dependency") as m_rm_dep,
        patch("yapping.cli.commands.compile_dependencies"),
        patch("yapping.cli.commands.compile_test_dependencies"),
    ):
        main(["rm", "foo", "--extra"])

    m_rm_dep.assert_called_with("pyproject.toml", "test", "foo")


@pytest.mark.parametrize("command", ("add", "rm"))
def test_main_commands_call_compile(command, setup_file):
    with (
        patch("yapping.cli.commands.add_dependency"),
        patch("yapping.cli.commands.remove_dependency"),
        patch("yapping.cli.commands.compile_dependencies") as m_pip_compile,
        patch("yapping.cli.commands.compile_test_dependencies") as m_pip_compile_test,
    ):
        main([command, "foo"])

    m_pip_compile.assert_called_once_with("pyproject.toml")
    m_pip_compile_test.assert_called_once_with(
        "pyproject.toml", "test", "test-requirements.txt"
    )


def test_main_compile_calls_compile():
    with (
        patch("yapping.cli.commands.compile_dependencies") as m_pip_compile,
        patch("yapping.cli.commands.compile_test_dependencies") as m_pip_compile_test,
    ):
        main(["compile"])

    m_pip_compile.assert_called_once_with("pyproject.toml")
    m_pip_compile_test.assert_called_once_with(
        "pyproject.toml", "test", "test-requirements.txt"
    )


def test_main_compile_only_extra_calls_compile():
    with (
        patch("yapping.cli.commands.compile_dependencies") as m_pip_compile,
        patch("yapping.cli.commands.compile_test_dependencies") as m_pip_compile_test,
    ):
        main(["compile", "--extra"])

    m_pip_compile.assert_not_called()
    m_pip_compile_test.assert_called_once_with(
        "pyproject.toml", "test", "test-requirements.txt"
    )


@pytest.mark.parametrize("update_type", ("patch", "minor", "major"))
def test_main_version_command(update_type):
    with patch("yapping.cli.commands.update_version") as m_version:
        main(["version", update_type])

    m_version.assert_called_once_with("pyproject.toml", update_type)


def test_main_init():
    with patch("yapping.cli.commands.init") as m_init:
        main(["init", "foo-project"])

    m_init.assert_called_once_with("foo-project", ".")


def test_main_init_compile():
    with (
        patch("yapping.cli.commands.init"),
        patch("yapping.cli.commands.compile_dependencies") as m_pip_compile,
        patch("yapping.cli.commands.compile_test_dependencies") as m_pip_compile_test,
    ):
        main(["init", "foo-project", "--compile"])

    m_pip_compile.assert_called_once()
    m_pip_compile_test.assert_called_once()


def test_main_version_command_wrong_choice():
    with pytest.raises(SystemExit) as exc, patch("yapping.cli.commands.update_version"):
        main(["version", "foo"])

    assert exc.value.code == 2


def test_main_unknown_command():
    with pytest.raises(SystemExit) as exc:
        main(["foo"])

    assert exc.value.code == 2


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
