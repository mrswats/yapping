from unittest.mock import patch

from yap import compile_dependencies


def test_compile_dependencies_calls_pip_compile():
    with patch("subprocess.run") as m_run:
        compile_dependencies("foo.toml")

    m_run.assert_called_once_with(
        ("pip-compile", "--generate-hashes", "foo.toml"), check=True
    )
