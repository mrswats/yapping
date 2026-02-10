import tomllib

from yap import add_dependency


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
