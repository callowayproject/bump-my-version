"""Functions for serializing and deserializing version objects."""
import re
from typing import Dict

from bumpversion.exceptions import BumpVersionError
from bumpversion.ui import get_indented_logger
from bumpversion.utils import key_val_string

logger = get_indented_logger(__name__)


def parse_version(version_string: str, parse_pattern: str) -> Dict[str, str]:
    """
    Parse a version string into a dictionary of the parts and values using a regular expression.

    Args:
        version_string: Version string to parse
        parse_pattern: The regular expression pattern to use for parsing

    Returns:
        A dictionary of version part labels and their values, or an empty dictionary
        if the version string doesn't match.

    Raises:
        BumpVersionError: If the parse_pattern is not a valid regular expression
    """
    if not version_string:
        logger.debug("Version string is empty, returning empty dict")
        return {}
    elif not parse_pattern:
        logger.debug("Parse pattern is empty, returning empty dict")
        return {}

    logger.debug("Parsing version '%s' using regexp '%s'", version_string, parse_pattern)
    logger.indent()

    try:
        pattern = re.compile(parse_pattern, re.VERBOSE)
    except re.error as e:
        raise BumpVersionError(f"'{parse_pattern}' is not a valid regular expression.") from e

    match = re.search(pattern, version_string)

    if not match:
        logger.debug(
            "'%s' does not parse current version '%s'",
            parse_pattern,
            version_string,
        )
        return {}

    parsed = match.groupdict(default="")
    logger.debug("Parsed the following values: %s", key_val_string(parsed))
    logger.dedent()

    return parsed
