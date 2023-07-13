"""Methods for changing files."""
import glob
import logging
from difflib import context_diff
from typing import List, MutableMapping, Optional

from bumpversion.config import FileConfig
from bumpversion.exceptions import VersionNotFoundError
from bumpversion.version_part import Version, VersionConfig

logger = logging.getLogger(__name__)


class ConfiguredFile:
    """A file to modify in a configured way."""

    def __init__(
        self,
        file_cfg: FileConfig,
        version_config: VersionConfig,
        search: Optional[str] = None,
        replace: Optional[str] = None,
    ) -> None:
        self.path = file_cfg.filename
        self.parse = file_cfg.parse or version_config.parse_regex.pattern
        self.serialize = file_cfg.serialize or version_config.serialize_formats
        self.search = search or file_cfg.search or version_config.search
        self.replace = replace or file_cfg.replace or version_config.replace
        self.ignore_missing_version = file_cfg.ignore_missing_version or False
        self.version_config = VersionConfig(
            self.parse, self.serialize, self.search, self.replace, version_config.part_configs
        )

    def contains_version(self, version: Version, context: MutableMapping) -> bool:
        """
        Check whether the version is present in the file.

        Args:
            version: The version to check
            context: The context to use

        Raises:
            VersionNotFoundError: if the version number isn't present in this file.

        Returns:
            True if the version number is in fact present.
        """
        search_expression = self.search.format(**context)

        if self.contains(search_expression):
            return True

        # the `search` pattern did not match, but the original supplied
        # version number (representing the same version part values) might
        # match instead.

        # check whether `search` isn't customized, i.e. should match only
        # very specific parts of the file
        search_pattern_is_default = self.search == self.version_config.search

        if search_pattern_is_default and self.contains(version.original):
            # original version is present, and we're not looking for something
            # more specific -> this is accepted as a match
            return True

        # version not found
        if self.ignore_missing_version:
            return False
        raise VersionNotFoundError(f"Did not find '{search_expression}' in file: '{self.path}'")

    def contains(self, search: str) -> bool:
        """Does the work of the contains_version method."""
        if not search:
            return False

        with open(self.path, "rt", encoding="utf-8") as f:
            search_lines = search.splitlines()
            lookbehind = []

            for lineno, line in enumerate(f.readlines()):
                lookbehind.append(line.rstrip("\n"))

                if len(lookbehind) > len(search_lines):
                    lookbehind = lookbehind[1:]

                if (
                    search_lines[0] in lookbehind[0]
                    and search_lines[-1] in lookbehind[-1]
                    and search_lines[1:-1] == lookbehind[1:-1]
                ):
                    logger.info(
                        "Found '%s' in %s at line %s: %s",
                        search,
                        self.path,
                        lineno - (len(lookbehind) - 1),
                        line.rstrip(),
                    )
                    return True
        return False

    def replace_version(
        self, current_version: Version, new_version: Version, context: MutableMapping, dry_run: bool = False
    ) -> None:
        """Replace the current version with the new version."""
        with open(self.path, "rt", encoding="utf-8") as f:
            file_content_before = f.read()
            file_new_lines = f.newlines[0] if isinstance(f.newlines, tuple) else f.newlines

        context["current_version"] = self.version_config.serialize(current_version, context)
        if new_version:
            context["new_version"] = self.version_config.serialize(new_version, context)

        search_for = self.version_config.search.format(**context)
        replace_with = self.version_config.replace.format(**context)

        file_content_after = file_content_before.replace(search_for, replace_with)

        if file_content_before == file_content_after and current_version.original:
            search_for_original_formatted = self.version_config.search.format(current_version=current_version.original)
            file_content_after = file_content_before.replace(search_for_original_formatted, replace_with)

        if file_content_before != file_content_after:
            logger.info("%s file %s:", "Would change" if dry_run else "Changing", self.path)
            logger.info(
                "\n".join(
                    list(
                        context_diff(
                            file_content_before.splitlines(),
                            file_content_after.splitlines(),
                            fromfile=f"before {self.path}",
                            tofile=f"after {self.path}",
                            lineterm="",
                        )
                    )
                )
            )
        else:
            logger.info("%s file %s", "Would not change" if dry_run else "Not changing", self.path)

        if not dry_run:  # pragma: no-coverage
            with open(self.path, "wt", encoding="utf-8", newline=file_new_lines) as f:
                f.write(file_content_after)

    def __str__(self) -> str:  # pragma: no-coverage
        return self.path

    def __repr__(self) -> str:  # pragma: no-coverage
        return f"<bumpversion.ConfiguredFile:{self.path}>"


def resolve_file_config(
    files: List[FileConfig], version_config: VersionConfig, search: Optional[str] = None, replace: Optional[str] = None
) -> List[ConfiguredFile]:
    """
    Resolve the files, searching and replacing values according to the FileConfig.

    Args:
        files: A list of file configurations
        version_config: How the version should be changed
        search: The search pattern to use instead of any configured search pattern
        replace: The replace pattern to use instead of any configured replace pattern

    Returns:
        A list of ConfiguredFiles
    """
    configured_files = []
    for file_cfg in files:
        if file_cfg.glob:
            configured_files.extend(get_glob_files(file_cfg, version_config))
        else:
            configured_files.append(ConfiguredFile(file_cfg, version_config, search, replace))

    return configured_files


def modify_files(
    files: List[ConfiguredFile],
    current_version: Version,
    new_version: Version,
    context: MutableMapping,
    dry_run: bool = False,
) -> None:
    """
    Modify the files, searching and replacing values according to the FileConfig.

    Args:
        files: The list of configured files
        current_version: The current version
        new_version: The next version
        context: The context used for rendering the version
        dry_run: True if this should be a report-only job
    """
    _check_files_contain_version(files, current_version, context)
    for f in files:
        f.replace_version(current_version, new_version, context, dry_run)


def get_glob_files(
    file_cfg: FileConfig, version_config: VersionConfig, search: Optional[str] = None, replace: Optional[str] = None
) -> List[ConfiguredFile]:
    """
    Return a list of files that match the glob pattern.

    Args:
        file_cfg: The file configuration containing the glob pattern
        version_config: The version configuration
        search: The search pattern to use instead of any configured search pattern
        replace: The replace pattern to use instead of any configured replace pattern

    Returns:
        A list of resolved files according to the pattern.
    """
    files = []
    for filename_glob in glob.glob(file_cfg.glob, recursive=True):
        new_file_cfg = file_cfg.copy()
        new_file_cfg.filename = filename_glob
        files.append(ConfiguredFile(new_file_cfg, version_config, search, replace))
    return files


def _check_files_contain_version(
    files: List[ConfiguredFile], current_version: Version, context: MutableMapping
) -> None:
    """Make sure files exist and contain version string."""
    logger.info(
        "Asserting files %s contain the version string...",
        ", ".join({str(f.path) for f in files}),
    )
    for f in files:
        context["current_version"] = f.version_config.serialize(current_version, context)
        f.contains_version(current_version, context)
