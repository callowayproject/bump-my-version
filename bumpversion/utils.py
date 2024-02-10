"""General utilities."""

import datetime
import string
from collections import ChainMap
from dataclasses import asdict
from typing import TYPE_CHECKING, Any, List, Optional, Tuple

if TYPE_CHECKING:  # pragma: no-coverage
    from bumpversion.config import Config
    from bumpversion.scm import SCMInfo
    from bumpversion.versioning.models import Version


def extract_regex_flags(regex_pattern: str) -> Tuple[str, str]:
    """
    Extract the regex flags from the regex pattern.

    Args:
        regex_pattern: The pattern that might start with regex flags

    Returns:
        A tuple of the regex pattern without the flag string and regex flag string
    """
    import re

    flag_pattern = r"^(\(\?[aiLmsux]+\))"
    bits = re.split(flag_pattern, regex_pattern)
    return (regex_pattern, "") if len(bits) == 1 else (bits[2], bits[1])


def recursive_sort_dict(input_value: Any) -> Any:
    """Sort a dictionary recursively."""
    if not isinstance(input_value, dict):
        return input_value

    return {key: recursive_sort_dict(input_value[key]) for key in sorted(input_value.keys())}


def key_val_string(d: dict) -> str:
    """Render the dictionary as a comma-delimited key=value string."""
    return ", ".join(f"{k}={v}" for k, v in sorted(d.items()))


def prefixed_environ() -> dict:
    """Return a dict of the environment with keys wrapped in `${}`."""
    import os

    return {f"${key}": value for key, value in os.environ.items()}


def labels_for_format(serialize_format: str) -> List[str]:
    """Return a list of labels for the given serialize_format."""
    return [item[1] for item in string.Formatter().parse(serialize_format) if item[1]]


def base_context(scm_info: Optional["SCMInfo"] = None) -> ChainMap:
    """The default context for rendering messages and tags."""
    from bumpversion.scm import SCMInfo  # Including this here to avoid circular imports

    scm = asdict(scm_info) if scm_info else asdict(SCMInfo())

    return ChainMap(
        {
            "now": datetime.datetime.now(),
            "utcnow": datetime.datetime.now(datetime.timezone.utc),
        },
        prefixed_environ(),
        scm,
        {c: c for c in ("#", ";")},
    )


def get_context(
    config: "Config", current_version: Optional["Version"] = None, new_version: Optional["Version"] = None
) -> ChainMap:
    """Return the context for rendering messages and tags."""
    ctx = base_context(config.scm_info)
    ctx = ctx.new_child({"current_version": config.current_version})
    if current_version:
        ctx = ctx.new_child({f"current_{part}": current_version[part].value for part in current_version})
    if new_version:
        ctx = ctx.new_child({f"new_{part}": new_version[part].value for part in new_version})
    return ctx


def get_overrides(**kwargs) -> dict:
    """Return a dictionary containing only the overridden key-values."""
    return {key: val for key, val in kwargs.items() if val is not None}


def get_nested_value(d: dict, path: str) -> Any:
    """
    Retrieves the value of a nested key in a dictionary based on the given path.

    Args:
        d: The dictionary to search.
        path: A string representing the path to the nested key, separated by periods.

    Returns:
        The value of the nested key.

    Raises:
        KeyError: If a key in the path does not exist.
        ValueError: If an element in the path is not a dictionary.
    """
    keys = path.split(".")
    current_element = d

    for key in keys:
        if not isinstance(current_element, dict):
            raise ValueError(f"Element at '{'.'.join(keys[:keys.index(key)])}' is not a dictionary")

        if key not in current_element:
            raise KeyError(f"Key '{key}' not found at '{'.'.join(keys[:keys.index(key)])}'")

        current_element = current_element[key]

    return current_element


def set_nested_value(d: dict, value: Any, path: str) -> None:
    """
    Sets the value of a nested key in a dictionary based on the given path.

    Args:
        d: The dictionary to search.
        value: The value to set.
        path: A string representing the path to the nested key, separated by periods.

    Raises:
        ValueError: If an element in the path is not a dictionary.
    """
    keys = path.split(".")
    last_element = keys[-1]
    current_element = d

    for i, key in enumerate(keys):
        if key == last_element:
            current_element[key] = value
        elif key not in current_element:
            raise KeyError(f"Key '{key}' not found at '{'.'.join(keys[:keys.index(key)])}'")
        elif not isinstance(current_element[key], dict):
            raise ValueError(f"Path '{'.'.join(keys[:i+1])}' does not lead to a dictionary.")
        else:
            current_element = current_element[key]
