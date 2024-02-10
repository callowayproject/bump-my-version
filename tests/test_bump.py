"""Tests for the bump module."""

from pathlib import Path
from textwrap import dedent
from unittest.mock import MagicMock, patch

import pytest

from bumpversion import bump
from bumpversion.exceptions import ConfigurationError
from bumpversion.files import ConfiguredFile
from bumpversion.scm import Git, SCMInfo
from tests.conftest import get_config_data, inside_dir


@pytest.fixture
def mock_context():
    return {"current_version": "1.2.3", "new_version": "1.2.4"}


def test_get_next_version_with_new_version():
    """Passing a new version should return that version."""
    # Arrange
    config, version_config, current_version = get_config_data({"current_version": "0.1.0"})
    version_part = "patch"
    new_version = "1.2.3"
    expected_next_version = version_config.parse("1.2.3")

    # Act
    actual_next_version = bump.get_next_version(current_version, config, version_part, new_version)

    # Assert
    assert actual_next_version == expected_next_version


def test_get_next_version_with_version_part():
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


def test_get_next_version_with_no_arguments():
    # Arrange
    current_version = MagicMock()
    config = MagicMock()
    version_part = None
    new_version = None

    # Act/Assert
    with pytest.raises(ConfigurationError):
        bump.get_next_version(current_version, config, version_part, new_version)


@patch("bumpversion.files.modify_files")
@patch("bumpversion.bump.update_config_file")
def test_do_bump_with_version_part(mock_update_config_file, mock_modify_files):
    # Arrange
    version_part = "major"
    new_version = None
    config, version_config, current_version = get_config_data(
        {"current_version": "1.2.3", "files": [{"filename": "foo.txt"}, {"filename": "bar.txt"}]}
    )
    config.scm_info = SCMInfo()
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
def test_do_bump_with_new_version(mock_update_config_file, mock_modify_files):
    # Arrange
    version_part = None
    new_version = "2.0.0"
    config, version_config, current_version = get_config_data(
        {
            "current_version": "1.2.3",
        }
    )
    config.scm_info = SCMInfo()
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


@patch("bumpversion.files.modify_files")
@patch("bumpversion.bump.update_config_file")
def test_do_bump_when_new_equals_current(mock_update_config_file, mock_modify_files, tmp_path: Path):
    """When the new version is the same as the current version, nothing should happen."""

    # Arrange
    version_part = None
    new_version = "1.2.3"

    with inside_dir(tmp_path):
        config, version_config, current_version = get_config_data({"current_version": "1.2.3"})
        # Act
        bump.do_bump(version_part, new_version, config)

    # Assert
    mock_modify_files.assert_not_called()
    mock_update_config_file.assert_not_called()


def test_do_bump_with_no_arguments():
    # Arrange
    version_part = None
    new_version = None
    config, version_config, current_version = get_config_data({"current_version": "1.2.3"})
    config.scm_info = SCMInfo()
    dry_run = False

    # Act/Assert
    with pytest.raises(ConfigurationError):
        bump.do_bump(version_part, new_version, config, dry_run=dry_run)


def test_commit_and_tag_with_no_tool():
    config, version_config, current_version = get_config_data(
        {
            "current_version": "1.2.3",
        }
    )
    config.scm_info = SCMInfo()
    mock_context = MagicMock()

    bump.commit_and_tag(config, None, [], mock_context, False)


def test_commit_and_tag_with_tool(mock_context):
    config, version_config, current_version = get_config_data(
        {"current_version": "1.2.3", "files": [{"filename": "foo.txt"}, {"filename": "bar.txt"}]}
    )
    config.scm_info = SCMInfo()
    config.scm_info.tool = MagicMock(spec=Git)
    configured_files = [ConfiguredFile(file_cfg, version_config) for file_cfg in config.files]
    bump.commit_and_tag(config, None, configured_files, mock_context, False)
    config.scm_info.tool.commit_to_scm.assert_called_once()
    config.scm_info.tool.tag_in_scm.assert_called_once()
    assert set(config.scm_info.tool.commit_to_scm.call_args[0][0]) == {"foo.txt", "bar.txt"}


def test_commit_and_tag_with_config_file(mock_context):
    config, version_config, current_version = get_config_data(
        {"current_version": "1.2.3", "files": [{"filename": "foo.txt"}, {"filename": "bar.txt"}]}
    )
    config.scm_info = SCMInfo()
    config.scm_info.tool = MagicMock(spec=Git)
    configured_files = [ConfiguredFile(file_cfg, version_config) for file_cfg in config.files]
    bump.commit_and_tag(config, Path("pyproject.toml"), configured_files, mock_context, False)
    config.scm_info.tool.commit_to_scm.assert_called_once()
    config.scm_info.tool.tag_in_scm.assert_called_once()
    assert set(config.scm_info.tool.commit_to_scm.call_args[0][0]) == {"foo.txt", "bar.txt", "pyproject.toml"}


def test_key_path_required_for_toml_change(tmp_path: Path, caplog):
    """If the key_path is not provided, the toml file should use standard search and replace."""
    from bumpversion import config
    from bumpversion.version_part import VersionConfig

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
        )
    )

    conf = config.get_configuration(config_file=config_path)

    # Act
    from click.testing import CliRunner, Result
    from bumpversion import cli

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
