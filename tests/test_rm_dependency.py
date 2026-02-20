import tomllib

from yapping.commands import remove_dependency
from yapping.commands import remove_optional_dependency


def test_rm_dependency_removes_dependency(setup_file):
    remove_dependency(setup_file, "django")

    with open(setup_file, "rb") as fp:
        data = tomllib.load(fp)

    assert "django" not in data["project"]["dependencies"]


def test_rm_dependency_idempotency(setup_file):
    remove_dependency(setup_file, "django")
    remove_dependency(setup_file, "django")

    with open(setup_file, "rb") as fp:
        data = tomllib.load(fp)

    assert "django" not in data["project"]["dependencies"]


def test_rm_optional_dependency_removes_dependency_from_optional_dependencies(
    setup_file,
):
    remove_optional_dependency(setup_file, "test", "pytest-django")

    with open(setup_file, "rb") as fp:
        data = tomllib.load(fp)

    assert "pytest-django" not in data["project"]["optional-dependencies"]["test"]


def test_rm_optional_dependency_is_idempotent(setup_file):
    remove_optional_dependency(setup_file, "test", "pytest")
    remove_optional_dependency(setup_file, "test", "pytest")

    with open(setup_file, "rb") as fp:
        data = tomllib.load(fp)

    assert "pytest" not in data["project"]["optional-dependencies"]["test"]
