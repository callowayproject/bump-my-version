"""Tests for the mercurial SCM."""

import json
import shutil
import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest
from pytest import param

from bumpversion import cli
from bumpversion.exceptions import BumpVersionError, DirtyWorkingDirectoryError
from bumpversion.scm.hg import Mercurial, assert_nondirty, tag
from bumpversion.scm.models import LatestTagInfo, SCMConfig
from bumpversion.utils import run_command
from tests.conftest import inside_dir

BASIC_CONFIG = """
[tool.bumpversion]
commit = true
tag = true
current_version = "1.0.0"
parse = "(?P<major>\\\\d+)\\\\.(?P<minor>\\\\d+)\\\\.(?P<patch>\\\\d+)(\\\\-(?P<release>[a-z]+))?"
serialize = [
    "{major}.{minor}.{patch}-{release}",
    "{major}.{minor}.{patch}"
]
"""

pytestmark = pytest.mark.skipif(not shutil.which("hg"), reason="Mercurial is not available.")


@pytest.fixture
def hg_instance(scm_config: SCMConfig):
    """Return a Mercurial instance."""
    return Mercurial(scm_config)


def commit_readme(message: str) -> str:
    """Commit the readme file and return the commit sha1, so we can tag it later on."""
    subprocess.run(["hg", "add", "readme.md"], check=True)  # noqa: S603, S607
    subprocess.run(["hg", "commit", "-m", message], check=True)  # noqa: S603, S607
    result = subprocess.run(  # noqa: S603
        ["hg", "id", "-r", "tip"], capture_output=True, check=True, text=True  # noqa: S607
    )
    return result.stdout.strip()


class TestMercurial:
    """Tests of the Mercurial class."""

    class TestIsAvailable:
        """Tests of the is_available method."""

        def test_hg_is_not_available(self, tmp_path: Path, hg_instance: Mercurial) -> None:
            """Should return false if it is not a mercurial repo."""
            with inside_dir(tmp_path):
                assert not hg_instance.is_available()

        def test_hg_is_available(self, hg_repo: Path, hg_instance: Mercurial) -> None:
            """Should return false if it is not a mercurial repo."""
            with inside_dir(hg_repo):
                assert hg_instance.is_available()

    class TestLatestTagInfo:
        """Test for the Mercurial.latest_tag_info() function."""

        def test_returns_default_if_not_available(self, tmp_path: Path, hg_instance: Mercurial) -> None:
            """If git is not available, it returns the default LatestTagInfo object, with all None values."""
            # Arrange
            expected = LatestTagInfo()

            # Act
            with inside_dir(tmp_path):
                info = hg_instance.latest_tag_info()

            # Assert
            assert info == expected

        def test_returns_correct_commit_and_tag_info(self, hg_repo: Path, hg_instance: Mercurial) -> None:
            """Should return information that it is a git repo."""
            # Arrange
            tag_prefix = "app/"
            readme = hg_repo.joinpath("readme.md")
            readme.touch()
            hg_instance.config.tag_name = f"{tag_prefix}{{new_version}}"

            # Act
            with inside_dir(hg_repo):
                commit_readme("first")
                tag(f"{tag_prefix}0.1.0", sign=False, message="bumpversion")
                tag_info = hg_instance.latest_tag_info()

            # Assert
            assert tag_info.commit_sha is not None
            assert tag_info.current_version == "0.1.0"
            assert tag_info.current_tag == f"{tag_prefix}0.1.0"
            assert tag_info.distance_to_latest_tag == 0
            assert tag_info.branch_name == "default"
            assert tag_info.short_branch_name == "default"
            assert tag_info.repository_root == hg_repo
            assert tag_info.dirty is False

    class TestAddPath:
        """Tests for the add_path method in the Mercurial class."""

        def test_adds_to_repo_if_file_is_within_repo(self, hg_repo: Path, hg_instance: Mercurial):
            """The file is added to the repo when it is within the repo root."""
            # Arrange
            new_file = hg_repo / "newfile.txt"
            new_file.write_text("new file")

            # Act
            with inside_dir(hg_repo):
                hg_instance.add_path(new_file)
                result = run_command(["hg", "status"])

            # Assert
            assert result.stdout == "A newfile.txt\n"

        @patch("bumpversion.scm.hg.run_command")
        def test_does_not_add_path_when_not_in_repository(
            self, mock_run_command, hg_repo: Path, hg_instance: Mercurial, fixtures_path: Path
        ):
            """The file is not added to the repo when it is outside the repo root."""
            # Arrange
            new_file = fixtures_path / "basic_cfg.toml"

            # Act
            with inside_dir(hg_repo):
                hg_instance.add_path(new_file)

            mock_run_command.assert_called_once_with(["hg", "root"])

    class TestGetAllTags:
        """Tests for the get_all_tags method."""

        def test_returns_correct_tags(self, hg_repo: Path, hg_instance: Mercurial):
            """Returns all the tags in the repo."""
            # Arrange
            readme = hg_repo.joinpath("readme.md")
            readme.touch()
            file1 = hg_repo.joinpath("file1.txt")
            file1.touch()
            file2 = hg_repo.joinpath("file2.txt")
            file2.touch()
            with inside_dir(hg_repo):
                commit_readme("first")
                tag("tag1")
                hg_instance.add_path(file1)
                run_command(["hg", "commit", "-m", "add file1"])
                tag("tag2")
                hg_instance.add_path(file2)
                run_command(["hg", "commit", "-m", "add file2"])
                tag("tag3")

                # Act
                tags = hg_instance.get_all_tags()

            # Assert
            assert set(tags) == {"tip", "tag1", "tag2", "tag3"}

        def test_handles_empty_tags(self, hg_repo: Path, hg_instance: Mercurial):
            """When there are no tags, an empty list is returned."""
            # Arrange
            with inside_dir(hg_repo):
                hg_repo.joinpath("readme.md").touch()
                commit_readme("first")

                # Act
                tags = hg_instance.get_all_tags()

            # Assert
            assert set(tags) == {"tip"}

        @pytest.mark.parametrize(
            ["side_effect"],
            [
                param(subprocess.CalledProcessError(1, "cmd"), id="command failure"),
                param(FileNotFoundError, id="file not found"),
                param(PermissionError, id="permission error"),
            ],
        )
        def test_failure_raises_error(self, hg_instance, side_effect, mocker):
            """On failure, it raises a BumpVersionError exception."""
            # Arrange
            mocker.patch("bumpversion.utils.run_command", side_effect=side_effect)

            # Act, Assert
            with pytest.raises(BumpVersionError):
                hg_instance.get_all_tags()


@pytest.mark.skipif(not shutil.which("hg"), reason="Mercurial is not available.")
def test_hg_bump_version_commits_changes(hg_repo: Path, fixtures_path: Path, runner) -> None:
    """Should commit changes to the repo when configured."""
    dest_cfg = hg_repo / ".bumpversion.toml"
    dest_cfg.write_text(BASIC_CONFIG)

    with inside_dir(hg_repo):
        run_command(["hg", "add", ".bumpversion.toml"])
        run_command(["hg", "commit", "-m", "add configuration"])
        runner.invoke(
            cli.cli,
            ["bump", "minor", "-vv"],
        )
        hg_result = run_command(["hg", "tags", "-T", "json"])

    hg_logs = json.loads(hg_result.stdout)
    tags = [item["tag"] for item in hg_logs]
    assert "v1.1.0" in tags


class TestAssertNonDirty:
    """Tests for the assert_nondirty function."""

    def test_recognizes_clean_working_directory(self, hg_repo: Path):
        """A clean repo does not raise an exception."""
        with inside_dir(hg_repo):
            assert_nondirty()

    def test_dirty_working_directory_raises_exception(self, hg_repo: Path):
        """A dirty working directory raises an exception."""
        # Arrange
        readme = hg_repo.joinpath("readme.md")
        readme.touch()
        with inside_dir(hg_repo):
            commit_readme("first")
            readme.write_text("new text")
            with pytest.raises(DirtyWorkingDirectoryError) as exc:
                assert_nondirty()

        assert "Mercurial working directory is not clean" in str(exc.value)
        assert "M readme.md" in str(exc.value)
