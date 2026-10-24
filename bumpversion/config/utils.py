"""Helper functions for the config module."""

from __future__ import annotations

import re
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Dict, List, Optional

from wcmatch import glob

from bumpversion.config.models import FileChange
from bumpversion.exceptions import BumpVersionError, ConfigurationError
from bumpversion.ui import get_indented_logger
from bumpversion.utils import Pathlike, find_repo_root
from bumpversion.versioning.models import VersionComponentSpec

# Built by concatenation so ruff doesn't flag it as a missing f-string.
REPO_ROOT_TOKEN = "{" + "repo_root}"

logger = get_indented_logger(__name__)


def get_all_file_configs(config_dict: dict) -> List[FileChange]:
    """Make sure all version components are included."""
    defaults = {
        "parse": config_dict["parse"],
        "serialize": config_dict["serialize"],
        "search": config_dict["search"],
        "replace": config_dict["replace"],
        "ignore_missing_version": config_dict["ignore_missing_version"],
        "ignore_missing_file": config_dict["ignore_missing_files"],
        "regex": config_dict["regex"],
        "include_bumps": tuple(config_dict["parts"]),
    }
    for filecfg in config_dict["files"]:
        if not isinstance(filecfg, dict):
            raise ConfigurationError(f"Each 'files' entry must be a table/mapping, got {filecfg!r}.")
    files = [{k: v for k, v in filecfg.items() if v is not None} for filecfg in config_dict["files"] if filecfg]
    for f in files:
        f.update({k: v for k, v in defaults.items() if k not in f})
    return [FileChange(**f) for f in files]


def resolve_file_paths(files: List[FileChange], config_file: Optional[Pathlike]) -> None:
    """
    Resolve `filename` and `glob` of each file configuration in place.

    `{repo_root}` expands to the repository root. Other relative paths are resolved from the
    configuration file's directory; absolute paths are used as-is.

    Args:
        files: The file configurations to update in place.
        config_file: The configuration file the files were read from, if any.

    Raises:
        ConfigurationError: If `{repo_root}` is used outside a git or mercurial repository.
    """
    config_dir = Path(config_file).resolve().parent if config_file else Path.cwd()
    # Leave paths untouched when they already resolve from the cwd, to keep output stable.
    rebase = config_dir != Path.cwd().resolve()
    repo_root = find_repo_root(config_dir)
    token = REPO_ROOT_TOKEN

    def resolve(value: str, escape: bool = False, negatable: bool = False) -> str:
        negated = negatable and value.startswith("!")  # keep the `!` in front of the base dir
        if negated:
            value = value[1:]
        if token in value:
            if repo_root is None:
                raise ConfigurationError(f"'{token}' used in '{value}', but not in a git or mercurial repository.")
            root = repo_root.as_posix()
            value = value.replace(token, glob.escape(root) if escape else root)
        # Check both flavours so `/foo` and `C:\foo` are absolute on every platform.
        if rebase and not (PurePosixPath(value).is_absolute() or PureWindowsPath(value).is_absolute()):
            base = config_dir.as_posix()
            value = f"{glob.escape(base) if escape else base}/{value}"
        return f"!{value}" if negated else value

    for file_cfg in files:
        if file_cfg.filename:
            file_cfg.filename = resolve(file_cfg.filename)
        if file_cfg.glob:
            file_cfg.glob = resolve(file_cfg.glob, escape=True)
            if file_cfg.glob_exclude:
                file_cfg.glob_exclude = tuple(resolve(p, escape=True, negatable=True) for p in file_cfg.glob_exclude)


def get_all_part_configs(config_dict: dict) -> Dict[str, VersionComponentSpec]:
    """Make sure all version components are included."""
    try:
        parsing_groups = list(re.compile(config_dict["parse"]).groupindex.keys())
    except re.error as e:
        raise BumpVersionError(f"Could not parse regex '{config_dict['parse']}': {e}") from e
    parts = config_dict["parts"]

    part_configs = {}
    for label in parsing_groups:
        is_independent = label.startswith("$")
        part_configs[label] = (
            VersionComponentSpec(**parts[label])
            if label in parts
            else VersionComponentSpec(independent=is_independent)
        )
    return part_configs


def resolve_glob_files(file_cfg: FileChange, ignore_missing: bool = False) -> List[FileChange]:
    """
    Return a list of file configurations that match the glob pattern.

    Args:
        file_cfg: The file configuration containing the glob pattern
        ignore_missing: Don't raise if the pattern matches no files, regardless of `ignore_missing_file`

    Returns:
        A list of resolved file configurations according to the pattern.

    Raises:
        FileNotFoundError: If no files match the pattern and neither `ignore_missing_file` nor `ignore_missing` is set.
    """
    files: List[FileChange] = []
    exclude = file_cfg.glob_exclude or ()
    glob_flags = glob.GLOBSTAR | glob.FORCEUNIX | glob.SPLIT | glob.EXTGLOB
    for filename_glob in glob.glob(file_cfg.glob, flags=glob_flags, exclude=exclude):
        new_file_cfg = file_cfg.model_copy()
        new_file_cfg.filename = filename_glob
        new_file_cfg.glob = None
        files.append(new_file_cfg)
    if not files:
        if not (file_cfg.ignore_missing_file or ignore_missing):
            raise FileNotFoundError(f"No files found matching glob '{file_cfg.glob}'")
        logger.info("No files found matching glob '%s', but ignoring", file_cfg.glob)
    return files
