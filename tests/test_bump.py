"""Tests for the bump module."""

import shutil
from pathlib import Path
from textwrap import dedent
from unittest.mock import MagicMock, patch

import pytest

from bumpversion import bump
from bumpversion.exceptions import ConfigurationError, VersionNotFoundError
from bumpversion.files import ConfiguredFile
from bumpversion.scm.git import Git
from bumpversion.scm.models import SCMConfig, SCMInfo, DefaultSCMTool
from bumpversion.utils import run_command
from tests.conftest import get_config_data, inside_dir


@pytest.fixture
def mock_context():
    return {"current_version": "1.2.3", "new_version": "1.2.4"}


class TestGetNextVersion:
    """Tests for the get_next_version function."""

    def test_passing_a_new_version_should_override_a_version_part(self, tmp_path: Path):
        """Passing a new version should return that version, even if a version part is provided."""
        # Arrange
        with inside_dir(tmp_path):
            config, version_config, current_version = get_config_data({"current_version": "0.1.0"})
            version_part = "patch"
            new_version = "1.2.3"
            expected_next_version = version_config.parse("1.2.3")

            # Act
            actual_next_version = bump.get_next_version(current_version, config, version_part, new_version)

        # Assert
        assert actual_next_version == expected_next_version

    def test_passing_version_part_should_increment_part(self):
        """If a version part is provided, it should return the increment of that part."""
        # Arrange
        config, version_config, current_version = get_config_data({"current_version": "0.1.0"})
        version_part = "major"
        new_version = None
        expected_next_version = version_config.parse("1.0.0")

        # Act
        actual_next_version = bump.get_next_version(current_version, config, version_part, new_version)

        # Assert
        assert actual_next_version == expected_next_version

    def test_passing_no_arguments_raises_error(self):
        """If no arguments are provided, an error should be raised."""
        # Arrange
        current_version = MagicMock()
        config = MagicMock()
        version_part = None
        new_version = None

        # Act/Assert
        with pytest.raises(ConfigurationError):
            bump.get_next_version(current_version, config, version_part, new_version)


class TestDoBump:
    """Tests for the do_bump function."""

    @patch("bumpversion.files.modify_files")
    @patch("bumpversion.bump.update_config_file")
    def test_passing_version_part_increments_part(
        self, mock_update_config_file, mock_modify_files, scm_config: SCMConfig
    ):
        """If a version part is provided, and no new version, it should increment that part."""
        # Arrange
        version_part = "major"
        new_version = None
        config, _, current_version = get_config_data(
            {
                "current_version": "1.2.3",
                "files": [{"filename": "foo.txt"}, {"filename": "bar.txt"}],
            }
        )
        config.scm_info = SCMInfo(scm_config)
        dry_run = False

        # Act
        bump.do_bump(version_part, new_version, config, dry_run=dry_run)

        # Assert
        mock_modify_files.assert_called_once()
        mock_update_config_file.assert_called_once()
        assert {f.file_change.filename for f in mock_modify_files.call_args[0][0]} == {
            "foo.txt",
            "bar.txt",
        }
        assert mock_update_config_file.call_args[0][0] is None
        assert mock_update_config_file.call_args[0][1] == config
        assert mock_update_config_file.call_args[0][2] == current_version
        assert mock_update_config_file.call_args[0][3] == current_version.bump(version_part)
        assert mock_update_config_file.call_args[0][5] is False

    @patch("bumpversion.files.modify_files")
    @patch("bumpversion.bump.update_config_file")
    def test_passing_new_version_sets_version(self, mock_update_config_file, mock_modify_files, scm_config: SCMConfig):
        """If a new version is provided, it should set the version to that new version."""
        # Arrange
        version_part = None
        new_version = "2.0.0"
        config, version_config, current_version = get_config_data(
            {
                "current_version": "1.2.3",
            }
        )
        config.scm_info = SCMInfo(scm_config)
        dry_run = True

        # Act
        bump.do_bump(version_part, new_version, config, dry_run=dry_run)

        # Assert
        mock_modify_files.assert_called_once()
        assert mock_modify_files.call_args[0][0] == []
        assert mock_modify_files.call_args[0][1] == current_version
        assert mock_modify_files.call_args[0][2] == version_config.parse(new_version)

        mock_update_config_file.assert_called_once()
        assert mock_update_config_file.call_args[0][0] is None
        assert mock_update_config_file.call_args[0][1] == config
        assert mock_update_config_file.call_args[0][2] == current_version
        assert mock_update_config_file.call_args[0][3] == version_config.parse(new_version)
        assert mock_update_config_file.call_args[0][5] is dry_run

    @patch("bumpversion.bump.commit_and_tag")
    @patch("bumpversion.bump.update_config_file")
    def test_doesnt_commit_if_modify_error(
        self, mock_update_config_file, mock_commit_and_tag, tmp_path: Path, fixtures_path: Path
    ):
        """If there is an error modifying a file, the commit should not happen."""
        from bumpversion import config

        # Arrange
        setup_py_path = tmp_path / "setup.py"
        setup_py_path.touch()
        init_path = tmp_path / "bumpversion/__init__.py"
        init_path.parent.mkdir(parents=True)
        init_path.touch()
        orig_config_path = fixtures_path / "basic_cfg.toml"
        dest_config_path = tmp_path / "pyproject.toml"
        shutil.copyfile(orig_config_path, dest_config_path)
        version_part = "patch"

        # Act
        with inside_dir(tmp_path):
            config = config.get_configuration(config_file=dest_config_path)
            with pytest.raises(VersionNotFoundError):
                bump.do_bump(version_part, None, config)

        # Assert
        mock_commit_and_tag.assert_not_called()

        mock_update_config_file.assert_not_called()

    @patch("bumpversion.files.modify_files")
    @patch("bumpversion.bump.update_config_file")
    def test_when_new_equals_current_nothing_happens(self, mock_update_config_file, mock_modify_files, tmp_path: Path):
        """When the new version is the same as the current version, nothing should happen."""
        # Arrange
        version_part = None
        new_version = "1.2.3"

        with inside_dir(tmp_path):
            config, _, _ = get_config_data({"current_version": "1.2.3"})
            # Act
            bump.do_bump(version_part, new_version, config)

        # Assert
        mock_modify_files.assert_not_called()
        mock_update_config_file.assert_not_called()

    def test_passing_no_arguments_raises_error(self, scm_config: SCMConfig):
        """If no arguments are provided, an error should be raised."""
        # Arrange
        version_part = None
        new_version = None
        config, _, _ = get_config_data({"current_version": "1.2.3"})
        config.scm_info = SCMInfo(scm_config)
        dry_run = False

        # Act/Assert
        with pytest.raises(ConfigurationError):
            bump.do_bump(version_part, new_version, config, dry_run=dry_run)

    @patch("bumpversion.files.modify_files")
    @patch("bumpversion.bump.update_config_file")
    def test_includes_files_with_include_bumps(
        self, mock_update_config_file, mock_modify_files, scm_config: SCMConfig
    ):
        """Files that have include_bumps are included when those bumps happen."""
        # Arrange
        new_version = None
        config, _, _ = get_config_data(
            {
                "current_version": "1.2.3",
                "files": [{"filename": "foo.txt", "include_bumps": ["major", "minor"]}, {"filename": "bar.txt"}],
            }
        )
        config.scm_info = SCMInfo(scm_config)
        dry_run = False

        # Act
        bump.do_bump("patch", new_version, config, dry_run=dry_run)

        # Assert
        assert {f.file_change.filename for f in mock_modify_files.call_args[0][0]} == {"bar.txt"}

        # Act
        bump.do_bump("minor", new_version, config, dry_run=dry_run)

        # Assert
        assert {f.file_change.filename for f in mock_modify_files.call_args[0][0]} == {"foo.txt", "bar.txt"}

    @patch("bumpversion.files.modify_files")
    @patch("bumpversion.bump.update_config_file")
    def test_excludes_files_with_exclude_bumps(
        self, mock_update_config_file, mock_modify_files, scm_config: SCMConfig
    ):
        """Files that have exclude_bumps are excluded when those bumps happen."""
        # Arrange
        new_version = None
        config, _, _ = get_config_data(
            {
                "current_version": "1.2.3",
                "files": [{"filename": "foo.txt", "exclude_bumps": ["patch"]}, {"filename": "bar.txt"}],
            }
        )
        config.scm_info = SCMInfo(scm_config)
        dry_run = False

        # Act
        bump.do_bump("patch", new_version, config, dry_run=dry_run)

        # Assert
        assert {f.file_change.filename for f in mock_modify_files.call_args[0][0]} == {"bar.txt"}

        # Act
        bump.do_bump("minor", new_version, config, dry_run=dry_run)

        # Assert
        assert {f.file_change.filename for f in mock_modify_files.call_args[0][0]} == {"foo.txt", "bar.txt"}


class TestCommitAndTag:
    """Tests for the commit_and_tag function."""

    def test_does_nothing_if_no_scm_tool(self, scm_config: SCMConfig):
        """If there is no SCM tool, nothing should happen."""
        # Arrange
        config, _, _ = get_config_data(
            {
                "current_version": "1.2.3",
            }
        )
        config.scm_info = SCMInfo(scm_config)
        config.scm_info.tool = None
        mock_commit_and_tag = MagicMock()
        config.scm_info.commit_and_tag = mock_commit_and_tag
        mock_context = MagicMock()

        # Act
        bump.commit_and_tag(config, None, [], mock_context, False)

        # Assert
        assert mock_commit_and_tag.call_count == 0

    def test_calls_scm_tool_commit_and_tag_with_files(self, mock_context, scm_config: SCMConfig):
        """When there is an SCM tool, the files should be passed to the SCM tool."""
        # Arrange
        config, version_config, _ = get_config_data(
            {"current_version": "1.2.3", "files": [{"filename": "foo.txt"}, {"filename": "bar.txt"}]}
        )
        config.scm_info = MagicMock(spec=SCMInfo)
        config.scm_info.tool = MagicMock(spec=Git)
        configured_files = [ConfiguredFile(file_cfg, version_config) for file_cfg in config.files]

        # Act
        bump.commit_and_tag(config, None, configured_files, mock_context, False)

        # Assert
        config.scm_info.commit_and_tag.assert_called_once()
        assert set(config.scm_info.commit_and_tag.call_args[0][0]) == {"foo.txt", "bar.txt"}

    def test_includes_config_file_in_files(self, mock_context, scm_config: SCMConfig):
        """If the config file is passed to commit_and_tag, it should be included in the files list."""
        # Arrange
        config, version_config, _ = get_config_data(
            {"current_version": "1.2.3", "files": [{"filename": "foo.txt"}, {"filename": "bar.txt"}]}
        )
        config.scm_info = MagicMock(spec=SCMInfo)
        config.scm_info.tool = MagicMock(spec=Git)
        configured_files = [ConfiguredFile(file_cfg, version_config) for file_cfg in config.files]

        # Act
        bump.commit_and_tag(config, Path("pyproject.toml"), configured_files, mock_context, False)

        # Assert
        config.scm_info.commit_and_tag.assert_called_once()
        assert set(config.scm_info.commit_and_tag.call_args[0][0]) == {"foo.txt", "bar.txt", "pyproject.toml"}


def test_key_path_required_for_toml_change(tmp_path: Path, caplog):
    """If the key_path is not provided, the toml file should use standard search and replace."""
    from click.testing import CliRunner, Result

    from bumpversion import cli, config

    # Arrange
    config_path = tmp_path / "pyproject.toml"
    config_path.write_text(
        dedent(
            """
            [project]
            version = "0.1.26"

            [tool.bumpversion]
            current_version = "0.1.26"
            allow_dirty = true
            commit = true

            [[tool.bumpversion.files]]
            filename = "pyproject.toml"
            search = "version = \\"{current_version}\\""
            replace = "version = \\"{new_version}\\""

            [tool.othertool]
            bake_cookies = true
            ignore-words-list = "sugar, salt, flour"
            """
        ),
        encoding="utf-8",
    )

    conf = config.get_configuration(config_file=config_path)

    # Act
    runner: CliRunner = CliRunner()
    with inside_dir(tmp_path):
        result: Result = runner.invoke(
            cli.cli,
            ["bump", "-vv", "minor"],
        )

    if result.exit_code != 0:
        print(caplog.text)
        print("Here is the output:")
        print(result.output)
        import traceback

        print(traceback.print_exception(result.exc_info[1]))

    # Assert
    assert result.exit_code == 0
    assert config_path.read_text() == dedent(
        """
        [project]
        version = "0.2.0"

        [tool.bumpversion]
        current_version = "0.2.0"
        allow_dirty = true
        commit = true

        [[tool.bumpversion.files]]
        filename = "pyproject.toml"
        search = "version = \\"{current_version}\\""
        replace = "version = \\"{new_version}\\""

        [tool.othertool]
        bake_cookies = true
        ignore-words-list = "sugar, salt, flour"
        """
    )


def test_changes_to_files_are_committed(git_repo: Path, caplog):
    """Any files changed during the bump are committed."""
    from click.testing import CliRunner, Result

    from bumpversion import cli

    # Arrange
    config_path = git_repo / ".bumpversion.toml"
    config_path.write_text(
        dedent(
            """
            [tool.bumpversion]
            current_version = "0.1.26"
            tag_name = "{new_version}"
            commit = true

            [[tool.bumpversion.files]]
            glob = "helm/charts/*/Chart.yaml"

            """
        ),
        encoding="utf-8",
    )
    chart_contents = dedent(
        """
        appVersion: 0.1.26
        version: 0.1.26

        """
    )
    chart1_path = git_repo / "helm" / "charts" / "somechart" / "Chart.yaml"
    chart2_path = git_repo / "helm" / "charts" / "otherchart" / "Chart.yaml"
    chart1_path.parent.mkdir(parents=True, exist_ok=True)
    chart1_path.write_text(chart_contents, encoding="utf-8")
    chart2_path.parent.mkdir(parents=True, exist_ok=True)
    chart2_path.write_text(chart_contents, encoding="utf-8")

    with inside_dir(git_repo):
        run_command(["git", "add", str(chart1_path), str(chart2_path), str(config_path)])
        run_command(["git", "commit", "-m", "Initial commit"])
        run_command(["git", "tag", "0.1.26"])

    # Act
    runner: CliRunner = CliRunner()
    with inside_dir(git_repo):
        result: Result = runner.invoke(
            cli.cli,
            ["bump", "-vv", "minor"],
        )

    if result.exit_code != 0:
        print(caplog.text)
        print("Here is the output:")
        print(result.output)
        import traceback

        print(traceback.print_exception(result.exc_info[1]))

    # Assert
    assert result.exit_code == 0
    assert config_path.read_text() == dedent(
        """
        [tool.bumpversion]
        current_version = "0.2.0"
        tag_name = "{new_version}"
        commit = true

        [[tool.bumpversion.files]]
        glob = "helm/charts/*/Chart.yaml"

        """
    )
    assert chart1_path.read_text() == dedent(
        """
        appVersion: 0.2.0
        version: 0.2.0

        """
    )
    assert chart2_path.read_text() == dedent(
        """
        appVersion: 0.2.0
        version: 0.2.0

        """
    )
    with inside_dir(git_repo):
        status = run_command(["git", "status", "--porcelain"])
        assert status.stdout == ""
