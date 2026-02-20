import tomllib

from yapping.commands import add_dependency
from yapping.commands import add_optional_dependency


def test_add_dependency_adds_dependency(setup_file):
    add_dependency(setup_file, "foo")

    with open(setup_file, "rb") as fp:
        data = tomllib.load(fp)

    assert "foo" in data["project"]["dependencies"]


def test_add_dependency_is_idempotent(setup_file):
    add_dependency(setup_file, "bar")
    add_dependency(setup_file, "bar")

    with open(setup_file, "rb") as fp:
        data = tomllib.load(fp)

    assert data["project"]["dependencies"].count("bar") == 1


def test_add_optional_dependency_adds_dependency_to_optional_dependencies(setup_file):
    add_optional_dependency(setup_file, "test", "foo")

    with open(setup_file, "rb") as fp:
        data = tomllib.load(fp)

    assert "foo" in data["project"]["optional-dependencies"]["test"]


def test_add_optional_dependency_is_idempotent(setup_file):
    add_optional_dependency(setup_file, "test", "foo")
    add_optional_dependency(setup_file, "test", "foo")

    with open(setup_file, "rb") as fp:
        data = tomllib.load(fp)

    assert data["project"]["optional-dependencies"]["test"].count("foo") == 1
