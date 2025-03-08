"""Git source control management implementation."""

import os
import re
import shlex
import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, ClassVar, List, MutableMapping, Optional

from bumpversion.exceptions import DirtyWorkingDirectoryError
from bumpversion.scm.models import LatestTagInfo, SCMConfig
from bumpversion.ui import get_indented_logger
from bumpversion.utils import Pathlike, format_and_raise_error, is_subpath, run_command

logger = get_indented_logger(__name__)


class Git:
    """Git implementation."""

    _TEST_AVAILABLE_COMMAND: ClassVar[List[str]] = ["git", "rev-parse", "--git-dir"]
    _COMMIT_COMMAND: ClassVar[List[str]] = ["git", "commit", "-F"]
    _ALL_TAGS_COMMAND: ClassVar[List[str]] = ["git", "tag", "--list"]

    def __init__(self, config: SCMConfig):
        self.config = config
        self._latest_tag_info: Optional[LatestTagInfo] = None

    def __repr__(self) -> str:
        """Return a string representation of the SCMTool."""
        return self.__str__()

    def __str__(self) -> str:
        """A string representation of the object."""
        return "Git"

    def is_available(self) -> bool:
        """Is the VCS implementation usable?"""
        try:
            result = run_command(self._TEST_AVAILABLE_COMMAND)
            return result.returncode == 0
        except (FileNotFoundError, PermissionError, NotADirectoryError, subprocess.CalledProcessError):
            return False

    def latest_tag_info(self) -> LatestTagInfo:
        """Return information about the latest tag."""
        if self._latest_tag_info is not None:
            return self._latest_tag_info

        if not self.is_available():
            return LatestTagInfo()

        info: dict[str, Any] = {}
        update_index()

        info |= commit_info(self.config)
        info |= revision_info()

        self._latest_tag_info = LatestTagInfo(**info)
        return self._latest_tag_info

    def add_path(self, path: Pathlike) -> None:
        """Add a path to the VCS."""
        repository_root = self.latest_tag_info().repository_root
        if not (repository_root and is_subpath(repository_root, path)):
            return

        cwd = Path.cwd()
        temp_path = os.path.relpath(path, cwd)
        try:
            run_command(["git", "add", "--update", str(temp_path)])
        except subprocess.CalledProcessError as e:
            format_and_raise_error(e)

    def get_all_tags(self) -> List[str]:
        """Return all tags in git."""
        try:
            result = run_command(self._ALL_TAGS_COMMAND)
            return result.stdout.splitlines()
        except (  # pragma: no-coverage
            FileNotFoundError,
            PermissionError,
            NotADirectoryError,
            subprocess.CalledProcessError,
        ):
            return []

    def commit_and_tag(self, files: List[Pathlike], context: MutableMapping, dry_run: bool = False) -> None:
        """Commit and tag files to the repository using the configuration."""
        if dry_run:
            return

        if self.config.commit:
            for path in files:
                self.add_path(path)

            self.commit(context)

        if self.config.tag:
            tag_name = self.config.tag_name.format(**context)
            tag_message = self.config.tag_message.format(**context)
            tag(tag_name, sign=self.config.sign_tags, message=tag_message)

            for m_tag_name in self.config.moveable_tags:
                moveable_tag(m_tag_name)

    def assert_nondirty(self) -> None:
        """
        Asserts that the repository is not dirty.

        Raises:
            DirtyWorkingDirectoryError: If the repository is not clean.
        """
        assert_nondirty()

    def commit(self, context: MutableMapping) -> None:
        """Commit the changes."""
        extra_args = shlex.split(self.config.commit_args) if self.config.commit_args else []

        current_version = context.get("current_version", "")
        new_version = context.get("new_version", "")
        commit_message = self.config.message.format(**context)

        if not current_version:  # pragma: no-coverage
            logger.warning("No current version given, using an empty string.")
        if not new_version:  # pragma: no-coverage
            logger.warning("No new version given, using an empty string.")

        with NamedTemporaryFile("wb", delete=False) as f:
            f.write(commit_message.encode("utf-8"))

        env = os.environ.copy()
        env["BUMPVERSION_CURRENT_VERSION"] = current_version
        env["BUMPVERSION_NEW_VERSION"] = new_version

        try:
            cmd = [*self._COMMIT_COMMAND, f.name, *extra_args]
            run_command(cmd, env=env)
        except (subprocess.CalledProcessError, TypeError) as exc:  # pragma: no-coverage
            format_and_raise_error(exc)
        finally:
            os.unlink(f.name)


def update_index() -> None:
    """Update the git index."""
    try:
        run_command(["git", "update-index", "--refresh", "-q"])
    except subprocess.CalledProcessError as e:
        logger.debug("Error when running git update-index: %s", e.stderr)


def commit_info(config: SCMConfig) -> dict:
    """
    Get the commit info for the repo.

    Args:
        config: The source control configuration.

    Returns:
        A dictionary containing information about the latest commit.
    """
    tag_pattern = config.tag_name.replace("{new_version}", "*")
    info = dict.fromkeys(["dirty", "commit_sha", "distance_to_latest_tag", "current_version", "current_tag"])
    info["distance_to_latest_tag"] = 0
    try:
        git_cmd = ["git", "describe", "--dirty", "--tags", "--long", "--abbrev=40", f"--match={tag_pattern}"]
        result = run_command(git_cmd)
    except subprocess.CalledProcessError as e:
        if e.stderr and "fatal: no names found, cannot describe anything." in e.stderr:
            logger.debug("No tags found, returning default values.")
        else:
            logger.debug("Error when running git describe: %s", e.stderr)
        return info

    describe_out = result.stdout.strip().split("-")
    if describe_out[-1].strip() == "dirty":
        info["dirty"] = True
        describe_out.pop()
    else:
        info["dirty"] = False

    info["commit_sha"] = describe_out.pop().lstrip("g")
    info["distance_to_latest_tag"] = int(describe_out.pop())
    info["current_tag"] = "-".join(describe_out)
    version = config.get_version_from_tag("-".join(describe_out))
    info["current_version"] = version or "-".join(describe_out).lstrip("v")

    return info


def revision_info() -> dict:
    """
    Returns a dictionary containing revision information.

    If an error occurs while running the git command, the dictionary values will be set to None.

    Returns:
        A dictionary with the following keys:
            - branch_name: The name of the current branch.
            - short_branch_name: A 20 lowercase characters of the branch name with special characters removed.
            - repository_root: The root directory of the Git repository.
    """
    info = dict.fromkeys(["branch_name", "short_branch_name", "repository_root"])
    repo_root_command = ["git", "rev-parse", "--show-toplevel"]
    current_branch_command = ["git", "branch", "--show-current"]

    try:
        repository_root_result = run_command(repo_root_command)
    except subprocess.CalledProcessError as e:
        logger.debug("Error when determining the repository root: %s", e.stderr)
        return info

    try:
        branch_name_result = run_command(current_branch_command)
    except subprocess.CalledProcessError as e:
        logger.debug("Error when determining the current branch: %s", e.stderr)
        return info

    repository_root = Path(repository_root_result.stdout.strip())
    branch_name = branch_name_result.stdout.strip()
    short_branch_name = re.sub(r"([^a-zA-Z0-9]*)", "", branch_name).lower()[:20]
    info["branch_name"] = branch_name
    info["short_branch_name"] = short_branch_name
    info["repository_root"] = repository_root

    return info


def tag(name: str, sign: bool = False, message: Optional[str] = None) -> None:
    """
    Create a tag of the new_version in git.

    If only name is given, bumpversion uses a lightweight tag.
    Otherwise, it uses an annotated tag.

    Args:
        name: The name of the tag
        sign: True to sign the tag
        message: An optional message to annotate the tag.
    """
    command = ["git", "tag", name]
    if sign:
        command += ["--sign"]
    if message:
        command += ["--message", message]
    try:
        run_command(command)
    except subprocess.CalledProcessError as e:
        format_and_raise_error(e)


def moveable_tag(name: str) -> None:
    """
    Create a new lightweight tag that should overwrite any previous tags with the same name.

    Args:
        name: The name of the moveable tag.
    """
    try:
        run_command(["git", "tag", "-f", name])
        push_remote("origin", name, force=True)
    except subprocess.CalledProcessError as e:
        format_and_raise_error(e)


def assert_nondirty() -> None:
    """Assert that the working directory is not dirty."""
    lines = [
        line.strip()
        for line in run_command(["git", "status", "--porcelain"]).stdout.splitlines()
        if not line.strip().startswith("??")
    ]
    if joined_lines := "\n".join(lines):
        raise DirtyWorkingDirectoryError(f"Git working directory is not clean:\n\n{joined_lines}")


def push_remote(remote_name: str, ref_name: str, force: bool = False) -> None:
    """Push the `ref_name` to the `remote_name` repository, optionally forcing the push."""
    try:
        result = run_command(["git", "remote"])
        if remote_name not in result.stdout:
            logger.warning("Remote '%s' not found, skipping push.", remote_name)
            return
        run_command(["git", "push", remote_name, ref_name, "--force" if force else ""])
    except subprocess.CalledProcessError as e:
        format_and_raise_error(e)
