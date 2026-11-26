.PHONY: install test lint format typecheck check build clean

install:  ## Install all dependency groups from the lockfile
	uv sync --locked --all-groups

test:  ## Run tests (fails under 100% line+branch coverage)
	uv run pytest

lint:  ## Lint and check formatting
	uv run ruff check .
	uv run ruff format --check .

format:  ## Auto-fix lint issues and format
	uv run ruff check --fix .
	uv run ruff format .

typecheck:  ## Type check with ty
	uv run ty check

check: lint typecheck test  ## Everything CI runs

build:  ## Build sdist and wheel into dist/
	uv build

clean:
	rm -rf build dist *.egg-info .coverage htmlcov coverage.xml .pytest_cache .ruff_cache
