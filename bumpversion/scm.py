"""Version control system management."""

import logging
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import TYPE_CHECKING, ChainMap, List, Optional, Type, Union

if TYPE_CHECKING:
    from bumpversion.config import Config

from bumpversion.exceptions import DirtyWorkingDirectoryError, SignedTagsError

logger = logging.getLogger(__name__)


@dataclass
class SCMInfo:
    """Information about the current source code manager and state."""

    tool: Optional[Type["BaseVCS"]] = None
    commit_sha: Optional[str] = None
    distance_to_latest_tag: Optional[int] = None
    current_version: Optional[str] = None
    dirty: Optional[bool] = None


class BaseVCS:
    """Base class for version control systems."""

    _TEST_USABLE_COMMAND: List[str] = []
    _COMMIT_COMMAND: List[str] = []

    @classmethod
    def commit(cls, message: str, current_version: str, new_version: str, extra_args: Optional[list] = None) -> None:
        """Commit the changes."""
        extra_args = extra_args or []

        with NamedTemporaryFile("wb", delete=False) as f:
            f.write(message.encode("utf-8"))

        env = os.environ.copy()
        env["HGENCODING"] = "utf-8"
        env["BUMPVERSION_CURRENT_VERSION"] = current_version
        env["BUMPVERSION_NEW_VERSION"] = new_version

        try:
            subprocess.check_output([*cls._COMMIT_COMMAND, f.name, *extra_args], env=env)
        except subprocess.CalledProcessError as exc:
            err_msg = f"Failed to run {exc.cmd}: return code {exc.returncode}, output: {exc.output}"
            logger.exception(err_msg)
            raise exc
        finally:
            os.unlink(f.name)

    @classmethod
    def is_usable(cls) -> bool:
        """Is the VCS implementation usable."""
        try:
            result = subprocess.run(cls._TEST_USABLE_COMMAND, check=True)
            return result.returncode == 0
        except (FileNotFoundError, PermissionError, NotADirectoryError, subprocess.CalledProcessError):
            return False

    @classmethod
    def assert_nondirty(cls) -> None:
        """Assert that the working directory is not dirty."""
        raise NotImplementedError()

    @classmethod
    def latest_tag_info(cls, tag_pattern: str) -> SCMInfo:
        """Return information about the latest tag."""
        raise NotImplementedError()

    @classmethod
    def add_path(cls, path: Union[str, Path]) -> None:
        """Add a path to the VCS."""
        raise NotImplementedError()

    @classmethod
    def tag(cls, name: str, sign: bool = False, message: Optional[str] = None) -> None:
        """Create a tag of the new_version in VCS."""
        raise NotImplementedError

    @classmethod
    def commit_to_scm(
        cls,
        files: List[Union[str, Path]],
        config: "Config",
        context: ChainMap,
        extra_args: Optional[List[str]] = None,
        dry_run: bool = False,
    ) -> None:
        """Commit the files to the source code management system."""
        if not cls.is_usable():
            logger.error("SCM tool '%s' is unusable, unable to commit.", cls.__name__)
        do_commit = config.commit and not dry_run
        logger.info(
            "%s %s commit",
            "Preparing" if do_commit else "Would prepare",
            cls.__name__,
        )
        for path in files:
            logger.info(
                "%s changes in file '%s' to %s",
                "Adding" if do_commit else "Would add",
                path,
                cls.__name__,
            )

            if do_commit:
                cls.add_path(path)

        commit_message = config.message.format(**context)

        logger.info(
            "%s to %s with message '%s'",
            "Committing" if do_commit else "Would commit",
            cls.__name__,
            commit_message,
        )
        if do_commit:
            cls.commit(
                message=commit_message,
                current_version=context["current_version"],
                new_version=context["new_version"],
                extra_args=extra_args,
            )

    @classmethod
    def tag_in_scm(cls, config: "Config", context: ChainMap, dry_run: bool = False) -> None:
        """Tag the current commit in the source code management system."""
        sign_tags = config.sign_tags
        tag_name = config.tag_name.format(**context)
        tag_message = config.tag_message.format(**context)
        do_tag = config.tag and not dry_run
        logger.info(
            "%s '%s' %s in %s and %s",
            "Tagging" if do_tag else "Would tag",
            tag_name,
            f"with message '{tag_message}'" if tag_message else "without message",
            cls.__name__,
            "signing" if sign_tags else "not signing",
        )
        if do_tag:
            cls.tag(tag_name, sign_tags, tag_message)


class Git(BaseVCS):
    """Git implementation."""

    _TEST_USABLE_COMMAND = ["git", "rev-parse", "--git-dir"]
    _COMMIT_COMMAND = ["git", "commit", "-F"]

    @classmethod
    def assert_nondirty(cls) -> None:
        """Assert that the working directory is not dirty."""
        lines = [
            line.strip()
            for line in subprocess.check_output(["git", "status", "--porcelain"]).splitlines()
            if not line.strip().startswith(b"??")
        ]

        if lines:
            joined_lines = b"\n".join(lines).decode()
            raise DirtyWorkingDirectoryError(f"Git working directory is not clean:\n{joined_lines}")

    @classmethod
    def latest_tag_info(cls, tag_pattern: str) -> SCMInfo:
        """Return information about the latest tag."""
        try:
            # git-describe doesn't update the git-index, so we do that
            subprocess.run(["git", "update-index", "--refresh"], check=True)

            # get info about the latest tag in git
            # TODO: This only works if the tag name is prefixed with `v`.
            #   Should allow for the configured format for the tag name.
            git_cmd = [
                "git",
                "describe",
                "--dirty",
                "--tags",
                "--long",
                "--abbrev=40",
                f"--match={tag_pattern}",
            ]
            result = subprocess.run(git_cmd, text=True, check=True, capture_output=True)
            describe_out = result.stdout.strip().split("-")
        except subprocess.CalledProcessError:
            logger.debug("Error when running git describe")
            return SCMInfo(tool=cls)

        info = SCMInfo()

        if describe_out[-1].strip() == "dirty":
            info.dirty = True
            describe_out.pop()
        else:
            info.dirty = False

        info.commit_sha = describe_out.pop().lstrip("g")
        info.distance_to_latest_tag = int(describe_out.pop())
        info.current_version = "-".join(describe_out).lstrip("v")

        return info

    @classmethod
    def add_path(cls, path: Union[str, Path]) -> None:
        """Add a path to the VCS."""
        subprocess.check_output(["git", "add", "--update", str(path)])

    @classmethod
    def tag(cls, name: str, sign: bool = False, message: Optional[str] = None) -> None:
        """
        Create a tag of the new_version in VCS.

        If only name is given, bumpversion uses a lightweight tag.
        Otherwise, it utilizes an annotated tag.

        Args:
            name: The name of the tag
            sign: True to sign the tag
            message: A optional message to annotate the tag.
        """
        command = ["git", "tag", name]
        if sign:
            command += ["--sign"]
        if message:
            command += ["--message", message]
        subprocess.check_output(command)


class Mercurial(BaseVCS):
    """Mercurial implementation."""

    _TEST_USABLE_COMMAND = ["hg", "root"]
    _COMMIT_COMMAND = ["hg", "commit", "--logfile"]

    @classmethod
    def latest_tag_info(cls, tag_pattern: str) -> SCMInfo:
        """Return information about the latest tag."""
        return SCMInfo(tool=cls)

    @classmethod
    def assert_nondirty(cls) -> None:
        """Assert that the working directory is clean."""
        lines = [
            line.strip()
            for line in subprocess.check_output(["hg", "status", "-mard"]).splitlines()
            if not line.strip().startswith(b"??")
        ]

        if lines:
            joined_lines = b"\n".join(lines).decode()
            raise DirtyWorkingDirectoryError(f"Mercurial working directory is not clean:\n{joined_lines}")

    @classmethod
    def add_path(cls, path: Union[str, Path]) -> None:
        """Add a path to the VCS."""
        pass

    @classmethod
    def tag(cls, name: str, sign: bool = False, message: Optional[str] = None) -> None:
        """
        Create a tag of the new_version in VCS.

        If only name is given, bumpversion uses a lightweight tag.
        Otherwise, it utilizes an annotated tag.

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
        subprocess.check_output(command)


def get_scm_info(tag_pattern: str) -> SCMInfo:
    """Return a dict with the latest source code management info."""
    if Git.is_usable():
        return Git.latest_tag_info(tag_pattern)
    elif Mercurial.is_usable():
        return Mercurial.latest_tag_info(tag_pattern)
    else:
        return SCMInfo()
