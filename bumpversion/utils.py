"""General utilities."""
import string
from collections import ChainMap
from dataclasses import asdict
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:  # pragma: no-coverage
    from bumpversion.config import Config
    from bumpversion.version_part import Version


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


def get_context(
    config: "Config", current_version: Optional["Version"] = None, new_version: Optional["Version"] = None
) -> ChainMap:
    """Return the context for rendering messages and tags."""
    import datetime

    ctx = ChainMap(
        {"current_version": config.current_version},
        {"now": datetime.datetime.now(), "utcnow": datetime.datetime.utcnow()},
        prefixed_environ(),
        asdict(config.scm_info),
        {c: c for c in ("#", ";")},
    )
    if current_version:
        ctx.new_child({f"current_{part}": current_version[part].value for part in current_version})
    if new_version:
        ctx.new_child({f"new_{part}": new_version[part].value for part in new_version})
    return ctx


def get_overrides(**kwargs) -> dict:
    """Return a dictionary containing only the overridden key-values."""
    return {key: val for key, val in kwargs.items() if val is not None}
