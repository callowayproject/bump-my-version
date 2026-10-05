"""Verify that the project is consistent with its current version, without changing anything."""

from string import Formatter
from typing import List, Optional

from bumpversion.config import Config
from bumpversion.context import get_context
from bumpversion.exceptions import VersionNotFoundError
from bumpversion.files import resolve_file_config
from bumpversion.ui import get_indented_logger

logger = get_indented_logger(__name__)


def references_current_version(search: str) -> bool:
    """Does the search pattern contain the current version, or one of its components?"""
    return any(field and field.startswith("current_") for _, field, _, _ in Formatter().parse(search))


def do_check(config: Config, release_tag: Optional[str] = None) -> List[str]:
    """
    Check that every configured file contains the current version.

    Each file is searched exactly as the next `bump` would search it before replacing anything,
    so a file somebody forgot to bump (or bumped by hand to a different version) is reported.
    A search pattern without the current version (ex. an "Unreleased" changelog heading) says nothing
    about the version and is skipped; a bump may well have replaced it.

    Args:
        config: The configuration to use
        release_tag: If given, the tag being released, which must match `tag_name` rendered with the current version

    Returns:
        The problems found. Empty if the project is consistent.
    """
    logger.indent()
    problems = []
    version = config.version_config.parse(config.current_version, raise_error=True)
    assert version is not None  # parse raises instead of returning None
    ctx = get_context(config, version, version)

    for configured_file in resolve_file_config(config.files_to_modify, config.version_config):
        if not references_current_version(configured_file.file_change.search):
            logger.info(
                "Skipping %s: the search pattern '%s' does not contain the current version",
                configured_file.file_change.filename,
                configured_file.file_change.search,
            )
            continue
        try:
            configured_file.contains_version(version, ctx)
        except (FileNotFoundError, VersionNotFoundError) as e:
            problems.append(str(e))

    if config.pep621_info is not None and config.pep621_info.version not in (None, config.current_version):
        problems.append(
            f"PEP 621 `project.version` is '{config.pep621_info.version}', "
            f"but `current_version` is '{config.current_version}'"
        )

    if release_tag is not None:
        expected_tag = config.tag_name.format(**{**ctx, "new_version": config.current_version})
        if release_tag != expected_tag:
            problems.append(
                f"The release tag '{release_tag}' does not match the current version '{config.current_version}': "
                f"expected '{expected_tag}'"
            )

    logger.dedent()
    return problems
