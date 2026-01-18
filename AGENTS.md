# AI Agent Guidelines (AGENTS.md)

This repository is a small Django test-runner package intended to make test output more human-friendly by highlighting the most relevant portions of tracebacks and messages.

## Goals

- Prefer small, focused changes.
- Preserve existing behavior unless the task explicitly requires a behavior change.
- Keep the library usable as a drop-in Django `TEST_RUNNER`.

## Local setup

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Clone the repository
git clone https://github.com/bradmontgomery/django-rainbowtests.git
cd django-rainbowtests

# Install all dependencies (dev + test)
uv sync --group dev --group test
```

## How to validate changes

Run the test suite:

```bash
uv run pytest
```

Run the linter:

```bash
uv run ruff check .
```

Ensure the code compiles:

```bash
uv run python -m compileall rainbowtests
```

If you have a sample Django project handy, validate integration by setting:

```python
TEST_RUNNER = 'rainbowtests.test.runner.RainbowDiscoverRunner'
```

...and running `python manage.py test`.

## Code & style conventions

- Do not do repo-wide reformatting unless explicitly requested.
- Avoid adding new dependencies for minor changes.
- Keep color/output behavior changes isolated to the existing modules (`rainbowtests/colors.py`, `rainbowtests/messages.py`, and `rainbowtests/test/*`) when possible.
- Use `uv run ruff check --fix .` to fix lint issues.

## Python/Django Compatibility

- **Python**: 3.10, 3.11, 3.12, 3.13, 3.14
- **Django**: 4.2, 5.2

## Packaging / docs

- Packaging is managed via `pyproject.toml` (PEP 517/621 with setuptools).
- Version is defined in `rainbowtests/__init__.py` and read dynamically by setuptools.
- Keep documentation consistent with packaging metadata.
- Prefer Markdown for documentation.

## Safety & privacy

- Do not add secrets (API keys, tokens) to code, tests, docs, or CI.
- Do not print environment variables or filesystem paths that could contain sensitive info.
