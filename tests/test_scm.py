"""Tests of the VCS module."""

import logging
import shutil
import subprocess
from pathlib import Path

import pytest
from pytest import param, LogCaptureFixture

from bumpversion import scm
from bumpversion.exceptions import DirtyWorkingDirectoryError, BumpVersionError
from bumpversion.ui import setup_logging
from bumpversion.utils import run_command
from tests.conftest import get_config_data, inside_dir


class TestSourceCodeManager:
    """Tests related to SourceCodeManager."""

    class TestGetVersionFromTag:
        """Tests for the get_version_from_tag classmethod."""

        simple_pattern = r"(?P<major>\\d+)\\.(?P<minor>\\d+)\.(?P<patch>\\d+)"
        complex_pattern = r"(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+)(-(?P<release>[0-9A-Za-z]+))?(\\+build\\.(?P<build>.[0-9A-Za-z]+))?"

        @pytest.mark.parametrize(
            ["tag", "tag_name", "parse_pattern", "expected"],
            [
                param("1.2.3", "{new_version}", simple_pattern, "1.2.3", id="no-prefix, no-suffix"),
                param("v/1.2.3", "v/{new_version}", simple_pattern, "1.2.3", id="prefix, no-suffix"),
                param("v/1.2.3/12345", "v/{new_version}/{something}", simple_pattern, "1.2.3", id="prefix, suffix"),
                param("1.2.3/2024-01-01", "{new_version}/{today}", simple_pattern, "1.2.3", id="no-prefix, suffix"),
                param(
                    "app/4.0.3-beta+build.1047",
                    "app/{new_version}",
                    complex_pattern,
                    "4.0.3-beta+build.1047",
                    id="complex",
                ),
            ],
        )
        def returns_version_from_pattern(self, tag: str, tag_name: str, parse_pattern: str, expected: str) -> None:
            """It properly returns the version from the tag."""
            # Act
            version = scm.SourceCodeManager.get_version_from_tag(tag, tag_name, parse_pattern)

            # Assert
            assert version == expected

    def test_format_and_raise_error_returns_scm_error(self, git_repo: Path) -> None:
        """The output formatting from called process error string includes the underlying scm error."""
        with inside_dir(git_repo):
            try:
                run_command(["git", "add", "newfile.txt"])
            except subprocess.CalledProcessError as e:
                with pytest.raises(BumpVersionError) as bump_error:
                    scm.Git.format_and_raise_error(e)
                assert bump_error.value.message == (
                    "Failed to run `git add newfile.txt`: return code 128, output: "
                    "fatal: pathspec 'newfile.txt' did not match any files\n"
                )


class TestGit:
    """Tests related to Git."""

    class TestIsUsable:
        """Tests related to is_usable."""

        def test_recognizes_a_git_repo(self, git_repo: Path) -> None:
            """Should return true if git is available, and it is a git repo."""
            with inside_dir(git_repo):
                assert scm.Git.is_usable()

        def test_recognizes_not_a_git_repo(self, tmp_path: Path) -> None:
            """Should return false if it is not a git repo."""
            with inside_dir(tmp_path):
                assert not scm.Git.is_usable()

    class TestAssertNonDirty:
        """Tests for the Git.assert_nondirty() function."""

        def test_does_nothing_when_not_dirty(self, git_repo: Path) -> None:
            """If the git repo is clean, assert_nondirty should do nothing."""
            with inside_dir(git_repo):
                scm.Git.assert_nondirty()

        def test_raises_error_when_dirty(self, git_repo: Path) -> None:
            """If the git repo has modified files, assert_nondirty should return false."""
            readme = git_repo.joinpath("readme.md")
            readme.touch()
            with pytest.raises(DirtyWorkingDirectoryError):
                with inside_dir(git_repo):
                    subprocess.run(["git", "add", "readme.md"])
                    scm.Git.assert_nondirty()

    class TestLatestTagInfo:
        """Test for the Git.latest_tag_info() function."""

        def test_an_empty_repo_only_fills_tool_info(self, git_repo: Path) -> None:
            """
            If the repo is empty, the info only includes the tool type.

            The git commands to get all the other information depend on there being a `HEAD` object.
            """
            tag_prefix = "app/"
            parse_pattern = r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)"
            tag_name = f"{tag_prefix}{{new_version}}"
            expected = scm.SCMInfo(
                tool=scm.Git,
                commit_sha=None,
                distance_to_latest_tag=0,
                current_version=None,
                branch_name=None,
                short_branch_name=None,
                repository_root=None,
                dirty=None,
            )
            with inside_dir(git_repo):
                latest_tag_info = scm.Git.latest_tag_info(tag_name, parse_pattern=parse_pattern)
                assert latest_tag_info == expected

        def test_returns_commit_and_tag_info(self, git_repo: Path) -> None:
            """Should return information that it is a git repo."""
            tag_prefix = "app/"
            parse_pattern = r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)"
            tag_name = f"{tag_prefix}{{new_version}}"
            readme = git_repo.joinpath("readme.md")
            readme.touch()
            with inside_dir(git_repo):
                # Add a file and tag
                subprocess.run(["git", "add", "readme.md"])
                subprocess.run(["git", "commit", "-m", "first"])
                subprocess.run(["git", "tag", f"{tag_prefix}0.1.0"])
                tag_info = scm.Git.latest_tag_info(tag_name, parse_pattern=parse_pattern)
                assert tag_info.commit_sha is not None
                assert tag_info.current_version == "0.1.0"
                assert tag_info.current_tag == f"{tag_prefix}0.1.0"
                assert tag_info.distance_to_latest_tag == 0
                assert tag_info.branch_name == "master"
                assert tag_info.short_branch_name == "master"
                assert tag_info.repository_root == git_repo
                assert tag_info.dirty is False


def test_git_detects_existing_tag(git_repo: Path, caplog: LogCaptureFixture) -> None:
    """Attempting to tag when a tag exists will do nothing."""
    # Arrange
    git_repo.joinpath("readme.md").touch()
    git_repo.joinpath("something.md").touch()
    overrides = {"current_version": "0.1.0", "commit": True, "tag": True}
    context = {
        "current_version": "0.1.0",
        "new_version": "0.2.0",
    }
    setup_logging(2)
    with inside_dir(git_repo):
        conf, version_config, current_version = get_config_data(overrides)
        subprocess.run(["git", "add", "readme.md"])
        subprocess.run(["git", "commit", "-m", "first"])
        subprocess.run(["git", "tag", "v0.1.0"])
        subprocess.run(["git", "add", "something.md"])
        subprocess.run(["git", "commit", "-m", "second"])
        subprocess.run(["git", "tag", "v0.2.0"])

        # Act
        scm.Git.tag_in_scm(config=conf, context=context)

    # Assert
    assert "Will not tag" in caplog.text


def test_hg_is_not_usable(tmp_path: Path) -> None:
    """Should return false if it is not a mercurial repo."""
    with inside_dir(tmp_path):
        assert not scm.Mercurial.is_usable()


@pytest.mark.skipif(not shutil.which("hg"), reason="Mercurial is not available.")
def test_hg_is_usable(hg_repo: Path) -> None:
    """Should return false if it is not a mercurial repo."""
    with inside_dir(hg_repo):
        assert scm.Mercurial.is_usable()


@pytest.mark.parametrize(
    ["repo", "scm_command", "scm_class"],
    [
        param(
            "git_repo",
            "git",
            scm.Git,
            id="git",
            marks=pytest.mark.skipif(not shutil.which("git"), reason="Git is not available."),
        ),
        param(
            "hg_repo",
            "hg",
            scm.Mercurial,
            id="hg",
            marks=pytest.mark.skipif(not shutil.which("hg"), reason="Mercurial is not available."),
        ),
    ],
)
def test_commit_and_tag_from_below_scm_root(repo: str, scm_command: str, scm_class: scm.SourceCodeManager, request):
    # Arrange
    repo_path: Path = request.getfixturevalue(repo)
    version_path = repo_path / "VERSION"
    version_path.write_text("30.0.3", encoding="utf-8")
    sub_dir_path = repo_path / "subdir"
    sub_dir_path.mkdir(exist_ok=True)

    overrides = {"current_version": "30.0.3", "commit": True, "tag": True, "files": [{"filename": str(version_path)}]}
    context = {
        "current_version": "30.0.3",
        "new_version": "30.1.0",
    }
    with inside_dir(repo_path):
        conf, version_config, current_version = get_config_data(overrides)
        subprocess.run([scm_command, "add", "VERSION"], check=True, capture_output=True)
        subprocess.run([scm_command, "commit", "-m", "initial commit"], check=True, capture_output=True)
        with inside_dir(sub_dir_path):
            version_path.write_text("30.1.0", encoding="utf-8")

            # Act
            scm_class.commit_to_scm(files=[version_path], config=conf, context=context)
            scm_class.tag_in_scm(config=conf, context=context)

        # Assert
        tag_info = scm_class.latest_tag_info(conf.tag_name, parse_pattern=conf.parse)
        if scm_command == "git":
            assert tag_info.commit_sha is not None
            assert tag_info.distance_to_latest_tag == 0
        assert tag_info.current_version == "30.1.0"
        assert tag_info.dirty is False


# write tests for no-commit, no-tag and dry-run
@pytest.mark.parametrize(
    ["repo", "scm_command", "scm_class"],
    [
        param(
            "git_repo",
            "git",
            scm.Git,
            id="git",
            marks=pytest.mark.skipif(not shutil.which("git"), reason="Git is not available."),
        ),
        param(
            "hg_repo",
            "hg",
            scm.Mercurial,
            id="hg",
            marks=pytest.mark.skipif(not shutil.which("hg"), reason="Mercurial is not available."),
        ),
    ],
)
@pytest.mark.parametrize(
    ["commit", "tag", "dry_run", "should_commit", "should_tag"],
    [
        param(True, True, True, False, False, id="dry-run-stops-commit-and-tag"),
        param(True, False, False, True, False, id="commit-no-tag"),
        param(False, True, False, False, True, id="no-commit-will-tag"),
    ],
)
def test_commit_tag_dry_run_interactions(
    repo: str,
    scm_command: str,
    scm_class: scm.SourceCodeManager,
    commit: bool,
    tag: bool,
    dry_run: bool,
    should_commit: bool,
    should_tag: bool,
    caplog: LogCaptureFixture,
    request,
):
    """Combinations of commit, tag, dry-run and should produce the expected results."""
    # Arrange
    caplog.set_level(logging.INFO)
    repo_path: Path = request.getfixturevalue(repo)
    version_path = repo_path / "VERSION"
    version_path.write_text("30.0.3", encoding="utf-8")

    overrides = {"current_version": "30.0.3", "commit": commit, "tag": tag, "files": [{"filename": str(version_path)}]}
    context = {
        "current_version": "30.0.3",
        "new_version": "30.1.0",
    }
    with inside_dir(repo_path):
        conf, version_config, current_version = get_config_data(overrides)
        subprocess.run([scm_command, "add", "VERSION"], check=True, capture_output=True)
        subprocess.run([scm_command, "commit", "-m", "initial commit"], check=True, capture_output=True)
        version_path.write_text("30.1.0", encoding="utf-8")
        # Act
        scm_class.commit_to_scm(files=[version_path], config=conf, context=context, dry_run=dry_run)
        scm_class.tag_in_scm(config=conf, context=context, dry_run=dry_run)

        # Assert
        if commit and dry_run:
            assert "Would commit" in caplog.text
        elif should_commit:
            assert "Committing " in caplog.text
        else:
            assert "Would not commit" in caplog.text

        if tag and dry_run:
            assert "Would tag" in caplog.text
        elif should_tag:
            assert "Tagging " in caplog.text
        else:
            assert "Would not tag" in caplog.text
