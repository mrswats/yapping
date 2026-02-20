# Yapping

Yet another python packaging manager.

But it is basically a thin wrapper around
[`pip-tools`](https://github.com/jazzband/pip-tools) which also adds and
removes dependencies from pyproject's `dependency` list.

## Installation:

```
pip install yapping
```

## Usage:

Using `yap` is very easy:

```console
yap add '<foo>'
yap rm '<foo>'
yap compile
yap version <version_upgrade_type>
```

You can also call the module directly, like:

```console
python -m yapping <...>
```

## Why you should use `yap`?

You should not. This is my personal pet project.
But, the good thing about it is that it does not lock you into it besides using
`pip-tools` for compiling the dependencies.

## Development

### Virtual Environment

Create a virtual Environment

```
virtualenv .venv -p pytthon 3.14
source .venv/bin/activate
```

### Tests

Using pytest for Tests

```
python -m pytest
```

### Formatting and Linting

Using pre-commit for linting and formatting

```
pre-commit install
pre-commit run --all-files
```

## Changelog

## v0.5.0

Add support for `optional-dependencies`.

## v0.4.0

Fixed an issue when running `yap` through `pipx` in which the `pip-compile` binary was not found.

## v0.3.0

Add the new `version` command to manage versions in `pyproject.toml`.

## v0.2.0

Add `--version` flag to check the version of the tool.

## v0.1.0

First release of the project. `add`, `rm`, `compile` commands.
