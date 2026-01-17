# Modernization Plan (Packaging + uv + Django/Python)

## Scope / goals

We will implement a modernization of `django-rainbowtests` to:

1. Migrate packaging to **`pyproject.toml`** (remove/replace `setup.py`).
2. Manage dependencies and dev workflows using **uv**.
3. Support **exactly** these Python versions: **3.10, 3.11, 3.12, 3.13, 3.14**.
4. Target **Django 4.2, 5.2, 6.0**.
5. Adopt **`rich`** for terminal color output and remove dependency on `django.utils.termcolors`.
6. Add **django-project-agnostic** tests using **pytest** in a repo-root `tests/` directory.
7. Add **GitHub Actions** CI to run the test suite across all supported Python/Django versions.
8. Update docs (`README.md`, `AGENTS.md`, etc.) to match the new reality.

## Current repository state (findings)

### Packaging

- Uses `setup.py` + `MANIFEST.in`.
- `setup.py` currently:
  - `install_requires=['django']` (unversioned).
  - Classifiers still include Python 2.x and Python 3.4.
  - Reads long description from `README.md`.
- `MANIFEST.in` includes `README.md` + `LICENSE.md`.

### Code / Django integration

- Primary runner: `rainbowtests/test/runner.py` with `RainbowDiscoverRunner(DiscoverRunner)`.
  - Overrides `run_suite` and sets `runner.resultclass = RainbowTextTestResult`.
  - Uses `settings.RAINBOWTESTS_SHOW_MESSAGES`.
  - Coverage runner uses `coverage.coverage()`.
- Legacy runner: `rainbowtests/test/simple.py` imports `django.test.simple.DjangoTestSuiteRunner` (removed long ago; incompatible with Django 4.2+).
- Color styles rely on `django.utils.termcolors.make_style`.
- There is effectively **no real automated test suite** in-repo (`rainbowtests/tests.py` is empty; no pytest/tox/CI config).

### Docs

- `README.md` still documents Django 1.4–1.8 + Python 2.7 / 3.4.
- `AGENTS.md` exists but currently describes pip/venv-based dev workflow, not uv.

## Key design decisions to make (before implementation)

1. **Build backend**: Use `setuptools` via PEP 517/621 (simplest migration, minimal behavior change).
2. **Version source**: Keep `rainbowtests.__version__` as the single source of truth and configure setuptools dynamic version from that attribute.
3. **Supported Python versions**: We support *exactly* 3.10–3.14; packaging will express this as a bounded range (e.g. `>=3.10,<3.15`) plus explicit trove classifiers, while CI enforces the exact matrix.
4. **Supported Django versions**: We will explicitly support 4.2 LTS, 5.2 (LTS), and 6.0.
   - Practical note: depending on today’s ecosystem, Django 6.0 may be prerelease/not available on PyPI yet; plan CI to optionally test prereleases.
5. **Color output implementation**: Adopt `rich` for styling and remove usage of `django.utils.termcolors`.
   - Maintain the existing public API shape in `rainbowtests/colors.py` as much as practical (callables like `green("text")`).
6. **Legacy runner removal**: `RainbowTestSuiteRunner` (Django <1.8) should be removed (or gated behind a safe import + clear error), because the project will officially support only Django 4.2+.
7. **Test strategy**: Add django-project-agnostic unit tests (no external Django project) validating:
   - resultclass injection works
   - colored dot output for success/error/failure
   - traceback highlighting behavior
   - `colors.*` functions return styled output (ANSI sequences) via rich

## Implementation plan (phased)

### Phase 0 — Baseline + safety net

- Add a pytest-based test harness in a repo-root `tests/` directory.
  - Keep it **django-project-agnostic**: tests should not require a separate Django project checkout.
  - It is acceptable (and expected) that tests install Django itself; the goal is to avoid needing an app/project scaffold.
  - Use minimal settings configuration inside tests (e.g., `django.conf.settings.configure(...)` when needed).
  - Prefer unit tests around `RainbowTextTestResult` + the runner wiring rather than full integration tests.

- Add GitHub Actions CI to run the test suite across the supported matrix:
  - Python: 3.10, 3.11, 3.12, 3.13, 3.14
  - Django: 4.2, 5.2, 6.0
  - If Django 6.0 is not released yet, install with prereleases enabled (e.g. `uv pip install --pre`) and/or split into an “experimental” job until stable.
  - If Python 3.14 is not available on GitHub Actions yet, use the appropriate setup-python prerelease channel and treat it similarly (tracked/optional) until GA.

- Run everything via uv in CI:
  - `uv sync --group test`
  - `uv run pytest`

Acceptance criteria:
- `uv run pytest` works locally.
- CI reproduces local runs for all stable versions in the matrix.

### Phase 1 — Migrate packaging to `pyproject.toml`

- Create `pyproject.toml` with:
  - `[build-system]` using `setuptools`.
  - `[project]` metadata (name, description, readme, license, authors, urls).
  - `requires-python` expressing our explicit support window (e.g. `">=3.10,<3.15"`).
  - Dependencies:
    - `Django>=4.2` (and likely `<7` to avoid unknown future breakages).
    - `rich` (for terminal color output)
  - Classifiers updated to Python 3.10–3.14 and supported Django versions.
  - Configure package discovery for `rainbowtests`.
  - Configure version as dynamic from `rainbowtests.__version__`.
- Remove or greatly simplify `setup.py` (eventually delete once packaging is stable).
- Ensure sdists/wheels include README/LICENSE as desired (verify with `python -m build` in CI).

Acceptance criteria:
- `python -m build` produces sdist/wheel.
- `pip install dist/*.whl` works.

### Phase 2 — Adopt uv for dependency management

- Standardize dev workflow around uv:
  - `uv sync` for dev environment creation.
  - `uv run python -m ...` for commands.
- Add dependency groups (PEP 735 style) in `pyproject.toml` (uv-supported), e.g.:
  - `dependency-groups.dev`: tooling (ruff, mypy optional)
  - `dependency-groups.test`: pytest, coverage (and any small pytest helpers as needed)
- Generate and commit `uv.lock`.
- Document common commands in README/AGENTS.

Acceptance criteria:
- Fresh checkout: `uv sync` + `uv run pytest` works.

### Phase 3 — Modernize code for Django 4.2+ / Python 3.10–3.14

Focus areas:

1. **Remove obsolete Django runner**:
   - Delete `rainbowtests/test/simple.py` OR keep it but make it inert on modern Django:
     - wrap import in `try/except ImportError` and raise a clear message if used.
   - Update README to remove all references to `RainbowTestSuiteRunner`.

2. **Audit `DiscoverRunner` integration**:
   - Confirm `run_suite` override still matches Django 4.2/5.2/6.0 expectations.
   - Confirm `unittest.TextTestRunner` usage still works with Django’s runner plumbing.
   - Consider overriding `get_resultclass()` or `get_test_runner_kwargs()` if Django provides cleaner hooks in modern versions.

3. **Coverage support**:
   - Update `RainbowDiscoverCoverageRunner` to use modern `coverage.Coverage()` API.
   - Consider moving coverage integration to docs (recommended modern workflow is `coverage run -m pytest` / `coverage run manage.py test`), and potentially deprecate the custom coverage runner.

4. **Color utilities (switch to rich)**:
   - Replace `django.utils.termcolors` usage with `rich`.
   - Keep `rainbowtests/colors.py` API stable (e.g., `colors.red("text") -> str`) by using rich to generate ANSI-colored strings.
     - Likely approach: render a `rich.text.Text` with a `rich.console.Console(force_terminal=True, file=io.StringIO())` and return the captured string.
   - Ensure behavior remains reasonable when output is not a TTY (either always emit ANSI, or make it configurable; decide and document).

5. **General Python modernization** (optional but recommended once tests exist):
   - Remove Python 2-era comments and encoding headers.
   - Use `super()` without args.
   - Use f-strings where it improves readability.

Acceptance criteria:
- Tests pass on Django 4.2 + 5.2.
- Django 6.0 tests pass (or are at least tracked) once available.

### Phase 4 — Documentation updates

- Update `README.md`:
  - Compatibility section to: Python 3.10/3.11/3.12/3.13/3.14; Django 4.2/5.2/6.0.
  - Remove legacy Django <1.8 guidance.
  - Provide modern installation examples (`pip install ...` and optionally `uv add django-rainbowtests`).
  - Document settings:
    - `RAINBOWTESTS_HIGHLIGHT_PATH`
    - `RAINBOWTESTS_SHOW_MESSAGES`
  - Add a “Development” section referencing uv.

- Update `AGENTS.md`:
  - Replace venv/pip steps with uv-first workflow.
  - Add the standard commands to run tests/linters using `uv run`.

Acceptance criteria:
- Docs do not mention unsupported Python/Django versions.
- Quickstart is accurate for both consumers and contributors.

## Deliverables (files likely to change)

- Add: `pyproject.toml`, `uv.lock`, `tests/`, CI workflow under `.github/workflows/`.
- Modify: `README.md`, `AGENTS.md`, `MANIFEST.in` (if needed), package code under `rainbowtests/test/`.
- Remove: `setup.py` (eventually), `rainbowtests/test/simple.py` (or deprecate/guard it).

## Open questions / risks

- Django 6.0 availability and installation constraints (may require prerelease installs for a while).
- Python 3.14 availability on GitHub Actions / wheels for dependencies (may require prerelease interpreters initially).
- Rich/ANSI behavior differences across terminals and non-TTY output (ensure deterministic tests).
- Whether Django’s internal runner APIs changed enough that overriding `run_suite` is brittle; tests across versions will surface this early.
    - Ideally our pytest test suite would capture this.
