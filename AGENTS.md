# AI Agent Guidelines (AGENTS.md)

This repository is a small Django test-runner package intended to make test output more human-friendly by highlighting the most relevant portions of tracebacks and messages.

## Goals

- Prefer small, focused changes.
- Preserve existing behavior unless the task explicitly requires a behavior change.
- Keep the library usable as a drop-in Django `TEST_RUNNER`.

## Local setup & validation

This project uses [uv](https://github.com/astral-sh/uv) and a `Makefile`.

```bash
make install   # uv sync --locked --all-groups
make check     # everything CI runs: ruff lint, ruff format --check, ty, pytest
```

- Tests must keep **100% line + branch coverage** (`--cov-fail-under=100` in `pyproject.toml`).
- `ty` must pass with no blanket ignores.
- Code is formatted with `ruff format`; run `make format` before committing.

To validate integration, use a sample Django project with:

```python
TEST_RUNNER = "rainbowtests.test.runner.RainbowDiscoverRunner"
```

...and run `python manage.py test` (try `-v 2`, `--buffer`, `--debug-sql`).

## Code & style conventions

- Avoid adding new dependencies for minor changes.
- Keep color/output behavior changes isolated to the existing modules (`rainbowtests/colors.py`, `rainbowtests/messages.py`, and `rainbowtests/test/*`) when possible.
- Use `make format` to fix lint and formatting issues.
- Add type hints to new code.
- Keep `RainbowDiscoverRunner` delegating to Django's `run_suite`/`get_test_runner_kwargs` so Django flags keep working.

## Python/Django Compatibility

- **Django 5.2**: Python 3.11–3.14
- **Django 6.0**: Python 3.12–3.14
- **Django 6.1**: Python 3.12–3.15

Keep this list in sync with `README.md`, `pyproject.toml` classifiers, and the CI matrix.

## Packaging / docs

- Packaging is managed via `pyproject.toml` (PEP 517/621 with setuptools).
- Version is defined in `rainbowtests/__init__.py` and read dynamically by setuptools.
- Record user-facing changes in `CHANGELOG.md`.
- Releases publish from bare semver tags (e.g. `0.8.0`) via PyPI trusted publishing, after CI passes.
- Keep documentation consistent with packaging metadata.
- Prefer Markdown for documentation.

## Safety & privacy

- Do not add secrets (API keys, tokens) to code, tests, docs, or CI.
- Do not print environment variables or filesystem paths that could contain sensitive info.
