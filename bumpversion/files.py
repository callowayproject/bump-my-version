"""Methods for changing files."""
import logging
import re
from copy import deepcopy
from difflib import context_diff
from typing import List, MutableMapping, Optional, Tuple

from bumpversion.config import FileConfig
from bumpversion.exceptions import VersionNotFoundError
from bumpversion.version_part import Version, VersionConfig

logger = logging.getLogger(__name__)


def get_search_pattern(search_str: str, context: MutableMapping, use_regex: bool = False) -> Tuple[re.Pattern, str]:
    """
    Render the search pattern and return the compiled regex pattern and the raw pattern.

    Args:
        search_str: A string containing the search pattern as a format string
        context: The context to use for rendering the search pattern
        use_regex: If True, the search pattern is treated as a regex pattern

    Returns:
        A tuple of the compiled regex pattern and the raw pattern as a string.
    """
    # the default search pattern is escaped, so we can still use it in a regex
    raw_pattern = search_str.format(**context)
    default = re.compile(re.escape(raw_pattern), re.MULTILINE | re.DOTALL)
    if not use_regex:
        logger.debug("No RegEx flag detected. Searching for the default pattern: '%s'", default.pattern)
        return default, raw_pattern

    re_context = {key: re.escape(str(value)) for key, value in context.items()}
    regex_pattern = search_str.format(**re_context)
    try:
        search_for_re = re.compile(regex_pattern, re.MULTILINE | re.DOTALL)
        logger.debug("Searching for the regex: '%s'", search_for_re.pattern)
        return search_for_re, raw_pattern
    except re.error as e:
        logger.error("Invalid regex '%s': %s.", default, e)

    logger.debug("Invalid regex. Searching for the default pattern: '%s'", raw_pattern)
    return default, raw_pattern


def contains_pattern(search: re.Pattern, contents: str) -> bool:
    """Does the search pattern match any part of the contents?"""
    if not search or not contents:
        return False

    for m in re.finditer(search, contents):
        line_no = contents.count("\n", 0, m.start(0)) + 1
        logger.info(
            "Found '%s' at line %s: %s",
            search,
            line_no,
            m.string[m.start() : m.end(0)],
        )
        return True
    return False


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
        self.regex = file_cfg.regex or False
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
        search_expression, raw_search_expression = get_search_pattern(self.search, context, self.regex)
        file_contents = self.get_file_contents()
        if contains_pattern(search_expression, file_contents):
            return True

        # the `search` pattern did not match, but the original supplied
        # version number (representing the same version part values) might
        # match instead.

        # check whether `search` isn't customized, i.e. should match only
        # very specific parts of the file
        search_pattern_is_default = self.search == self.version_config.search

        if search_pattern_is_default and contains_pattern(re.compile(re.escape(version.original)), file_contents):
            # The original version is present, and we're not looking for something
            # more specific -> this is accepted as a match
            return True

        # version not found
        if self.ignore_missing_version:
            return False
        raise VersionNotFoundError(f"Did not find '{raw_search_expression}' in file: '{self.path}'")

    def replace_version(
        self, current_version: Version, new_version: Version, context: MutableMapping, dry_run: bool = False
    ) -> None:
        """Replace the current version with the new version."""
        file_content_before = self.get_file_contents()

        context["current_version"] = self.version_config.serialize(current_version, context)
        if new_version:
            context["new_version"] = self.version_config.serialize(new_version, context)

        search_for, raw_search_pattern = get_search_pattern(self.search, context, self.regex)
        replace_with = self.version_config.replace.format(**context)

        file_content_after = search_for.sub(replace_with, file_content_before)

        if file_content_before == file_content_after and current_version.original:
            og_context = deepcopy(context)
            og_context["current_version"] = current_version.original
            search_for_og, og_raw_search_pattern = get_search_pattern(self.search, og_context, self.regex)
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
    return [ConfiguredFile(file_cfg, version_config, search, replace) for file_cfg in files]


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
