import tomllib

import pytest
import tomli_w

from yapping.commands import update_version
from yapping.exceptions import YappingException


@pytest.mark.parametrize(
    "update_type, new_version",
    [
        ("patch", "0.1.1"),
        ("minor", "0.2.0"),
        ("major", "1.0.0"),
    ],
)
def test_update_version(setup_file, update_type, new_version):
    update_version(setup_file, update_type)

    with open(setup_file, "rb") as fp:
        data = tomllib.load(fp)

    assert data["project"]["version"] == new_version


def test_update_version_with_non_compatible_version_schema(setup_file):
    with open(setup_file, "rb") as f:
        data = tomllib.load(f)

    data["project"]["version"] = "foo"

    with open(setup_file, "wb") as f:
        tomli_w.dump(data, f)

    with pytest.raises(YappingException) as exc:
        update_version(setup_file, "patch")

    assert exc.value.args[0] == "Version does not match semver: X.Y.Z"
