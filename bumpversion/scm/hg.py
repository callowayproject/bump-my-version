"""Mercurial source control management."""

import subprocess
from typing import ClassVar, List, MutableMapping, Optional

from bumpversion.exceptions import DirtyWorkingDirectoryError, SignedTagsError
from bumpversion.scm.models import LatestTagInfo, SCMConfig
from bumpversion.ui import get_indented_logger
from bumpversion.utils import Pathlike, run_command

logger = get_indented_logger(__name__)


class Mercurial:
    """Mercurial source control management."""

    _TEST_AVAILABLE_COMMAND: ClassVar[List[str]] = ["hg", "root"]
    _COMMIT_COMMAND: ClassVar[List[str]] = ["hg", "commit", "--logfile"]
    _ALL_TAGS_COMMAND: ClassVar[List[str]] = ["hg", "log", '--rev="tag()"', '--template="{tags}\n"']

    def __init__(self, config: SCMConfig):
        self.config = config
        self._latest_tag_info: Optional[LatestTagInfo] = None

    def __repr__(self) -> str:
        """Return a string representation of the SCMTool."""
        return self.__str__()

    def __str__(self) -> str:
        """A string representation of the object."""
        return "Mercurial"

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

        info = commit_info(self.config)
        self._latest_tag_info = LatestTagInfo(**info)
        return self._latest_tag_info

    def add_path(self, path: Pathlike) -> None:
        """Add a path to the Source Control Management repository."""
        pass

    def commit_and_tag(self, files: List[Pathlike], context: MutableMapping, dry_run: bool = False) -> None:
        """Commit and tag files to the repository using the configuration."""

    def tag(self, name: str, sign: bool = False, message: Optional[str] = None) -> None:
        """
        Create a tag of the new_version in VCS.

        If only name is given, bumpversion uses a lightweight tag.
        Otherwise, it uses an annotated tag.

        Args:
            name: The name of the tag
            sign: True to sign the tag
            message: A optional message to annotate the tag.

        Raises:
            SignedTagsError: If ``sign`` is ``True``
        """
        command = ["hg", "tag", name]
        if sign:
            raise SignedTagsError("Mercurial does not support signed tags.")
        if message:
            command += ["--message", message]
        run_command(command)

    def assert_nondirty(self) -> None:
        """Assert that the working directory is clean."""
        assert_nondirty()


def commit_info(config: SCMConfig) -> dict:
    """
    Get the commit info for the repo.

    Args:
        config: The source control configuration.

    Returns:
        A dictionary containing information about the latest commit.
    """
    tag_pattern = config.tag_name.replace("{new_version}", ".*")
    info = dict.fromkeys(["dirty", "commit_sha", "distance_to_latest_tag", "current_version", "current_tag"])
    info["distance_to_latest_tag"] = 0
    result = run_command(["hg", "log", "-r", f"tag('re:{tag_pattern}')", "--template", "{latesttag}\n"])
    result.check_returncode()

    if result.stdout:
        tag_string = result.stdout.splitlines(keepends=False)[-1]
        info["current_version"] = config.get_version_from_tag(tag_string)
    else:
        logger.debug("No tags found")

    info["dirty"] = len(run_command(["hg", "status", "-mard"]).stdout) != 0
    return info


def tag(name: str, sign: bool = False, message: Optional[str] = None) -> None:
    """
    Create a tag of the new_version in VCS.

    If only name is given, bumpversion uses a lightweight tag.
    Otherwise, it uses an annotated tag.

    Args:
        name: The name of the tag
        sign: True to sign the tag
        message: A optional message to annotate the tag.

    Raises:
        SignedTagsError: If ``sign`` is ``True``
    """
    command = ["hg", "tag", name]
    if sign:
        raise SignedTagsError("Mercurial does not support signed tags.")
    if message:
        command += ["--message", message]
    run_command(command)


def assert_nondirty() -> None:
    """Assert that the working directory is clean."""
    print(run_command(["hg", "status", "-mard"]).stdout.splitlines())
    if lines := [
        line.strip()
        for line in run_command(["hg", "status", "-mard"]).stdout.splitlines()
        if not line.strip().startswith("??")
    ]:
        joined_lines = "\n".join(lines)
        raise DirtyWorkingDirectoryError(f"Mercurial working directory is not clean:\n{joined_lines}")
