"""Bump My Version configuration models."""
from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Optional, Union

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

if TYPE_CHECKING:
    from bumpversion.scm import SCMInfo
    from bumpversion.version_part import VersionConfig


class VersionPartConfig(BaseModel):
    """Configuration of a part of the version."""

    values: Optional[list] = None  # Optional. Numeric is used if missing or no items in list
    optional_value: Optional[str] = None  # Optional.
    # Defaults to first value. 0 in the case of numeric. Empty string means nothing is optional.
    first_value: Union[str, int, None] = None  # Optional. Defaults to first value in values
    independent: bool = False


class FileConfig(BaseModel):
    """Search and replace file config."""

    parse: str
    serialize: List[str]
    search: str
    replace: str
    regex: bool
    ignore_missing_version: bool
    filename: Optional[str] = None
    glob: Optional[str] = None  # Conflicts with filename. If both are specified, glob wins
    key_path: Optional[str] = None  # If specified, and has an appropriate extension, will be treated as a data file


class Config(BaseSettings):
    """Bump Version configuration."""

    current_version: Optional[str]
    parse: str
    serialize: List[str] = Field(min_length=1)
    search: str
    replace: str
    regex: bool
    ignore_missing_version: bool
    tag: bool
    sign_tags: bool
    tag_name: str
    tag_message: Optional[str]
    allow_dirty: bool
    commit: bool
    message: str
    commit_args: Optional[str]
    scm_info: Optional["SCMInfo"]
    parts: Dict[str, VersionPartConfig]
    files: List[FileConfig]
    included_paths: List[str] = Field(default_factory=list)
    excluded_paths: List[str] = Field(default_factory=list)
    model_config = SettingsConfigDict(env_prefix="bumpversion_")

    def add_files(self, filename: Union[str, List[str]]) -> None:
        """Add a filename to the list of files."""
        filenames = [filename] if isinstance(filename, str) else filename
        for name in filenames:
            if name in self.resolved_filemap:
                continue
            self.files.append(
                FileConfig(
                    filename=name,
                    glob=None,
                    key_path=None,
                    parse=self.parse,
                    serialize=self.serialize,
                    search=self.search,
                    replace=self.replace,
                    regex=self.regex,
                    ignore_missing_version=self.ignore_missing_version,
                )
            )

    @property
    def resolved_filemap(self) -> Dict[str, FileConfig]:
        """Return a map of filenames to file configs, expanding any globs."""
        from bumpversion.config.utils import resolve_glob_files

        new_files = []
        for file_cfg in self.files:
            if file_cfg.glob:
                new_files.extend(resolve_glob_files(file_cfg))
            else:
                new_files.append(file_cfg)

        return {file_cfg.filename: file_cfg for file_cfg in new_files}

    @property
    def files_to_modify(self) -> List[FileConfig]:
        """Return a list of files to modify."""
        files_not_excluded = [
            file_cfg.filename
            for file_cfg in self.resolved_filemap.values()
            if file_cfg.filename not in self.excluded_paths
        ]
        inclusion_set = set(self.included_paths) | set(files_not_excluded)
        return [file_cfg for file_cfg in self.resolved_filemap.values() if file_cfg.filename in inclusion_set]

    @property
    def version_config(self) -> "VersionConfig":
        """Return the version configuration."""
        from bumpversion.version_part import VersionConfig

        return VersionConfig(self.parse, self.serialize, self.search, self.replace, self.parts)
