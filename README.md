# Yapping

Yet another python packaging manager.

But it is basically a thin wrapper around
[`pip-tools`](https://github.com/jazzband/pip-tools) which also adds and
removes dependencies from pyproject's `dependency` list

## Usage:

```console
yap add `foo`
yap rm `foo`
yap compile

```

## Installation:

```
pip install pyp
```

## Virtual Environment

Create a virtual Environment

```
virtualenv .venv -p pytthon 3.14
source .venv/bin/activate
```

## Tests

Using pytest for Tests

```
python -m pytest
```

## Formatting and Linting

Using pre-commit for linting and formatting

```
pre-commit install
pre-commit run --all-files
```
