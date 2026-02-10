import shutil
from pathlib import Path

import pytest

TESTING_PYPROJECT = "testing/pyproject.toml"


@pytest.fixture
def setup_file(tmp_path: Path) -> Path:
    shutil.copy(TESTING_PYPROJECT, tmp_path)
    return tmp_path / "pyproject.toml"
