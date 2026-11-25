# Changelog

## 0.8.0 (unreleased)

### ⚠️ Breaking
- Dropped Python 3.10 and Django 4.2.
- Removed `rainbowtests.test.simple.RainbowTestSuiteRunner`. It only raised `NotImplementedError`; use `rainbowtests.test.runner.RainbowDiscoverRunner`.
- Removed the empty `models.py`, `views.py` and `tests.py` stubs.

### ✨ Added
- Support for Django 6.0 and 6.1, and Python 3.15.
- Type hints, plus a `py.typed` marker.

### 🐛 Fixed
- `RainbowDiscoverRunner` now honors Django's `--buffer`, `--durations`, `--pdb` and `--debug-sql` flags, and logs the `--shuffle` seed. Previously these were ignored.
- The happy/sad message is now written to stderr, alongside unittest's output.

### 🔧 Internal
- 100% line + branch test coverage, enforced in CI across every supported Django/Python pair.
- ty type checking, `ruff format`, and a `Makefile`.
- PyPI publishing uses trusted publishing and runs only after CI passes.

## 0.7.0
- Modernized packaging (`pyproject.toml`, uv) for Python 3.10+ and Django 4.2 / 5.2.
