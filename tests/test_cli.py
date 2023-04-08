"""Tests for `bumpversion` package."""

from click.testing import CliRunner, Result

from bumpversion import __version__, cli
from tests.conftest import inside_dir

# To learn more about testing Click applications, visit the link below.
# https://click.palletsprojects.com/en/8.1.x/testing/


def test_version_displays_library_version():
    """
    Arrange/Act: Run the `version` subcommand.

    Assert: The output matches the library version.
    """
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(cli.cli, ["--version"])
    assert __version__ in result.output.strip(), "Version number should match library version."


def test_bump_no_configured_files(mocker, tmp_path):
    """
    Arrange/Act: Run the `bump` subcommand with --no-configured-files.

    Assert: There is no configured files specified to modify
    """
    mocked_do_bump = mocker.patch("bumpversion.cli.do_bump")
    runner: CliRunner = CliRunner()
    with inside_dir(tmp_path):
        result: Result = runner.invoke(
            cli.cli, ["bump", "--current-version", "1.0.0", "--no-configured-files", "patch"]
        )

    if result.exit_code != 0:
        print(result.output)

    assert result.exit_code == 0

    call_args = mocked_do_bump.call_args[0]
    assert len(call_args[2].files) == 0


def test_no_configured_files_still_file_args_work(mocker, tmp_path):
    mocked_do_bump = mocker.patch("bumpversion.cli.do_bump")
    runner: CliRunner = CliRunner()
    with inside_dir(tmp_path):
        result: Result = runner.invoke(
            cli.cli, ["bump", "--current-version", "1.0.0", "--no-configured-files", "patch", "do-this-file.txt"]
        )

    if result.exit_code != 0:
        print(result.output)

    assert result.exit_code == 0

    call_args = mocked_do_bump.call_args[0]
    assert len(call_args[2].files) == 1
    assert call_args[2].files[0].filename == "do-this-file.txt"
