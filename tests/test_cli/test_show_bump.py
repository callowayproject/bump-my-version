"""Tests the show_bump command."""

import shutil
from pathlib import Path

from click.testing import CliRunner, Result
from bumpversion import cli
from tests.conftest import inside_dir


def test_show_bump_uses_current_version(tmp_path: Path, fixtures_path: Path):
    """The show_bump subcommand should list the parts of the configuration."""
    # Arrange
    config_path = tmp_path / "pyproject.toml"
    toml_path = fixtures_path / "basic_cfg.toml"
    shutil.copy(toml_path, config_path)
    runner: CliRunner = CliRunner()

    with inside_dir(tmp_path):
        result: Result = runner.invoke(cli.cli, ["show-bump"])

    if result.exit_code != 0:
        print(result.output)
        print(result.exception)

    assert result.exit_code == 0
    assert result.output == "\n".join(
        [
            "1.0.0 ── bump ─┬─ major ─── 2.0.0-dev",
            "               ├─ minor ─── 1.1.0-dev",
            "               ├─ patch ─── 1.0.1-dev",
            "               ╰─ release ─ invalid: The part has already the maximum value among "
            "['dev', 'gamma'] and cannot be bumped.\n",
        ]
    )


def test_show_bump_uses_passed_version(tmp_path: Path, fixtures_path: Path):
    """The show_bump subcommand should list the parts of the configuration."""
    # Arrange
    config_path = tmp_path / "pyproject.toml"
    toml_path = fixtures_path / "basic_cfg.toml"
    shutil.copy(toml_path, config_path)
    runner: CliRunner = CliRunner()

    with inside_dir(tmp_path):
        result: Result = runner.invoke(cli.cli, ["show-bump", "1.2.3"])

    if result.exit_code != 0:
        print(result.output)
        print(result.exception)

    assert result.exit_code == 0
    assert result.output == "\n".join(
        [
            "1.2.3 ── bump ─┬─ major ─── 2.0.0-dev",
            "               ├─ minor ─── 1.3.0-dev",
            "               ├─ patch ─── 1.2.4-dev",
            "               ╰─ release ─ invalid: The part has already the maximum value among ['dev', 'gamma'] "
            "and cannot be bumped.\n",
        ]
    )
