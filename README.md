# django-rainbowtests

[![PyPI version](https://img.shields.io/pypi/v/django-rainbowtests.svg?style=flat-square)](https://pypi.org/project/django-rainbowtests/)
[![License](https://img.shields.io/pypi/l/django-rainbowtests.svg?style=flat-square)](https://pypi.org/project/django-rainbowtests/)
[![CI](https://github.com/bradmontgomery/django-rainbowtests/actions/workflows/ci.yml/badge.svg)](https://github.com/bradmontgomery/django-rainbowtests/actions/workflows/ci.yml)

This is a custom test runner for Django that gives you *really* colorful test output.

## Installation

Install the latest release with:

```bash
pip install django-rainbowtests
```

Or with uv:

```bash
uv add django-rainbowtests
```

## Usage

Set your test runner in Django settings:

```python
TEST_RUNNER = "rainbowtests.test.runner.RainbowDiscoverRunner"
```

Then run your tests as usual:

```bash
python manage.py test
```

All of Django's test flags still work: `--buffer`, `--durations`, `--shuffle`, `--failfast`, and so on.
`--pdb` and `--debug-sql` use Django's own result classes, so their output is not colorized.

## Settings

### RAINBOWTESTS_HIGHLIGHT_PATH

While running your tests, any lines in your tracebacks that match this path will be highlighted, making them easier to find and read. If you omit this setting, the default is to use the path to your Django installation.

```python
RAINBOWTESTS_HIGHLIGHT_PATH = "/path/to/my/project/"
```

### RAINBOWTESTS_SHOW_MESSAGES

If the test output is too verbose and you just want a colorful version of the standard Django test output, set `RAINBOWTESTS_SHOW_MESSAGES` to `False`:

```python
RAINBOWTESTS_SHOW_MESSAGES = False
```

## Python/Django Compatibility

| Django | Python |
|---|---|
| 5.2 LTS | 3.11, 3.12, 3.13, 3.14 |
| 6.0 | 3.12, 3.13, 3.14 |
| 6.1 | 3.12, 3.13, 3.14, 3.15 |

Every combination above is tested in CI.

## Coverage

There is support for [coverage](http://nedbatchelder.com/code/coverage/) via a custom test runner:

```python
TEST_RUNNER = "rainbowtests.test.runner.RainbowDiscoverCoverageRunner"
```

Run your tests as normal (`python manage.py test`), and if you have coverage installed, you should see a report when your tests complete.

**Note:** The recommended modern workflow is to use `coverage run manage.py test` directly, which gives you more control over coverage settings.

## Development

This project uses [uv](https://github.com/astral-sh/uv) and a `Makefile`.

```bash
git clone https://github.com/bradmontgomery/django-rainbowtests.git
cd django-rainbowtests
make install    # uv sync --locked --all-groups
make check      # ruff lint + format check, ty type check, tests
```

| Target | What it does |
|---|---|
| `make test` | pytest; **fails below 100% line + branch coverage** |
| `make lint` | `ruff check` + `ruff format --check` |
| `make format` | auto-fix lint issues and format |
| `make typecheck` | [ty](https://github.com/astral-sh/ty) type check |
| `make build` | build sdist + wheel into `dist/` |

### Releasing

1. Bump `__version__` in `rainbowtests/__init__.py` and update `CHANGELOG.md`.
2. Tag and push: `git tag 1.0.0 && git push origin 1.0.0`.
3. The `publish` workflow runs the full CI suite, then publishes to PyPI with trusted publishing.

See [CHANGELOG.md](CHANGELOG.md) for release history.

## License

MIT. See [LICENSE.md](LICENSE.md).
