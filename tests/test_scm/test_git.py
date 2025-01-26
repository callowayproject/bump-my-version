"""Tests for bumpversion.scm.git."""

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from pytest import param

from bumpversion.exceptions import BumpVersionError, DirtyWorkingDirectoryError
from bumpversion.scm.git import Git, assert_nondirty, commit_info, moveable_tag, revision_info, tag
from bumpversion.scm.models import LatestTagInfo, SCMConfig
from bumpversion.utils import run_command
from tests.conftest import inside_dir


class TestGit:
    """Tests related to Git."""

    class TestIsAvailable:
        """Tests related to Git.is_available."""

        def test_recognizes_a_git_repo(self, git_repo: Path, scm_config: SCMConfig) -> None:
            """Should return true if git is available, and it is a git repo."""
            with inside_dir(git_repo):
                git_tool = Git(scm_config)
                assert git_tool.is_available()

        def test_recognizes_not_a_git_repo(self, tmp_path: Path, scm_config: SCMConfig) -> None:
            """Should return false if it is not a git repo."""
            with inside_dir(tmp_path):
                git_tool = Git(scm_config)
                assert not git_tool.is_available()

    class TestLatestTagInfo:
        """Test for the Git.latest_tag_info() function."""

        def test_returns_default_if_not_available(self, tmp_path: Path, scm_config: SCMConfig) -> None:
            """If git is not available, it returns the default LatestTagInfo object, with all None values."""
            # Arrange
            expected = LatestTagInfo()
            tool = Git(scm_config)

            # Act
            with inside_dir(tmp_path):
                info = tool.latest_tag_info()

            # Assert
            assert info == expected

        def test_returns_correct_commit_and_tag_info(self, git_repo: Path, scm_config: SCMConfig) -> None:
            """Should return information that it is a git repo."""
            # Arrange
            tag_prefix = "app/"
            readme = git_repo.joinpath("readme.md")
            readme.touch()
            scm_config.tag_name = f"{tag_prefix}{{new_version}}"

            # Act
            with inside_dir(git_repo):
                commit_readme("first")
                tag(f"{tag_prefix}0.1.0", sign=False, message="bumpversion")
                tag_info = Git(scm_config).latest_tag_info()

            # Assert
            assert tag_info.commit_sha is not None
            assert tag_info.current_version == "0.1.0"
            assert tag_info.current_tag == f"{tag_prefix}0.1.0"
            assert tag_info.distance_to_latest_tag == 0
            assert tag_info.branch_name == "main"
            assert tag_info.short_branch_name == "main"
            assert tag_info.repository_root == git_repo
            assert tag_info.dirty is False

    class TestGitAddPath:
        """Tests for the add_path method in the Git class."""

        @patch("bumpversion.scm.git.run_command")
        @patch("bumpversion.scm.git.Git.latest_tag_info")
        @patch("bumpversion.scm.git.is_subpath")
        def test_valid_subpath_is_added(
            self, mock_is_subpath, mock_latest_tag_info, mock_run_command, scm_config: SCMConfig, tmp_path: Path
        ):
            """A path that is a subpath of the repository root should be added."""
            # Arrange
            repository_root = tmp_path / "repository"
            repository_root.mkdir()
            path_to_add = repository_root / "file.txt"
            mock_latest_tag_info.return_value.repository_root = repository_root
            mock_is_subpath.return_value = True
            mock_run_command.return_value = None
            git_instance = Git(scm_config)

            # Act
            with inside_dir(repository_root):
                git_instance.add_path(path_to_add)

            # Assert
            mock_run_command.assert_called_once_with(["git", "add", "--update", "file.txt"])

        @patch("bumpversion.scm.git.run_command")
        @patch("bumpversion.scm.git.Git.latest_tag_info")
        @patch("bumpversion.scm.git.is_subpath")
        def test_invalid_subpath_is_not_added(
            self, mock_is_subpath, mock_latest_tag_info, mock_run_command, scm_config, tmp_path: Path
        ):
            """A path that is not a subpath of the repository root should not be added."""
            # Arrange
            repository_root = tmp_path / "repository"
            repository_root.mkdir()
            path_to_add = repository_root / "file.txt"
            mock_latest_tag_info.return_value.repository_root = repository_root
            mock_is_subpath.return_value = False
            git_instance = Git(scm_config)

            # Act
            git_instance.add_path(path_to_add)

            # Assert
            mock_run_command.assert_not_called()

        @patch("bumpversion.scm.git.run_command")
        @patch("bumpversion.scm.git.Git.latest_tag_info")
        @patch("bumpversion.scm.git.is_subpath")
        def test_raises_error_on_command_failure(
            self, mock_is_subpath, mock_latest_tag_info, mock_run_command, scm_config: SCMConfig, tmp_path: Path
        ):
            """If the git command fails, a BumpVersionError should be raised."""
            # Arrange
            repository_root = tmp_path / "repository"
            repository_root.mkdir()
            path_to_add = repository_root / "file.txt"
            mock_latest_tag_info.return_value.repository_root = repository_root
            mock_is_subpath.return_value = True
            mock_run_command.side_effect = subprocess.CalledProcessError(returncode=1, cmd="git add")
            git_instance = Git(scm_config)

            # Act / Assert
            with inside_dir(repository_root):
                with pytest.raises(BumpVersionError):
                    git_instance.add_path(path_to_add)


class TestRevisionInfo:
    """Tests for the revision_info function."""

    def test_returns_correct_data(self, git_repo: Path) -> None:
        """Should return the correct branch name and repository root."""
        # Arrange

        # Act
        with inside_dir(git_repo):
            result = revision_info()

        # Assert
        assert result["branch_name"] == "main"
        assert result["short_branch_name"] == "main"
        assert result["repository_root"] == git_repo

    @patch("bumpversion.scm.git.run_command")
    def test_returns_empty_data_on_git_command_error(self, mock_run_command):
        """If there is an error with the git command, the branch name and repository root should be empty."""
        # Arrange
        mock_run_command.side_effect = subprocess.CalledProcessError(1, "git")

        # Act
        result = revision_info()

        # Assert
        assert result["branch_name"] is None
        assert result["short_branch_name"] is None
        assert result["repository_root"] is None

    @pytest.mark.parametrize(
        ["branch_name", "expected"],
        [
            param("feature/add-very-long-branch-name-testing", "featureaddverylongbr", id="long branch name"),
            param("feat/add(#34)Special", "featadd34special", id="branch name with special characters"),
        ],
    )
    def test_short_branch_name_logic(self, git_repo: Path, branch_name: str, expected: str) -> None:
        """Long branch names should be shortened to 20 characters."""
        # Arrange
        with inside_dir(git_repo):
            run_command(["git", "checkout", "-b", branch_name])

            # Act
            result = revision_info()

        # Assert
        assert result["branch_name"] == branch_name
        assert result["short_branch_name"] == expected


class TestMoveableTag:
    """Tests for the moveable_tag function."""

    def test_moves_tags(self, git_repo: Path) -> None:
        """Tag moves to subsequent commit."""
        # Arrange
        readme = git_repo.joinpath("readme.md")
        readme.touch()

        # Act
        with inside_dir(git_repo):
            first_sha = commit_readme("first")
            moveable_tag("v1")

            readme.write_text("ping")
            second_sha = commit_readme("second")
            moveable_tag("v1")

            v1_sha = get_commit_sha("v1")

        # Assert
        assert v1_sha == second_sha
        assert v1_sha != first_sha


def get_commit_sha(tag: str) -> str:
    """Get the commit sha of a tag."""
    result = subprocess.run(  # noqa: S603
        ["git", "describe", "--tags", "--abbrev=40", "--long", f"--match={tag}"],  # noqa: S607
        capture_output=True,
        check=True,
        text=True,
    )
    bits = result.stdout.strip().split("-")
    return bits[2].lstrip("g")


def commit_readme(message: str) -> str:
    """Commit the readme file and return the commit sha1, so we can tag it later on."""
    subprocess.run(["git", "add", "readme.md"], check=True)  # noqa: S603, S607
    subprocess.run(["git", "commit", "-m", message], check=True)  # noqa: S603, S607
    result = subprocess.run(  # noqa: S603
        ["git", "rev-parse", "HEAD"], capture_output=True, check=True, text=True  # noqa: S607
    )
    return result.stdout.strip()


class TestAssertNonDirty:
    """Tests for the Git.assert_nondirty() function."""

    def test_does_nothing_when_not_dirty(self, git_repo: Path) -> None:
        """If the git repo is clean, assert_nondirty should do nothing."""
        with inside_dir(git_repo):
            assert_nondirty()

    def test_raises_error_when_dirty(self, git_repo: Path) -> None:
        """If the git repo has modified files, assert_nondirty should return false."""
        readme = git_repo.joinpath("readme.md")
        readme.touch()
        with pytest.raises(DirtyWorkingDirectoryError):
            with inside_dir(git_repo):
                subprocess.run(["git", "add", "readme.md"], check=False)  # noqa: S603, S607
                assert_nondirty()


class TestCommitInfo:
    """Tests for the commit_info function."""

    def test_returns_correct_structure(self, scm_config: SCMConfig, git_repo: Path) -> None:
        """Test that the returned dictionary has the correct structure."""
        # Arrange
        readme = git_repo.joinpath("readme.md")
        readme.touch()

        # Act
        with inside_dir(git_repo):
            commit_readme("first")
            tag("v1.0.0")
            result = commit_info(scm_config)

        # Assert
        assert isinstance(result, dict)
        assert "dirty" in result
        assert "commit_sha" in result
        assert "distance_to_latest_tag" in result
        assert "current_version" in result
        assert "current_tag" in result

    def test_detects_dirty_repo(self, scm_config: SCMConfig, git_repo: Path):
        """Test that the function detects a dirty repository."""
        # Arrange
        readme = git_repo.joinpath("readme.md")
        readme.touch()

        # Act
        with inside_dir(git_repo):
            commit_readme("first")
            tag_name = scm_config.tag_name.replace("{new_version}", "1.0.0")
            tag(tag_name)
            readme.write_text("ping")
            run_command(["git", "add", str(readme)])
            result = commit_info(scm_config)

        # Assert
        assert result["dirty"] is True

    @patch("bumpversion.scm.git.run_command")
    def test_commit_info_handles_clean_repo(self, mock_run_command):
        """Test that the function correctly identifies a clean repository."""
        # Arrange
        config = MagicMock(spec=SCMConfig)
        config.tag_name = "{new_version}"
        mock_result = MagicMock()
        mock_result.stdout = "v1.0.0-0-gabcd1234\n"
        mock_run_command.return_value = mock_result

        # Act
        result = commit_info(config)

        # Assert
        assert result["dirty"] is False

    @patch("bumpversion.scm.git.run_command")
    def test_commit_info_parses_commit_sha_correctly(self, mock_run_command):
        """Test that the commit SHA is correctly parsed."""
        # Arrange
        config = MagicMock(spec=SCMConfig)
        config.tag_name = "{new_version}"
        mock_result = MagicMock()
        mock_result.stdout = "v1.0.0-5-gabcd1234\n"
        mock_run_command.return_value = mock_result

        # Act
        result = commit_info(config)

        # Assert
        assert result["commit_sha"] == "abcd1234"

    @patch("bumpversion.scm.git.run_command")
    def test_commit_info_calculates_distance_to_latest_tag(self, mock_run_command):
        """Test that the function correctly calculates the distance to the latest tag."""
        # Arrange
        config = MagicMock(spec=SCMConfig)
        config.tag_name = "{new_version}"
        mock_result = MagicMock()
        mock_result.stdout = "v1.0.0-3-gabcd1234\n"
        mock_run_command.return_value = mock_result

        # Act
        result = commit_info(config)

        # Assert
        assert result["distance_to_latest_tag"] == 3

    @patch("bumpversion.scm.git.run_command")
    def test_commit_info_parses_current_tag_correctly(self, mock_run_command):
        """Test that the current tag is correctly parsed."""
        # Arrange
        config = MagicMock(spec=SCMConfig)
        config.tag_name = "{new_version}"
        mock_result = MagicMock()
        mock_result.stdout = "v1.0.0-0-gabcd1234\n"
        mock_run_command.return_value = mock_result

        # Act
        result = commit_info(config)

        # Assert
        assert result["current_tag"] == "v1.0.0"

    @patch("bumpversion.scm.git.run_command")
    def test_commit_info_calls_get_version_from_tag(self, mock_run_command):
        """Test that the function calls get_version_from_tag with the correct arguments."""
        # Arrange
        config = MagicMock(spec=SCMConfig)
        config.tag_name = "{new_version}"
        mock_result = MagicMock()
        mock_result.stdout = "v1.0.0-0-gabcd1234\n"
        mock_run_command.return_value = mock_result

        # Act
        commit_info(config)

        # Assert
        config.get_version_from_tag.assert_called_with("v1.0.0")

    @patch("bumpversion.scm.git.run_command")
    def test_commit_info_handles_subprocess_error(self, mock_run_command):
        """Test that the function handles subprocess errors gracefully."""
        # Arrange
        config = MagicMock(spec=SCMConfig)
        config.tag_name = "{new_version}"
        mock_run_command.side_effect = subprocess.CalledProcessError(1, "git describe")

        # Act
        result = commit_info(config)

        # Assert
        assert result["dirty"] is None
        assert result["commit_sha"] is None
        assert result["distance_to_latest_tag"] == 0
        assert result["current_version"] is None
        assert result["current_tag"] is None
