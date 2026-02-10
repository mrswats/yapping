import tomllib

from yap import remove_dependency


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
