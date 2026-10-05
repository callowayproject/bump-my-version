"""Tests the check command."""

from pathlib import Path

from click.testing import Result

from bumpversion import cli
from tests.conftest import inside_dir

CONFIG = """
[tool.bumpversion]
current_version = "1.2.3"

[[tool.bumpversion.files]]
filename = "VERSION"
"""


def test_check_passes_when_consistent(tmp_path: Path, runner):
    """The check subcommand exits successfully when every file contains the current version."""
    # Arrange
    (tmp_path / ".bumpversion.toml").write_text(CONFIG)
    (tmp_path / "VERSION").write_text("1.2.3\n")

    # Act
    with inside_dir(tmp_path):
        result: Result = runner.invoke(cli.cli, ["check"])

    # Assert
    assert result.exit_code == 0, result.output
    assert "1.2.3 is consistent" in result.output


def test_check_fails_on_stale_file(tmp_path: Path, runner):
    """The check subcommand exits with 1 and names the file that was not bumped."""
    # Arrange
    (tmp_path / ".bumpversion.toml").write_text(CONFIG)
    (tmp_path / "VERSION").write_text("1.2.2\n")

    # Act
    with inside_dir(tmp_path):
        result: Result = runner.invoke(cli.cli, ["check"])

    # Assert
    assert result.exit_code == 1
    assert "VERSION" in result.output


def test_check_release_tag(tmp_path: Path, runner):
    """The --release-tag option fails the check unless it matches the current version."""
    # Arrange
    (tmp_path / ".bumpversion.toml").write_text(CONFIG)
    (tmp_path / "VERSION").write_text("1.2.3\n")

    # Act
    with inside_dir(tmp_path):
        matching: Result = runner.invoke(cli.cli, ["check", "--release-tag", "v1.2.3"])
        mismatching: Result = runner.invoke(cli.cli, ["check", "--release-tag", "v1.2.2"])

    # Assert
    assert matching.exit_code == 0, matching.output
    assert mismatching.exit_code == 1
    assert "v1.2.2" in mismatching.output


def test_check_current_version_option(tmp_path: Path, runner):
    """The --current-version option overrides the configured version."""
    # Arrange
    (tmp_path / ".bumpversion.toml").write_text(CONFIG)
    (tmp_path / "VERSION").write_text("1.2.4\n")

    # Act
    with inside_dir(tmp_path):
        result: Result = runner.invoke(cli.cli, ["check", "--current-version", "1.2.4"])

    # Assert
    assert result.exit_code == 0, result.output


def test_keep_replacement_is_checked_but_not_bumped(tmp_path: Path, runner):
    """A file configuration replacing with `\\g<0>` is left alone by bump, but its pattern is still required."""
    # Arrange
    (tmp_path / ".bumpversion.toml").write_text(
        CONFIG
        + """
[[tool.bumpversion.files]]
filename = "CHANGELOG.md"
search = "^## {current_version} \\\\(\\\\d{{4}}-\\\\d{{2}}-\\\\d{{2}}\\\\)"
replace = "\\\\g<0>"
regex = true
"""
    )
    (tmp_path / "VERSION").write_text("1.2.3\n")
    changelog = "## 1.2.3 (2026-10-05)\n- fix\n"
    (tmp_path / "CHANGELOG.md").write_text(changelog)

    # Act
    with inside_dir(tmp_path):
        check_before: Result = runner.invoke(cli.cli, ["check"])
        bump: Result = runner.invoke(cli.cli, ["bump", "patch", "--no-commit", "--no-tag"])
        check_after: Result = runner.invoke(cli.cli, ["check"])

    # Assert
    assert check_before.exit_code == 0, check_before.output
    assert bump.exit_code == 0, bump.output
    assert (tmp_path / "VERSION").read_text() == "1.2.4\n"
    assert (tmp_path / "CHANGELOG.md").read_text() == changelog
    assert check_after.exit_code == 1
    assert "CHANGELOG.md" in check_after.output
