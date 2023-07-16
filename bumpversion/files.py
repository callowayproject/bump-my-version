"""Methods for changing files."""
import glob
import logging
import re
from copy import deepcopy
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
        self.no_regex = file_cfg.no_regex or False
        self.ignore_missing_version = file_cfg.ignore_missing_version or False
        self.version_config = VersionConfig(
            self.parse, self.serialize, self.search, self.replace, version_config.part_configs
        )
        self._newlines: Optional[str] = None

    def get_file_contents(self) -> str:
        """Return the contents of the file."""
        with open(self.path, "rt", encoding="utf-8") as f:
            contents = f.read()
            self._newlines = f.newlines[0] if isinstance(f.newlines, tuple) else f.newlines
            return contents

    def write_file_contents(self, contents: str) -> None:
        """Write the contents of the file."""
        if self._newlines is None:
            _ = self.get_file_contents()

        with open(self.path, "wt", encoding="utf-8", newline=self._newlines) as f:
            f.write(contents)

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
        search_expression = self.get_search_pattern(context)

        if self.contains(search_expression):
            return True

        # the `search` pattern did not match, but the original supplied
        # version number (representing the same version part values) might
        # match instead.

        # check whether `search` isn't customized, i.e. should match only
        # very specific parts of the file
        search_pattern_is_default = self.search == self.version_config.search

        if search_pattern_is_default and self.contains(re.compile(re.escape(version.original))):
            # The original version is present, and we're not looking for something
            # more specific -> this is accepted as a match
            return True

        # version not found
        if self.ignore_missing_version:
            return False
        raise VersionNotFoundError(f"Did not find '{search_expression.pattern}' in file: '{self.path}'")

    def contains(self, search: re.Pattern) -> bool:
        """Does the work of the contains_version method."""
        if not search:
            return False

        contents = self.get_file_contents()

        for m in re.finditer(search, contents):
            line_no = contents.count("\n", 0, m.start(0)) + 1
            logger.info(
                "Found '%s' in %s at line %s: %s",
                search,
                self.path,
                line_no,
                m.string[m.start() : m.end(0)],
            )
            return True
        return False

    def replace_version(
        self, current_version: Version, new_version: Version, context: MutableMapping, dry_run: bool = False
    ) -> None:
        """Replace the current version with the new version."""
        file_content_before = self.get_file_contents()

        context["current_version"] = self.version_config.serialize(current_version, context)
        if new_version:
            context["new_version"] = self.version_config.serialize(new_version, context)

        search_for = self.get_search_pattern(context)
        replace_with = self.version_config.replace.format(**context)

        file_content_after = search_for.sub(replace_with, file_content_before)

        if file_content_before == file_content_after and current_version.original:
            og_context = deepcopy(context)
            og_context["current_version"] = current_version.original
            search_for_og = self.get_search_pattern(og_context)
            file_content_after = search_for_og.sub(replace_with, file_content_before)

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
            self.write_file_contents(file_content_after)

    def get_search_pattern(self, context: MutableMapping) -> re.Pattern:
        """Compile and return the regex if it is valid, otherwise return the string."""
        # the default search pattern is escaped, so we can still use it in a regex
        default = re.compile(re.escape(self.version_config.search.format(**context)), re.MULTILINE | re.DOTALL)
        if self.no_regex:
            logger.debug("No RegEx flag detected. Searching for the default pattern: '%s'", default.pattern)
            return default

        re_context = {key: re.escape(str(value)) for key, value in context.items()}
        regex_pattern = self.version_config.search.format(**re_context)
        try:
            search_for_re = re.compile(regex_pattern, re.MULTILINE | re.DOTALL)
            logger.debug("Searching for the regex: '%s'", search_for_re.pattern)
            return search_for_re
        except re.error as e:
            logger.error("Invalid regex '%s' for file %s: %s.", default, self.path, e)

        logger.debug("Searching for the default pattern: '%s'", default.pattern)
        return default

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
