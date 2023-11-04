"""Tests for `bumpversion` package."""
import shutil
import subprocess
import traceback
from pathlib import Path

import pytest
from click.testing import CliRunner, Result
from pytest import param

from bumpversion import __version__, cli
from tests.conftest import inside_dir


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


def test_bump_legacy(mocker, tmp_path):
    """
    Arrange/Act: Run the `bump` subcommand with --no-configured-files.

    Assert: There is no configured files specified to modify
    """
    mocked_do_bump = mocker.patch("bumpversion.cli.do_bump")
    runner: CliRunner = CliRunner()
    with inside_dir(tmp_path):
        result: Result = runner.invoke(cli.cli, ["--current-version", "1.0.0", "--no-configured-files", "patch"])

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
    assert the_config.serialize == ["XXX{spam};{blob};{slurp}"]
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


def test_listing_with_version_part(tmp_path: Path, fixtures_path: Path):
    """The --list option should list the configuration with new_version."""
    # Arrange
    config_path = tmp_path / "pyproject.toml"
    toml_path = fixtures_path / "basic_cfg.toml"
    shutil.copy(toml_path, config_path)
    runner: CliRunner = CliRunner()

    with inside_dir(tmp_path):
        result: Result = runner.invoke(cli.cli, ["bump", "--list", "patch"])

    if result.exit_code != 0:
        print(result.output)
        print(result.exception)

    assert result.exit_code == 0
    assert set(result.output.splitlines(keepends=False)) == {
        "WARNING:",
        "",
        "DEPRECATED: The --list option is deprecated and will be removed in a future version.",
        "new_version=1.0.1-dev",
        "current_version=1.0.0",
        "excluded_paths=[]",
        "parse=(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+)(\\-(?P<release>[a-z]+))?",
        "serialize=['{major}.{minor}.{patch}-{release}', '{major}.{minor}.{patch}']",
        "search={current_version}",
        "replace={new_version}",
        "regex=False",
        "ignore_missing_version=False",
        "included_paths=[]",
        "tag=True",
        "sign_tags=False",
        "tag_name=v{new_version}",
        "tag_message=Bump version: {current_version} → {new_version}",
        "allow_dirty=False",
        "commit=True",
        "message=Bump version: {current_version} → {new_version}",
        "commit_args=None",
        (
            "files=["
            "{'filename': 'setup.py', 'glob': None, 'parse': "
            "'(?P<major>\\\\d+)\\\\.(?P<minor>\\\\d+)\\\\.(?P<patch>\\\\d+)(\\\\-(?P<release>[a-z]+))?', 'serialize': "
            "['{major}.{minor}.{patch}-{release}', '{major}.{minor}.{patch}'], 'search': '{current_version}', "
            "'replace': '{new_version}', 'regex': False, 'ignore_missing_version': False}, "
            "{'filename': 'bumpversion/__init__.py', 'glob': None, 'parse': "
            "'(?P<major>\\\\d+)\\\\.(?P<minor>\\\\d+)\\\\.(?P<patch>\\\\d+)(\\\\-(?P<release>[a-z]+))?', 'serialize': "
            "['{major}.{minor}.{patch}-{release}', '{major}.{minor}.{patch}'], 'search': '{current_version}', "
            "'replace': '{new_version}', 'regex': False, 'ignore_missing_version': False}, "
            "{'filename': 'CHANGELOG.md', 'glob': None, 'parse': "
            "'(?P<major>\\\\d+)\\\\.(?P<minor>\\\\d+)\\\\.(?P<patch>\\\\d+)(\\\\-(?P<release>[a-z]+))?', 'serialize': "
            "['{major}.{minor}.{patch}-{release}', '{major}.{minor}.{patch}'], 'search': '**unreleased**', "
            "'replace': '**unreleased**\\n**v{new_version}**', 'regex': False, 'ignore_missing_version': False}]"
        ),
    }


def test_listing_without_version_part(tmp_path: Path, fixtures_path: Path):
    """The --list option should list the configuration without new_version."""
    # Arrange
    config_path = tmp_path / "pyproject.toml"
    toml_path = fixtures_path / "basic_cfg.toml"
    shutil.copy(toml_path, config_path)
    runner: CliRunner = CliRunner()

    with inside_dir(tmp_path):
        result: Result = runner.invoke(cli.cli, ["bump", "--list"])

    if result.exit_code != 0:
        print(result.output)
        print(result.exception)

    assert result.exit_code == 0
    assert set(result.output.splitlines(keepends=False)) == {
        "WARNING:",
        "",
        "DEPRECATED: The --list option is deprecated and will be removed in a future version.",
        "current_version=1.0.0",
        "excluded_paths=[]",
        "parse=(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+)(\\-(?P<release>[a-z]+))?",
        "serialize=['{major}.{minor}.{patch}-{release}', '{major}.{minor}.{patch}']",
        "search={current_version}",
        "replace={new_version}",
        "regex=False",
        "ignore_missing_version=False",
        "included_paths=[]",
        "tag=True",
        "sign_tags=False",
        "tag_name=v{new_version}",
        "tag_message=Bump version: {current_version} → {new_version}",
        "allow_dirty=False",
        "commit=True",
        "message=Bump version: {current_version} → {new_version}",
        "commit_args=None",
        (
            "files=["
            "{'filename': 'setup.py', 'glob': None, 'parse': "
            "'(?P<major>\\\\d+)\\\\.(?P<minor>\\\\d+)\\\\.(?P<patch>\\\\d+)(\\\\-(?P<release>[a-z]+))?', 'serialize': "
            "['{major}.{minor}.{patch}-{release}', '{major}.{minor}.{patch}'], 'search': '{current_version}', "
            "'replace': '{new_version}', 'regex': False, 'ignore_missing_version': False}, "
            "{'filename': 'bumpversion/__init__.py', 'glob': None, 'parse': "
            "'(?P<major>\\\\d+)\\\\.(?P<minor>\\\\d+)\\\\.(?P<patch>\\\\d+)(\\\\-(?P<release>[a-z]+))?', 'serialize': "
            "['{major}.{minor}.{patch}-{release}', '{major}.{minor}.{patch}'], 'search': '{current_version}', "
            "'replace': '{new_version}', 'regex': False, 'ignore_missing_version': False}, "
            "{'filename': 'CHANGELOG.md', 'glob': None, 'parse': "
            "'(?P<major>\\\\d+)\\\\.(?P<minor>\\\\d+)\\\\.(?P<patch>\\\\d+)(\\\\-(?P<release>[a-z]+))?', 'serialize': "
            "['{major}.{minor}.{patch}-{release}', '{major}.{minor}.{patch}'], 'search': '**unreleased**', "
            "'replace': '**unreleased**\\n**v{new_version}**', 'regex': False, 'ignore_missing_version': False}]"
        ),
    }


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


def test_show(tmp_path: Path, fixtures_path: Path):
    """The show subcommand should list the parts of the configuration."""
    # Arrange
    config_path = tmp_path / "pyproject.toml"
    toml_path = fixtures_path / "basic_cfg.toml"
    shutil.copy(toml_path, config_path)
    runner: CliRunner = CliRunner()

    with inside_dir(tmp_path):
        result: Result = runner.invoke(cli.cli, ["show", "current_version"])

    if result.exit_code != 0:
        print(result.output)
        print(result.exception)

    assert result.exit_code == 0
    assert result.output.splitlines(keepends=False) == ["1.0.0"]


def test_major(tmp_path: Path):
    """The major subcommand should bump the given value to the next major version."""
    # Arrange
    runner: CliRunner = CliRunner()

    with inside_dir(tmp_path):
        result: Result = runner.invoke(cli.cli, ["major", "v0.1.2"])

    if result.exit_code != 0:
        print(result.output)
        print(result.exception)

    assert result.exit_code == 0
    assert result.output.splitlines(keepends=False) == ["1.0.0"]


def test_minor(tmp_path: Path):
    """The minor subcommand should bump the given value to the next minor version."""
    # Arrange
    runner: CliRunner = CliRunner()

    with inside_dir(tmp_path):
        result: Result = runner.invoke(cli.cli, ["minor", "v0.0.2"])

    if result.exit_code != 0:
        print(result.output)
        print(result.exception)

    assert result.exit_code == 0
    assert result.output.splitlines(keepends=False) == ["0.1.0"]


def test_patch(tmp_path: Path):
    """The patch subcommand should bump the given value to the next patch version."""
    # Arrange
    runner: CliRunner = CliRunner()

    with inside_dir(tmp_path):
        result: Result = runner.invoke(cli.cli, ["patch", "v1.2.3"])

    if result.exit_code != 0:
        print(result.output)
        print(result.exception)

    assert result.exit_code == 0
    assert result.output.splitlines(keepends=False) == ["1.2.4"]


def test_show_and_increment(tmp_path: Path, fixtures_path: Path):
    """The show subcommand should incrment the version and display it."""
    # Arrange
    config_path = tmp_path / "pyproject.toml"
    toml_path = fixtures_path / "basic_cfg.toml"
    shutil.copy(toml_path, config_path)
    runner: CliRunner = CliRunner()

    with inside_dir(tmp_path):
        result: Result = runner.invoke(cli.cli, ["show", "new_version", "--increment", "minor"])

    if result.exit_code != 0:
        print(result.output)
        print(result.exception)

    assert result.exit_code == 0
    assert result.output.splitlines(keepends=False) == ["1.1.0-dev"]


def test_show_no_args(tmp_path: Path, fixtures_path: Path):
    """The show subcommand should list the entire configuration."""
    # Arrange
    config_path = tmp_path / "pyproject.toml"
    toml_path = fixtures_path / "basic_cfg.toml"
    expected_output = fixtures_path.joinpath("basic_cfg_expected.yaml").read_text()

    shutil.copy(toml_path, config_path)
    runner: CliRunner = CliRunner()

    with inside_dir(tmp_path):
        result: Result = runner.invoke(cli.cli, ["show", "--format", "yaml"])

    if result.exit_code != 0:
        print(result.output)
        print(result.exception)

    assert result.exit_code == 0
    assert result.output.strip() == expected_output.strip()


def test_replace(mocker, tmp_path, fixtures_path):
    """The replace subcommand should replace the version in the file."""
    # Arrange
    toml_path = fixtures_path / "basic_cfg.toml"
    config_path = tmp_path / "pyproject.toml"
    shutil.copy(toml_path, config_path)

    mocked_modify_files = mocker.patch("bumpversion.cli.modify_files")
    runner: CliRunner = CliRunner()
    with inside_dir(tmp_path):
        result: Result = runner.invoke(cli.cli, ["replace", "--new-version", "1.1.0"])

    if result.exit_code != 0:
        print(result.output)

    assert result.exit_code == 0

    call_args = mocked_modify_files.call_args[0]
    configured_files = call_args[0]
    assert len(configured_files) == 3
    actual_filenames = {f.path for f in configured_files}
    assert actual_filenames == {"setup.py", "CHANGELOG.md", "bumpversion/__init__.py"}


def test_replace_no_newversion(mocker, tmp_path, fixtures_path):
    """The replace subcommand should set new_version to None in the context."""
    # Arrange
    toml_path = fixtures_path / "basic_cfg.toml"
    config_path = tmp_path / "pyproject.toml"
    shutil.copy(toml_path, config_path)

    mocked_modify_files = mocker.patch("bumpversion.cli.modify_files")
    runner: CliRunner = CliRunner()
    with inside_dir(tmp_path):
        result: Result = runner.invoke(cli.cli, ["replace"])

    if result.exit_code != 0:
        print(result.output)

    assert result.exit_code == 0

    call_args = mocked_modify_files.call_args[0]
    assert call_args[2] is None


def test_replace_specific_files(mocker, git_repo, fixtures_path):
    """The replace subcommand should set the files to only the specified files."""
    # Arrange
    toml_path = fixtures_path / "basic_cfg.toml"
    config_path = git_repo / "pyproject.toml"
    shutil.copy(toml_path, config_path)

    mocked_modify_files = mocker.patch("bumpversion.cli.modify_files")
    runner: CliRunner = CliRunner()
    with inside_dir(git_repo):
        result: Result = runner.invoke(cli.cli, ["replace", "--no-configured-files", "VERSION"])

    if result.exit_code != 0:
        print(result.output)

    assert result.exit_code == 0

    call_args = mocked_modify_files.call_args[0]
    configured_files = call_args[0]
    assert len(configured_files) == 1
    assert configured_files[0].path == "VERSION"


TEST_REPLACE_CONFIG = {
    "tool": {
        "bumpversion": {
            "allow_dirty": True,
            "commit": False,
            "current_version": "2.17.7",
            "files": [],
            "message": "Bump version: {current_version} → {new_version}",
            "parse": "(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+)",
            "parts": {
                "major": {},
                "minor": {},
                "patch": {},
            },
            "replace": "{new_version}",
            "search": "{current_version}",
            "serialize": ["{major}.{minor}.{patch}"],
            "sign_tags": False,
            "tag": False,
            "tag_message": "Bump version: {current_version} → {new_version}",
            "tag_name": "v{new_version}",
        }
    }
}


def test_replace_search_with_plain_string(tmp_path, fixtures_path):
    """Replace should not worry if the search or replace values have version info."""
    from tomlkit import dumps

    # Arrange
    config_path = tmp_path / "pyproject.toml"
    config_path.write_text(dumps(TEST_REPLACE_CONFIG))
    doc_path = tmp_path / "docs.yaml"
    doc_path.write_text("url: https://github.com/sampleuser/workflows/main/.github/update_mailmap.py")

    runner: CliRunner = CliRunner()
    with inside_dir(tmp_path):
        result: Result = runner.invoke(
            cli.cli,
            [
                "replace",
                "--no-configured-files",
                "--search",
                "/workflows/main/",
                "--replace",
                "/workflows/v{current_version}/",
                "./docs.yaml",
            ],
        )

    if result.exit_code != 0:
        print("Here is the output:")
        print(result.output)
        print(traceback.print_exception(result.exc_info[1]))

    assert result.exit_code == 0


def test_valid_regex_not_ignoring_regex(tmp_path: Path, caplog) -> None:
    """A search string not meant to be a regex (but is) is still found and replaced correctly."""
    # Arrange
    search = "(unreleased)"
    replace = "(2023-01-01)"

    version_path = tmp_path / "VERSION"
    version_path.write_text("# Changelog\n\n## [0.0.1 (unreleased)](https://cool.url)\n\n- Test unreleased package.\n")
    config_file = tmp_path / ".bumpversion.toml"
    config_file.write_text(
        "[tool.bumpversion]\n"
        'current_version = "0.0.1"\n'
        "allow_dirty = true\n\n"
        "[[tool.bumpversion.files]]\n"
        'filename = "VERSION"\n'
        "regex = false\n"
        f'search = "{search}"\n'
        f'replace = "{replace}"\n'
    )

    # Act
    runner: CliRunner = CliRunner()
    with inside_dir(tmp_path):
        result: Result = runner.invoke(
            cli.cli,
            [
                "replace",
                "--verbose",
                "--no-regex",
                "--no-configured-files",
                "--search",
                search,
                "--replace",
                replace,
                "VERSION",
            ],
        )

    # Assert
    if result.exit_code != 0:
        print(result.output)

    assert result.exit_code == 0
    assert (
        version_path.read_text()
        == "# Changelog\n\n## [0.0.1 (2023-01-01)](https://cool.url)\n\n- Test unreleased package.\n"
    )
