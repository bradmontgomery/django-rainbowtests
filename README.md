# django-rainbowtests

[![PyPI version](http://img.shields.io/pypi/v/django-rainbowtests.svg?style=flat-square)](https://pypi.python.org/pypi/django-rainbowtests/)
[![License](http://img.shields.io/pypi/l/django-rainbowtests.svg?style=flat-square)](https://pypi.python.org/pypi/django-rainbowtests/)
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
TEST_RUNNER = 'rainbowtests.test.runner.RainbowDiscoverRunner'
```

Then run your tests as usual:

```bash
python manage.py test
```

## Settings

### RAINBOWTESTS_HIGHLIGHT_PATH

While running your tests, any lines in your tracebacks that match this path will be highlighted, making them easier to find and read. If you omit this setting, the default is to use the path to your Django installation.

```python
RAINBOWTESTS_HIGHLIGHT_PATH = '/path/to/my/project/'
```

### RAINBOWTESTS_SHOW_MESSAGES

If the test output is too verbose and you just want a colorful version of the standard Django test output, set `RAINBOWTESTS_SHOW_MESSAGES` to `False`:

```python
RAINBOWTESTS_SHOW_MESSAGES = False
```

## Python/Django Compatibility

- **Python**: 3.10, 3.11, 3.12, 3.13, 3.14
- **Django**: 4.2, 5.2, 6.0

## Coverage

There is support for [coverage](http://nedbatchelder.com/code/coverage/) via a custom test runner:

```python
TEST_RUNNER = 'rainbowtests.test.runner.RainbowDiscoverCoverageRunner'
```

Run your tests as normal (`python manage.py test`), and if you have coverage installed, you should see a report when your tests complete.

**Note:** The recommended modern workflow is to use `coverage run manage.py test` directly, which gives you more control over coverage settings.

## Development

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Clone the repository
git clone https://github.com/bradmontgomery/django-rainbowtests.git
cd django-rainbowtests

# Install dependencies
uv sync --group dev --group test

# Run tests
uv run pytest

# Run linter
uv run ruff check .
```

## License

MIT. See [LICENSE.md](LICENSE.md).
