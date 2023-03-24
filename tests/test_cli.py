"""Tests for `bump_version` package."""

import bump_version.cli as cli
from click.testing import CliRunner, Result
from bump_version import __version__

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


def test_verbose_output():
    """
    Arrange/Act: Run the `version` subcommand with the '-v' flag.
    Assert: The output indicates verbose logging is enabled.
    """
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(cli.cli, ["-v", "version"])
    assert "Verbose" in result.output.strip(), "Verbose logging should be indicated in output."


def test_hello_displays_expected_message():
    """
    Arrange/Act: Run the `version` subcommand.
    Assert:  The output matches the library version.
    """
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(cli.cli, ["hello"])
    assert "bump-my-version" in result.output.strip(), "'Hello' messages should contain the CLI name."
