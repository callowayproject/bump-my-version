"""Mercurial source control management."""

import json
import os
import re
import shlex
import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import ClassVar, List, MutableMapping, Optional

from bumpversion.exceptions import DirtyWorkingDirectoryError, SignedTagsError
from bumpversion.scm.models import LatestTagInfo, SCMConfig
from bumpversion.ui import get_indented_logger
from bumpversion.utils import Pathlike, format_and_raise_error, is_subpath, run_command

logger = get_indented_logger(__name__)


class Mercurial:
    """Mercurial source control management."""

    _TEST_AVAILABLE_COMMAND: ClassVar[List[str]] = ["hg", "root"]
    _COMMIT_COMMAND: ClassVar[List[str]] = ["hg", "commit", "--logfile"]

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

    def get_all_tags(self) -> List[str]:
        """Return all tags in a mercurial repository."""
        try:
            result = run_command(["hg", "tags", "-T", "json"])
            tags = json.loads(result.stdout) if result.stdout else []
            return [tag["tag"] for tag in tags]
        except (
            FileNotFoundError,
            PermissionError,
            NotADirectoryError,
            subprocess.CalledProcessError,
        ) as e:
            format_and_raise_error(e)
            return []

    def add_path(self, path: Pathlike) -> None:
        """Add a path to the Source Control Management repository."""
        repository_root = self.latest_tag_info().repository_root
        if not (repository_root and is_subpath(repository_root, path)):
            return

        cwd = Path.cwd()
        temp_path = os.path.relpath(path, cwd)
        try:
            run_command(["hg", "add", str(temp_path)])
        except subprocess.CalledProcessError as e:  # pragma: no-cover
            format_and_raise_error(e)

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

            # for m_tag_name in self.config.moveable_tags:
            #     moveable_tag(m_tag_name)

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

    @staticmethod
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
        tag(name, sign=sign, message=message)

    @staticmethod
    def assert_nondirty() -> None:
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
    info = dict.fromkeys(
        [
            "dirty",
            "commit_sha",
            "short_commit_sha",
            "distance_to_latest_tag",
            "current_version",
            "current_tag",
            "branch_name",
            "short_branch_name",
            "repository_root",
        ]
    )

    info["distance_to_latest_tag"] = 0
    result = run_command(["hg", "log", "-r", f"last(tag('re:{tag_pattern}') - tip)", "-T", "json"])
    repo_path = run_command(["hg", "root"]).stdout.strip()

    output_info = parse_commit_log(result.stdout, config)
    info |= output_info

    if not output_info:
        logger.debug("No tags found")

    info["repository_root"] = Path(repo_path)
    info["dirty"] = len(run_command(["hg", "status", "-mard"]).stdout) != 0
    return info


def parse_commit_log(log_string: str, config: SCMConfig) -> dict:
    """Parse the commit log string."""
    output_info = json.loads(log_string) if log_string else {}
    if not output_info:
        return {}
    first_rev = output_info[0]
    branch_name = first_rev["branch"]
    short_branch_name = re.sub(r"([^a-zA-Z0-9]*)", "", branch_name).lower()[:20]

    return {
        "current_version": config.get_version_from_tag(first_rev["tags"][0]),
        "current_tag": first_rev["tags"][0],
        "commit_sha": first_rev["node"],
        "short_commit_sha": first_rev["node"][:7],
        "distance_to_latest_tag": 0,
        "branch_name": branch_name,
        "short_branch_name": short_branch_name,
    }


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
    if lines := [
        line.strip()
        for line in run_command(["hg", "status", "-mard"]).stdout.splitlines()
        if not line.strip().startswith("??")
    ]:
        joined_lines = "\n".join(lines)
        raise DirtyWorkingDirectoryError(f"Mercurial working directory is not clean:\n{joined_lines}")
