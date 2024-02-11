"""Tests for `bumpversion` package."""

import shutil
import traceback
from pathlib import Path

from click.testing import CliRunner, Result

from bumpversion import cli
from tests.conftest import inside_dir

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


class TestReplaceCLI:
    """Test the replace CLI subcommand."""

    class TestDefaultReplacesVersion:
        """Test the default behavior of the replace subcommand."""

        def test_default_affects_all_configured_files(self, mocker, tmp_path, fixtures_path):
            """The replace subcommand should replace the version in all configured files."""
            # Arrange
            toml_path = fixtures_path / "basic_cfg.toml"
            config_path = tmp_path / "pyproject.toml"
            shutil.copy(toml_path, config_path)

            mocked_modify_files = mocker.patch("bumpversion.cli.modify_files")
            runner: CliRunner = CliRunner()
            with inside_dir(tmp_path):
                result: Result = runner.invoke(cli.cli, ["replace", "--new-version", "1.1.0"])

            if result.exit_code != 0:
                print("Here is the output:")
                print(result.output)
                print(traceback.print_exception(result.exc_info[1]))

            assert result.exit_code == 0

            call_args = mocked_modify_files.call_args[0]
            configured_files = call_args[0]
            assert len(configured_files) == 3
            actual_filenames = {f.file_change.filename for f in configured_files}
            assert actual_filenames == {"setup.py", "CHANGELOG.md", "bumpversion/__init__.py"}

        def test_can_limit_to_specific_files(self, mocker, git_repo, fixtures_path):
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
                print("Here is the output:")
                print(result.output)
                print(traceback.print_exception(result.exc_info[1]))

            assert result.exit_code == 0

            call_args = mocked_modify_files.call_args[0]
            configured_files = call_args[0]
            assert len(configured_files) == 1
            assert configured_files[0].file_change.filename == "VERSION"

    class TestOptions:
        """Test the options of the replace subcommand."""

        def test_missing_newversion_is_set_to_none(self, mocker, tmp_path, fixtures_path):
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
                print("Here is the output:")
                print(result.output)
                print(traceback.print_exception(result.exc_info[1]))

            assert result.exit_code == 0

            call_args = mocked_modify_files.call_args[0]
            assert call_args[2] is None

        def test_ignores_missing_files_with_option(self, mocker, tmp_path, fixtures_path):
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
                        "replace",
                        "--verbose",
                        "--no-regex",
                        "--no-configured-files",
                        "--ignore-missing-files",
                        "VERSION",
                    ],
                )

            # Assert
            if result.exit_code != 0:
                print("Here is the output:")
                print(result.output)
                print(traceback.print_exception(result.exc_info[1]))

            assert result.exit_code == 0

    class TestSearchInputs:
        """Test the search inputs of the replace subcommand."""

        def test_accepts_plain_string(self, tmp_path, fixtures_path):
            """Replace should not worry if the search values have version info."""
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

        def test_unintentional_valid_regex_still_found(self, tmp_path: Path, caplog) -> None:
            """A search string not meant to be a regex (but is) is still found and replaced correctly."""
            # Arrange
            search = "(unreleased)"
            replace = "(2023-01-01)"

            version_path = tmp_path / "VERSION"
            version_path.write_text(
                "# Changelog\n\n## [0.0.1 (unreleased)](https://cool.url)\n\n- Test unreleased package.\n"
            )
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
                print("Here is the output:")
                print(result.output)
                print(traceback.print_exception(result.exc_info[1]))

            assert result.exit_code == 0
            assert (
                version_path.read_text()
                == "# Changelog\n\n## [0.0.1 (2023-01-01)](https://cool.url)\n\n- Test unreleased package.\n"
            )

    class TestReplaceInputs:
        """Test the replace inputs of the replace subcommand."""

        def test_accepts_empty_string(self, tmp_path, fixtures_path):
            """Replace should be able to replace strings with an empty string."""
            from tomlkit import dumps

            # Arrange
            config_path = tmp_path / "pyproject.toml"
            config_path.write_text(dumps(TEST_REPLACE_CONFIG))
            doc_path = tmp_path / "docs.yaml"
            doc_path.write_text("We should censor profanity\n\n")

            runner: CliRunner = CliRunner()
            with inside_dir(tmp_path):
                result: Result = runner.invoke(
                    cli.cli,
                    [
                        "replace",
                        "--verbose",
                        "--no-configured-files",
                        "--allow-dirty",
                        "--search",
                        "profanity",
                        "--replace",
                        "",
                        "./docs.yaml",
                    ],
                )

            if result.exit_code != 0:
                print("Here is the output:")
                print(result.output)
                print(traceback.print_exception(result.exc_info[1]))
            assert result.exit_code == 0
            assert doc_path.read_text() == "We should censor \n\n"

        def test_accepts_plain_string(self, tmp_path, fixtures_path):
            """Replace should not worry if the replace values have version info."""
            from tomlkit import dumps

            # Arrange
            config_path = tmp_path / "pyproject.toml"
            config_path.write_text(dumps(TEST_REPLACE_CONFIG))
            doc_path = tmp_path / "docs.yaml"
            doc_path.write_text("url: https://github.com/sampleuser/workflows/v2.17.7/.github/update_mailmap.py")

            runner: CliRunner = CliRunner()
            with inside_dir(tmp_path):
                result: Result = runner.invoke(
                    cli.cli,
                    [
                        "replace",
                        "--no-configured-files",
                        "--search",
                        "/workflows/v{current_version}/",
                        "--replace",
                        "/workflows/main/",
                        "./docs.yaml",
                    ],
                )

            if result.exit_code != 0:
                print("Here is the output:")
                print(result.output)
                print(traceback.print_exception(result.exc_info[1]))

            assert result.exit_code == 0
            assert (
                doc_path.read_text() == "url: https://github.com/sampleuser/workflows/main/.github/update_mailmap.py"
            )
