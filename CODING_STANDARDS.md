# Coding Standards

Rules for code in this repository. Tooling config in `pyproject.toml` is authoritative; this file summarises it. Run everything through `uv run`.

## Style

- Python 3.9+ compatible; line length 120; format with `uv run ruff format`.
- Lint with `uv run ruff check` (preview mode). Don't add `# noqa` without a reason in the same comment.
- Type annotations on every function signature; `uv run mypy bumpversion/` must pass.
- Imports used only for typing go under `if TYPE_CHECKING:` (ruff `TCH`).
- Keep functions simple (McCabe `C90`); prefer early returns over deep nesting.
- No bare `except`; catch the narrowest exception and chain with `raise ... from`.
- Pydantic 2.x models for configuration; don't hand-roll validation that a model can do.

## Docstrings

- Google style, required on all public modules, classes, functions and methods (`interrogate` fail-under 95).
- One-line summary in present tense ending with a period.
- Tests are exempt from `pydoclint`.

## Tests

- pytest, under `tests/`, mirroring the `bumpversion/` layout.
- Arrange / Act / Assert; one behaviour per test; names say what and why.
- Prefer `tmp_path` and fixtures over hand-made temp files; parametrize instead of copy-pasting; mock only external boundaries (subprocess, SCM, clock).
- Bug fixes start with a failing regression test.

## Pre-commit gate

```bash
uv run ruff check bumpversion/ && uv run ruff format bumpversion/
uv run mypy bumpversion/
uv run interrogate bumpversion/
uv run pytest --agent-digest=term -p no:sugar
```

## Topic guidance

Detailed, task-specific guidance lives in [docs/agents/python/](docs/agents/python/). Load only the file that matches the task; the repo rules above win on conflict.

| When you are... | Read |
| ----------------- | ------ |
| Writing or reviewing docstrings | [writing-python-docstrings.md](docs/agents/python/writing-python-docstrings.md) |
| Doing TDD / naming tests | [tdd-best-practices.md](docs/agents/python/tdd-best-practices.md) |
| Writing any pytest test (index of patterns) | [SKILL.md](docs/agents/python/SKILL.md) |
| Setting up fixtures / `conftest.py` | [custom-fixtures-and-conftest.md](docs/agents/python/custom-fixtures-and-conftest.md), [fixtures-for-setup-or-teardown.md](docs/agents/python/fixtures-for-setup-or-teardown.md) |
| Parametrizing tests | [parameterized-tests.md](docs/agents/python/parameterized-tests.md) |
| Mocking | [mocking.md](docs/agents/python/mocking.md) |
| Asserting exceptions | [testing-exceptions.md](docs/agents/python/testing-exceptions.md) |
| Touching the filesystem in tests | [temporary-files-and-dirs.md](docs/agents/python/temporary-files-and-dirs.md) |
| Testing async code | [testing-async-code.md](docs/agents/python/testing-async-code.md) |

To add guidance: drop a markdown file in `docs/agents/python/` and add one row to the table above.
