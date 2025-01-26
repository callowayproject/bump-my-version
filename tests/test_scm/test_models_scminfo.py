"""Tests for the bumpversion.scm.base.SCMInfo class."""

from pathlib import Path
from unittest.mock import patch

import pytest
from pytest import param

from bumpversion.scm.models import DefaultSCMTool, LatestTagInfo, SCMConfig, SCMInfo
from tests.conftest import inside_dir


def test_initialization(scm_config: SCMConfig, tmp_path: Path) -> None:
    """Ensure SCMInfo initializes with correct defaults."""
    # Arrange
    # Act
    with inside_dir(tmp_path):
        scm_info = SCMInfo(config=scm_config)

    # Assert
    assert scm_info.config == scm_config
    assert scm_info.commit_sha is None
    assert scm_info.distance_to_latest_tag == 0
    assert scm_info.current_version is None
    assert scm_info.current_tag is None
    assert scm_info.branch_name is None
    assert scm_info.short_branch_name is None
    assert scm_info.repository_root is None
    assert scm_info.dirty is None
    assert isinstance(scm_info.tool, DefaultSCMTool)


class TestPathInRepo:
    """Tests for the path_in_repo method."""

    def test_no_repository_root_returns_true(self, scm_config: SCMConfig, tmp_path: Path) -> None:
        """Ensure path_in_repo returns True when repository_root is None."""
        # Arrange
        with inside_dir(tmp_path):
            scm_info = SCMInfo(scm_config)
        scm_info.repository_root = None

        # Act
        result = scm_info.path_in_repo("some/path")

        # Assert
        assert result is True

    def test_absolute_path_in_repo_returns_true(self, scm_config: SCMConfig, tmp_path: Path) -> None:
        """Ensure path_in_repo returns the correct result for absolute paths."""
        # Arrange
        full_test_path = tmp_path / "repo" / "root" / "some" / "path"
        with inside_dir(tmp_path):
            scm_info = SCMInfo(scm_config)
            scm_info.repository_root = tmp_path / "repo" / "root"

        # Act
        result = scm_info.path_in_repo(full_test_path)

        # Assert
        assert result is True

    def test_relative_path_in_repo_returns_true(self, scm_config: SCMConfig, tmp_path: Path) -> None:
        """Ensure path_in_repo returns the correct result for relative paths."""
        # Arrange
        with inside_dir(tmp_path):
            scm_info = SCMInfo(scm_config)
            scm_info.repository_root = tmp_path / "repo" / "root"

        # Act
        result = scm_info.path_in_repo("some/path")

        # Assert
        assert result is True

    def test_absolute_path_outside_repo_returns_false(self, scm_config: SCMConfig, tmp_path: Path) -> None:
        """Ensure path_in_repo returns the correct result for absolute paths."""
        # Arrange
        with inside_dir(tmp_path):
            scm_info = SCMInfo(scm_config)
            scm_info.repository_root = tmp_path / "repo" / "root"

        # Act
        result = scm_info.path_in_repo(tmp_path)

        # Assert
        assert result is False


@patch("bumpversion.scm.git.Git.is_available", return_value=True)
@patch("bumpversion.scm.git.Git.latest_tag_info")
def test_set_from_scm_tool(mock_latest_tag_info, mock_is_available, scm_config: SCMConfig, tmp_path: Path) -> None:
    """Ensure _set_from_scm_tool sets the correct tool if available."""
    # Arrange
    mock_latest_tag_info.return_value = LatestTagInfo(
        commit_sha="abc123",
        distance_to_latest_tag=5,
        current_version="0.1.0",
        current_tag="v0.1.0",
        branch_name="main",
        short_branch_name="main",
        repository_root=tmp_path,
        dirty=False,
    )
    scm_info = SCMInfo(scm_config)

    # Act
    scm_info._set_from_scm_tool()

    # Assert
    assert scm_info.commit_sha == "abc123"
    assert scm_info.distance_to_latest_tag == 5
    assert scm_info.current_version == "0.1.0"
    assert scm_info.current_tag == "v0.1.0"
    assert scm_info.branch_name == "main"
    assert scm_info.short_branch_name == "main"
    assert scm_info.repository_root == tmp_path
    assert scm_info.dirty is False


class TestCommitAndTag:
    """Tests for the commit_and_tag method."""

    def test_skips_commit_if_not_configured(self, scm_config: SCMConfig, tmp_path: Path) -> None:
        """Ensure commit_and_tag skips commit if not configured."""
        # Arrange
        scm_config.commit = False
        scm_config.tag = True
        with inside_dir(tmp_path):
            scm_info = SCMInfo(config=scm_config)
            scm_info.tool = DefaultSCMTool(scm_config)
            mock_context = {"current_version": "1.0.0", "new_version": "1.0.1"}

            with patch.object(scm_info, "_commit") as mock_commit, patch.object(scm_info, "_tag") as mock_tag:
                # Act
                scm_info.commit_and_tag([], mock_context)

                # Assert
                mock_commit.assert_not_called()
                mock_tag.assert_called()

    def test_skips_tag_if_not_configured(self, scm_config: SCMConfig, tmp_path: Path) -> None:
        """Ensure commit_and_tag skips tag if not configured."""
        # Arrange
        scm_config.commit = True
        scm_config.tag = False
        with inside_dir(tmp_path):
            scm_info = SCMInfo(config=scm_config)
            scm_info.tool = DefaultSCMTool(scm_config)
            mock_context = {"current_version": "1.0.0", "new_version": "1.0.1"}

            with patch.object(scm_info, "_commit") as mock_commit, patch.object(scm_info, "_tag") as mock_tag:
                # Act
                scm_info.commit_and_tag([], mock_context)

                # Assert
                mock_commit.assert_called()
                mock_tag.assert_not_called()
