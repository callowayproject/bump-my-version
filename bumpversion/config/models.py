"""Bump My Version configuration models."""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from itertools import chain
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, MutableMapping, Optional, Tuple, Union

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from bumpversion.scm.models import SCMInfo  # ruff: ignore[typing-only-first-party-import]
from bumpversion.ui import get_indented_logger
from bumpversion.versioning.models import VersionComponentSpec  # ruff: ignore[typing-only-first-party-import]

if TYPE_CHECKING:  # pragma: no-coverage
    from bumpversion.versioning.models import VersionSpec
    from bumpversion.versioning.version_config import VersionConfig

logger = get_indented_logger(__name__)


class FileChange(BaseModel):
    """A change to make to a file."""

    parse: str
    serialize: tuple
    search: str
    replace: str
    regex: bool
    ignore_missing_version: bool
    ignore_missing_file: bool
    filename: Optional[str] = None
    glob: Optional[str] = None  # Conflicts with filename. If both are specified, glob wins
    glob_exclude: Optional[tuple] = None
    key_path: Optional[str] = None  # If specified, and has an appropriate extension, will be treated as a data file
    include_bumps: Optional[tuple] = None
    exclude_bumps: tuple = Field(default_factory=tuple)

    def __hash__(self):
        """Return a hash of the model."""
        return hash(tuple(sorted(self.model_dump().items())))

    def get_search_pattern(self, context: MutableMapping) -> Tuple[re.Pattern, str]:
        """
        Render the search pattern and return the compiled regex pattern and the raw pattern.

        Args:
            context: The context to use for rendering the search pattern

        Returns:
            A tuple of the compiled regex pattern and the raw pattern as a string.
        """
        logger.debug("Rendering search pattern with context")
        logger.indent()
        # the default search pattern is escaped, so we can still use it in a regex
        raw_pattern = self.search.format(**context)
        default = re.compile(re.escape(raw_pattern), re.MULTILINE | re.DOTALL)
        if not self.regex:
            logger.debug(
                "No RegEx flag detected. Searching for the default pattern: '%s'",
                default.pattern,
            )
            logger.dedent()
            return default, raw_pattern

        re_context = {key: re.escape(str(value)) for key, value in context.items()}
        regex_pattern = self.search.format(**re_context)
        try:
            search_for_re = re.compile(regex_pattern, re.MULTILINE | re.DOTALL)
            logger.debug("Searching for the regex: '%s'", search_for_re.pattern)
            logger.dedent()
            return search_for_re, raw_pattern
        except re.error as e:
            logger.error("Invalid regex '%s': %s.", default, e)

        logger.debug("Invalid regex. Searching for the default pattern: '%s'", raw_pattern)
        logger.dedent()

        return default, raw_pattern


class Config(BaseSettings):
    """Bump Version configuration."""

    current_version: Optional[str]
    parse: str
    serialize: tuple = Field(min_length=1)
    search: str
    replace: str
    regex: bool
    ignore_missing_version: bool
    ignore_missing_files: bool
    tag: bool
    push_tag: bool
    sign_tags: bool
    tag_name: str
    tag_message: Optional[str]
    allow_dirty: bool
    commit: bool
    message: str
    commit_args: Optional[str]
    pep621_info: Optional[PEP621Info]
    scm_info: Optional[SCMInfo]
    parts: Dict[str, VersionComponentSpec]
    moveable_tags: List[str] = Field(default_factory=list)
    files: List[FileChange] = Field(default_factory=list)
    setup_hooks: List[str] = Field(default_factory=list)
    pre_commit_hooks: List[str] = Field(default_factory=list)
    post_commit_hooks: List[str] = Field(default_factory=list)
    allow_shell_hooks: bool = False
    included_paths: List[str] = Field(default_factory=list)
    excluded_paths: List[str] = Field(default_factory=list)
    model_config = SettingsConfigDict(env_prefix="bumpversion_")
    _resolved_filemap: Optional[Dict[str, List[FileChange]]] = None
    _ignore_unmatched_globs: bool = False

    def add_files(self, filename: Union[str, List[str]]) -> None:
        """Add a filename to the list of files."""
        if not filename:
            return
        filenames = [filename] if isinstance(filename, str) else filename
        files = set(self.files)
        configured = {Path(key).resolve() for key in self.resolved_filemap}
        for name in filenames:
            if Path(name).resolve() in configured:
                continue  # already configured under another spelling; don't process it twice
            files.add(
                FileChange(
                    filename=name,
                    glob=None,
                    key_path=None,
                    parse=self.parse,
                    serialize=self.serialize,
                    search=self.search,
                    replace=self.replace,
                    regex=self.regex,
                    ignore_missing_version=self.ignore_missing_version,
                    ignore_missing_file=self.ignore_missing_files,
                    include_bumps=tuple(self.parts.keys()),
                )
            )
        self.files = list(files)

        self._resolved_filemap = None

    def exclude_configured_files(self) -> None:
        """Exclude all configured files, so only files added later are modified."""
        # Configured files won't be modified, so a glob that matches nothing isn't an error.
        self._ignore_unmatched_globs = True
        self._resolved_filemap = None
        self.excluded_paths = list(self.resolved_filemap.keys())

    @property
    def resolved_filemap(self) -> Dict[str, List[FileChange]]:
        """The cached resolved filemap."""
        if self._resolved_filemap is None:
            self._resolved_filemap = self._resolve_filemap()
        return self._resolved_filemap

    def _resolve_filemap(self) -> Dict[str, List[FileChange]]:
        """Return a map of filenames to file configs, expanding any globs."""
        from bumpversion.config.utils import resolve_glob_files

        output = defaultdict(list)
        new_files = []
        for file_cfg in self.files:
            if file_cfg.glob:
                new_files.extend(resolve_glob_files(file_cfg, ignore_missing=self._ignore_unmatched_globs))
            else:
                new_files.append(file_cfg)

        for file_cfg in new_files:
            output[file_cfg.filename].append(file_cfg)
        return output

    @property
    def files_to_modify(self) -> List[FileChange]:
        """A list of files to modify."""
        # Compare resolved paths: config filenames may be absolute while CLI paths are relative.
        excluded = {Path(p).resolve() for p in self.excluded_paths}
        included = {Path(p).resolve() for p in self.included_paths}
        selected = []
        for key, file_cfg_list in self.resolved_filemap.items():
            resolved = Path(key).resolve()  # once per key
            if resolved in included or resolved not in excluded:
                selected.append(file_cfg_list)
        return list(chain.from_iterable(selected))

    @property
    def version_config(self) -> VersionConfig:
        """The version configuration."""
        from bumpversion.versioning.version_config import VersionConfig

        return VersionConfig(self.parse, self.serialize, self.search, self.replace, self.parts)

    def version_spec(self, version: Optional[str] = None) -> VersionSpec:
        """The version specification."""
        from bumpversion.versioning.models import VersionSpec

        return VersionSpec(self.parts)


@dataclass
class PEP621Info:
    """PEP 621 info, in particular, the static version number."""

    version: Optional[str]
