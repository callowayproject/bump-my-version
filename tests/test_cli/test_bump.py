"""Tests the bump CLI subcommand."""

import shutil
import subprocess
import traceback
from datetime import datetime
from pathlib import Path

import pytest
from pytest import param

from click.testing import CliRunner, Result

from bumpversion import cli
from tests.conftest import inside_dir


class TestNoConfiguredFilesOption:
    """Tests around the behavior of the --no-configured-files option."""

    def test_no_files_marked_to_modify(self, mocker, tmp_path: Path):
        """
        No files are sent to the `do_bump` function if the --no-configured-files option is used.
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
        passed_config = call_args[2]
        assert len(passed_config.files) == 0

    def test_file_args_marked_to_modify(self, mocker, tmp_path: Path):
        """File paths marked in the command-line arguments are sent to the `do_bump` function."""
        mocked_do_bump = mocker.patch("bumpversion.cli.do_bump")
        runner: CliRunner = CliRunner()
        with inside_dir(tmp_path):
            result: Result = runner.invoke(
                cli.cli,
                ["bump", "--current-version", "1.0.0", "--no-configured-files", "patch", "do-this-file.txt"],
            )

        if result.exit_code != 0:
            print(result.output)

        assert result.exit_code == 0

        call_args = mocked_do_bump.call_args[0]
        passed_config = call_args[2]
        assert len(passed_config.files) == 1
        assert passed_config.files[0].filename == "do-this-file.txt"


def test_bump_nested_regex(tmp_path: Path, fixtures_path: Path, caplog):
    """
    Arrange/Act: Run the `bump` subcommand with --no-configured-files.

    Assert: There is no configured files specified to modify
    """
    cff_path = tmp_path / "citation.cff"
    cff_path.write_text("cff-version: 1.2.0\ndate-released: 2023-09-19\n")
    content = fixtures_path.joinpath("regex_test_config.toml").read_text()
    config_path = tmp_path / ".bumpversion.toml"
    config_path.write_text(content)

    runner: CliRunner = CliRunner()
    with inside_dir(tmp_path):
        result: Result = runner.invoke(cli.cli, ["bump", "-vv", "patch"])

    if result.exit_code != 0:
        print(result.output)
        print(caplog.text)

    assert result.exit_code == 0

    now = datetime.now().isoformat()[:10]
    assert cff_path.read_text() == f"cff-version: 1.2.0\ndate-released: {now}\n"


def test_missing_explicit_config_file(tmp_path: Path):
    """The command-line processor should raise an exception if the config file is missing."""
    with inside_dir(tmp_path):
        runner: CliRunner = CliRunner()
        with inside_dir(tmp_path):
            result: Result = runner.invoke(cli.cli, ["bump", "--config-file", "missing-file.cfg"])
        assert result.exit_code != 0
        assert "'missing-file.cfg' does not exist." in result.output


def test_cli_options_override_config(tmp_path: Path, fixtures_path: Path, mocker):
    """The command-line processor should override the config file."""
    # Arrange
    config_path = tmp_path / "this_config.toml"
    fixture_toml = fixtures_path / "basic_cfg.toml"
    shutil.copy(fixture_toml, config_path)
    runner: CliRunner = CliRunner()
    mocked_do_bump = mocker.patch("bumpversion.cli.do_bump")

    # Act
    with inside_dir(tmp_path):
        result: Result = runner.invoke(
            cli.cli,
            [
                "bump",
                "--config-file",
                str(config_path),
                "--current-version",
                "1.1.0",
                "--new-version",
                "1.2.0",
                "--allow-dirty",
                "--parse",
                r"XXX(?P<spam>\d+);(?P<blob>\d+);(?P<slurp>\d+)",
                "--serialize",
                "XXX{spam};{blob};{slurp}",
                "--search",
                "my-search",
                "--replace",
                "my-replace",
                "--no-commit",
                "--no-tag",
                "slurp",
                "do-this-file.txt",
            ],
        )

    # Assert
    assert result.exit_code == 0
    assert mocked_do_bump.call_count == 1
    assert mocked_do_bump.call_args[0][0] == "slurp"
    assert mocked_do_bump.call_args[0][1] == "1.2.0"
    the_config = mocked_do_bump.call_args[0][2]
    assert the_config.current_version == "1.1.0"
    assert the_config.allow_dirty
    assert the_config.parse == r"XXX(?P<spam>\d+);(?P<blob>\d+);(?P<slurp>\d+)"
    assert the_config.serialize == ("XXX{spam};{blob};{slurp}",)
    assert the_config.search == "my-search"
    assert the_config.replace == "my-replace"
    assert the_config.commit is False
    assert the_config.tag is False
    assert len(the_config.files) == 4
    assert {f.filename for f in the_config.files} == {
        "setup.py",
        "bumpversion/__init__.py",
        "CHANGELOG.md",
        "do-this-file.txt",
    }
    assert mocked_do_bump.call_args[0][3] == config_path


@pytest.mark.parametrize(
    ["repo", "scm_command"],
    [
        param("git_repo", "git", id="git"),
        param("hg_repo", "hg", id="hg"),
    ],
)
def test_dirty_work_dir_raises_error(repo: str, scm_command: str, request):
    repo_path: Path = request.getfixturevalue(repo)
    with inside_dir(repo_path):
        # Arrange
        repo_path.joinpath("dirty2").write_text("i'm dirty! 1.1.1")
        subprocess.run([scm_command, "add", "dirty2"], check=True)
        runner: CliRunner = CliRunner()

        # Act
        result: Result = runner.invoke(
            cli.cli, ["bump", "patch", "--current-version", "1.1.1", "--no-allow-dirty", "dirty2"]
        )

    # Assert
    assert result.exit_code != 0
    assert "working directory is not clean" in result.output


def test_non_scm_operations_if_scm_not_installed(tmp_path: Path, monkeypatch):
    """Everything works except SCM commands if the SCM is unusable."""
    # Arrange
    monkeypatch.setenv("PATH", "")

    with inside_dir(tmp_path):
        version_path = tmp_path / "VERSION"
        version_path.write_text("31.0.3")

        runner: CliRunner = CliRunner()

        # Act
        runner.invoke(cli.cli, ["bump", "major", "--current-version", "31.0.3", "VERSION"])

    # Assert
    assert version_path.read_text() == "32.0.0"


@pytest.mark.parametrize(
    ["version_part"],
    [
        param("charlie", id="bad_version_part"),
        param("", id="missing_version_part"),
    ],
)
def test_detects_bad_or_missing_version_part(version_part: str, tmp_path: Path, monkeypatch):
    """It properly detects bad or missing version part."""
    # Arrange
    monkeypatch.setenv("PATH", "")

    with inside_dir(tmp_path):
        version_path = tmp_path / "VERSION"
        version_path.write_text("31.0.3")

        runner: CliRunner = CliRunner()
        args = ["bump", "--current-version", "31.0.3"]
        if version_part:
            args.append(version_part)
        args.append("VERSION")
        # Act
        result = runner.invoke(cli.cli, args)

    # Assert
    assert result.exception is not None
    assert "Unknown version part:" in result.stdout


def test_ignores_missing_files_with_option(tmp_path, fixtures_path):
    """The replace subcommand should ignore missing."""

    config_file = tmp_path / ".bumpversion.toml"
    config_file.write_text(
        "[tool.bumpversion]\n"
        'current_version = "0.0.1"\n'
        "allow_dirty = true\n\n"
        "[[tool.bumpversion.files]]\n"
        'filename = "VERSION"\n'
        "regex = false\n"
    )

    # Act
    runner: CliRunner = CliRunner()
    with inside_dir(tmp_path):
        result: Result = runner.invoke(
            cli.cli,
            [
                "bump",
                "--verbose",
                "--no-regex",
                "--no-configured-files",
                "--ignore-missing-files",
                "minor",
                "VERSION",
            ],
        )

    # Assert
    if result.exit_code != 0:
        print("Here is the output:")
        print(result.output)
        print(traceback.print_exception(result.exc_info[1]))

    assert result.exit_code == 0
