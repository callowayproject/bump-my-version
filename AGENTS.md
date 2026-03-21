# Agent instructions

This file provides guidance to AI Agents when working with code in this repository.

## Commands

```bash
# Install for development
uv sync --all-groups

# Run all tests
uv run pytest --agent-digest=term -p no:sugar

# Run a single test file
uv run pytest --agent-digest=term -p no:sugar tests/test_files.py

# Run a single test
uv run pytest --agent-digest=term -p no:sugar tests/test_files.py::test_function_name

# Lint and format
uv run ruff check bumpversion/
uv run ruff format bumpversion/

# Type checking
uv run mypy bumpversion/

# Check docstring coverage (must stay above 95%)
uv run interrogate bumpversion/

# Run pre-commit hooks on all files
pre-commit run --all-files
```

## Architecture

The tool works as a pipeline: read config → detect SCM state → parse current version → run setup hooks → calculate next version → build context → modify files → run pre-commit hooks → commit & tag → run post-commit hooks.

### Key modules

**`bumpversion/cli.py`** — Click-based CLI entry point. Commands: `bump`, `show`, `replace`, `sample-config`, `show-bump`. Routes to `bump.py` or `show.py` for logic.

**`bumpversion/bump.py`** — Core workflow: `get_next_version()` and `do_bump()`. Orchestrates config loading, file modification, and SCM operations.

**`bumpversion/config/`** — Pydantic 2.x models for configuration. `files.py` discovers and reads config from `pyproject.toml`, `.bumpversion.toml`, `setup.cfg`, etc. `models.py` defines `BumpVersionConfig` and `FileChange`.

**`bumpversion/versioning/`** — Version parsing and manipulation. `models.py` has `Version`, `VersionComponent`, `VersionComponentSpec`. `functions.py` has `NumericFunction`, `ValuesFunction`, `CalVerFunction`. `serialization.py` handles template-based version string rendering.

**`bumpversion/files.py`** — `ConfiguredFile` performs search/replace on individual files. `modify_files()` handles batches with dry-run support. Supports glob patterns, data files (JSON/YAML/TOML with key paths).

**`bumpversion/scm/`** — Git (`git.py`) and Mercurial (`hg.py`) backends. Reads current version from tags, creates commits and tags. Supports moveable tags and commit signing.

**`bumpversion/context.py`** — Builds the template context dict injected into version format strings (datetime, SCM info, environment variables).

**`bumpversion/hooks.py`** — Runs setup/pre-commit/post-commit shell hooks with version info as environment variables.

### Configuration model

Config flows from file (`.bumpversion.toml` or `[tool.bumpversion]` in `pyproject.toml`) → CLI overrides → resolved `BumpVersionConfig`. The `current_version` field is the source of truth; it's updated in-place in config files as part of each bump.

### Version components

Each part of a version (major, minor, patch) is a `VersionComponent` with a `VersionComponentSpec` describing its behavior (numeric increment, fixed values list, or CalVer expression). Components have dependency relationships — bumping a higher-order component resets dependent ones.

## Code style

- Line length: 119 characters
- Docstrings: Google style, required on all public symbols (95% coverage enforced by interrogate)
- Ruff with preview mode enabled; see `[tool.ruff.lint]` in `pyproject.toml` for full rule set
- Type annotations required on all function signatures
