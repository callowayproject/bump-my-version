import shutil
from pathlib import Path

from click.testing import Result

from bumpversion import cli
from tests.conftest import inside_dir


def test_show(tmp_path: Path, fixtures_path: Path, runner):
    """The show subcommand should list the parts of the configuration."""
    # Arrange
    config_path = tmp_path / "pyproject.toml"
    toml_path = fixtures_path / "basic_cfg.toml"
    shutil.copy(toml_path, config_path)

    with inside_dir(tmp_path):
        result: Result = runner.invoke(cli.cli, ["show", "current_version"])

    if result.exit_code != 0:
        print(result.output)
        print(result.exception)

    assert result.exit_code == 0
    assert result.output.splitlines(keepends=False) == ["1.0.0"]


def test_show_and_increment(tmp_path: Path, fixtures_path: Path, runner):
    """The show subcommand should increment the version and display it."""
    # Arrange
    config_path = tmp_path / "pyproject.toml"
    toml_path = fixtures_path / "basic_cfg.toml"
    shutil.copy(toml_path, config_path)

    with inside_dir(tmp_path):
        result: Result = runner.invoke(cli.cli, ["show", "new_version", "--increment", "minor"])

    if result.exit_code != 0:
        print(result.output)
        print(result.exception)

    assert result.exit_code == 0
    assert result.output.splitlines(keepends=False) == ["1.1.0-dev"]


def test_show_no_args(tmp_path: Path, fixtures_path: Path, runner):
    """The show subcommand should list the entire configuration."""
    # Arrange
    config_path = tmp_path / "pyproject.toml"
    toml_path = fixtures_path / "basic_cfg.toml"
    expected_output = fixtures_path.joinpath("basic_cfg_expected.yaml").read_text()

    shutil.copy(toml_path, config_path)

    with inside_dir(tmp_path):
        result: Result = runner.invoke(cli.cli, ["show", "--format", "yaml"])

    if result.exit_code != 0:
        print(result.output)
        print(result.exception)

    assert result.exit_code == 0
    assert result.output.strip() == expected_output.strip()


def test_show_increment_with_unparsable_version_is_a_clean_error(
    tmp_path: Path, fixtures_path: Path, runner
):
    """An unparsable current version should be a usage error, not a traceback."""
    # Arrange
    config_path = tmp_path / "pyproject.toml"
    toml_path = fixtures_path / "basic_cfg.toml"
    shutil.copy(toml_path, config_path)

    with inside_dir(tmp_path):
        result: Result = runner.invoke(
            cli.cli, ["show", "--increment", "patch", "--current-version", "garbage!!"]
        )

    assert result.exit_code == 2
    assert "garbage!!" in result.output
    assert "Traceback" not in result.output
