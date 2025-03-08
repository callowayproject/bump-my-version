"""Data models for source code management functions."""

import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, List, MutableMapping, Optional, Protocol

from bumpversion.ui import get_indented_logger
from bumpversion.utils import Pathlike, extract_regex_flags

logger = get_indented_logger(__name__)

if TYPE_CHECKING:  # pragma: no-coverage
    from bumpversion.config import Config


@dataclass
class SCMConfig:
    """Configuration for source code management functions."""

    tag: bool
    sign_tags: bool
    tag_name: str
    allow_dirty: bool
    commit: bool
    message: str
    parse_pattern: str
    tag_message: Optional[str] = None
    commit_args: Optional[str] = None
    moveable_tags: List[str] = field(default_factory=list)

    def get_version_from_tag(self, tag: str) -> Optional[str]:
        """Return the version from a tag."""
        version_pattern = self.parse_pattern.replace("\\\\", "\\")
        version_pattern, regex_flags = extract_regex_flags(version_pattern)
        parts = self.tag_name.split("{new_version}", maxsplit=1)
        prefix = parts[0]
        # suffix = parts[1]
        rep = f"{regex_flags}{re.escape(prefix)}(?P<current_version>{version_pattern})"
        tag_regex = re.compile(rep)
        return match["current_version"] if (match := tag_regex.search(tag)) else None

    @classmethod
    def from_config(cls, config: "Config") -> "SCMConfig":
        """Return a SCMConfig from a Config object."""
        return cls(
            tag=config.tag,
            tag_name=config.tag_name,
            sign_tags=config.sign_tags,
            allow_dirty=config.allow_dirty,
            commit=config.commit,
            message=config.message,
            parse_pattern=config.parse,
            tag_message=config.tag_message,
            commit_args=config.commit_args,
            moveable_tags=config.moveable_tags,
        )


@dataclass
class LatestTagInfo:
    """Information about the latest tag."""

    commit_sha: Optional[str] = None
    distance_to_latest_tag: int = 0
    current_version: Optional[str] = None
    current_tag: Optional[str] = None
    branch_name: Optional[str] = None
    short_branch_name: Optional[str] = None
    repository_root: Optional[Path] = None
    dirty: Optional[bool] = None


class SCMTool(Protocol):
    """Protocol for source code management tools."""

    def __init__(self, config: SCMConfig): ...

    def is_available(self) -> bool:
        """Return whether the SCM tool is available."""
        ...

    def latest_tag_info(self) -> LatestTagInfo:
        """Return the latest tag information."""
        ...

    def add_path(self, path: Pathlike) -> None:
        """Add a path to the pending commit."""
        ...

    def get_all_tags(self) -> List[str]:
        """Return all tags in the SCM."""
        ...

    def commit_and_tag(self, files: List[Pathlike], context: MutableMapping, dry_run: bool = False) -> None:
        """Commit and tag files to the repository using the configuration."""
        ...

    def assert_nondirty(self) -> None:
        """
        Asserts that the repository is not dirty.

        Raises:
            DirtyWorkingDirectoryError: If the repository is not clean.
        """
        ...


class DefaultSCMTool:
    """Default implementation of the SCMTool protocol."""

    def __init__(self, config: SCMConfig):
        self.config = config

    def __repr__(self) -> str:
        """Return a string representation of the SCMTool."""
        return self.__str__()

    def __str__(self) -> str:
        """A string representation of the object."""
        return "None"

    def is_available(self) -> bool:
        """Return whether the SCM tool is available."""
        return True

    def latest_tag_info(self) -> LatestTagInfo:
        """Return the latest tag information."""
        return LatestTagInfo()

    def add_path(self, path: Pathlike) -> None:
        """Add a path to the pending commit."""
        logger.debug("No source code management system configured. Skipping adding path '%s'.", path)

    def get_all_tags(self) -> List[str]:
        """Return all tags in the SCM."""
        return []

    def commit_and_tag(self, files: List[Pathlike], context: MutableMapping, dry_run: bool = False) -> None:
        """Pretend to commit and tag files to the repository using the configuration."""
        logger.debug("No source code management system configured. Skipping committing and tagging.")

    def assert_nondirty(self) -> None:
        """Always says the repository is clean."""
        return


class SCMInfo:
    """Information about the current source code manager and state."""

    def __init__(self, config: SCMConfig):
        self.config = config
        self.commit_sha: Optional[str] = None
        self.distance_to_latest_tag: int = 0
        self.current_version: Optional[str] = None
        self.current_tag: Optional[str] = None
        self.branch_name: Optional[str] = None
        self.short_branch_name: Optional[str] = None
        self.repository_root: Optional[Path] = None
        self.dirty: Optional[bool] = None
        self.tool: SCMTool = DefaultSCMTool(config)
        self._set_from_scm_tool()

    def __repr__(self) -> str:
        """Return a string representation of the SCMInfo."""
        import pprint
        from io import StringIO

        str_io = StringIO()
        pprint.pprint(self.as_dict(), stream=str_io)
        return str_io.getvalue().rstrip()

    def as_dict(self) -> dict[str, Any]:
        """Return the information as a dict."""
        return {
            "commit_sha": self.commit_sha,
            "distance_to_latest_tag": self.distance_to_latest_tag,
            "current_version": self.current_version,
            "current_tag": self.current_tag,
            "branch_name": self.branch_name,
            "short_branch_name": self.short_branch_name,
            "repository_root": self.repository_root,
            "dirty": self.dirty,
            "tool": self.tool,
        }

    def _set_from_scm_tool(self):
        """Set information from the source code management tool."""
        from bumpversion.scm.git import Git
        from bumpversion.scm.hg import Mercurial

        git = Git(self.config)
        hg = Mercurial(self.config)
        if git.is_available():
            self.tool = git
        elif hg.is_available():
            self.tool = hg
        self._update_from_latest_tag_info(self.tool.latest_tag_info())

    def _update_from_latest_tag_info(self, latest_tag_info: LatestTagInfo):
        """Update information from the latest tag information."""
        for attr_name, value in asdict(latest_tag_info).items():
            setattr(self, attr_name, value)

    def path_in_repo(self, path: Pathlike) -> bool:
        """Return whether a path is inside this repository."""
        if self.repository_root is None:
            return True
        elif not Path(path).is_absolute():
            return True
        return str(path).startswith(str(self.repository_root))

    def commit_and_tag(self, files: List[Pathlike], context: MutableMapping, dry_run: bool = False) -> None:
        """Commit the files to the source code management system."""
        logger.indent()

        if self.config.commit:
            self._commit(files, context, dry_run)
        else:
            logger.info("Would not commit")

        if self.config.tag:
            self._tag(context, dry_run)
        else:
            logger.info("Would not tag")

        self.tool.commit_and_tag(files=files, context=context, dry_run=dry_run)
        logger.dedent()

    def _commit(self, files: List[Pathlike], context: MutableMapping, dry_run: bool = False) -> None:
        """Commit the files to the source code management system."""
        do_commit = not dry_run
        logger.info("%s the commit", "Preparing" if do_commit else "Would prepare")

        for path in files:
            logger.info("%s changes in file '%s' to repository", "Adding" if do_commit else "Would add", path)

        commit_message = self.config.message.format(**context)
        logger.info(
            "%s to repository with message '%s'", "Committing" if do_commit else "Would commit", commit_message
        )

    def _tag(self, context: MutableMapping, dry_run: bool = False) -> None:
        """Tag the current commit in the source code management system."""
        sign_tags = self.config.sign_tags
        tag_name = self.config.tag_name.format(**context)
        tag_message = self.config.tag_message.format(**context)
        existing_tags = self.tool.get_all_tags()
        do_tag = not dry_run

        if tag_name in existing_tags:
            logger.warning("Tag '%s' already exists. Will not tag.", tag_name)
            return

        logger.info(
            "%s '%s' %s to repository and %s",
            "Adding tag" if do_tag else "Would add tag",
            tag_name,
            f"with message '{tag_message}'" if tag_message else "without message",
            "signing" if sign_tags else "not signing",
        )

        for moveable_tag in self.config.moveable_tags:
            tag_name = moveable_tag.format(**context)
            logger.info("%s moveable tag '%s' in repository", "Tagging" if do_tag else "Would tag", tag_name)
