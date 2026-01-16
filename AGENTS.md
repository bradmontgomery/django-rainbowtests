# AI Agent Guidelines (AGENTS.md)

This repository is a small Django test-runner package intended to make test output more human-friendly by highlighting the most relevant portions of tracebacks and messages.

## Goals

- Prefer small, focused changes.
- Preserve existing behavior unless the task explicitly requires a behavior change.
- Keep the library usable as a drop-in Django `TEST_RUNNER`.

## Local setup

- Use a virtual environment.
- Install in editable mode for development:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .
```

- Install Django appropriate to the change you’re making (this project historically targeted older Django, but modernization work may change that).

## How to validate changes

- Run any existing test/lint commands already present in the repo.
- At minimum, ensure the code still imports and compiles:

```bash
python -m compileall rainbowtests setup.py
```

- If you have a sample Django project handy, validate integration by setting:

```python
TEST_RUNNER = 'rainbowtests.test.runner.RainbowDiscoverRunner'
```

…and running `python manage.py test`.

## Code & style conventions

- Do not do repo-wide reformatting unless explicitly requested.
- Avoid adding new dependencies for minor changes.
- Keep color/output behavior changes isolated to the existing modules (`rainbowtests/colors.py`, `rainbowtests/messages.py`, and `rainbowtests/test/*`) when possible.

## Packaging / docs

- Keep packaging metadata consistent with documentation files in the repo root (e.g., `README.md`, `LICENSE.md`).
- Prefer Markdown for documentation.

## Safety & privacy

- Do not add secrets (API keys, tokens) to code, tests, docs, or CI.
- Do not print environment variables or filesystem paths that could contain sensitive info.
