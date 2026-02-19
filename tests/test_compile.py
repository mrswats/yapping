from unittest.mock import patch

from yapping.commands import compile_dependencies
from yapping.commands import compile_test_dependencies


def test_compile_dependencies_calls_pip_compile():
    with patch("subprocess.run") as m_run:
        compile_dependencies("foo.toml")

    m_run.assert_called()
    args = m_run.call_args[0]
    assert "pip-compile" in args[0][0]
    assert args[0][1:] == ("--quiet", "--generate-hashes", "foo.toml")


def test_compile_test_dependencies_calls_pip_compile():
    with patch("subprocess.run") as m_run:
        compile_test_dependencies("foo.toml", "test", "test-requirements.txt")

    m_run.assert_called()
    args = m_run.call_args[0]
    assert "pip-compile" in args[0][0]
    assert args[0][1:] == (
        "--quiet",
        "--generate-hashes",
        "--extra=test",
        "-o",
        "test-requirements.txt",
        "foo.toml",
    )
