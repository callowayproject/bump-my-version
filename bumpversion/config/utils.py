"""Helper functions for the config module."""
from __future__ import annotations

import glob
import itertools
from typing import Dict, List

from bumpversion.config.models import FileChange, VersionPartConfig
from bumpversion.utils import labels_for_format


def get_all_file_configs(config_dict: dict) -> List[FileChange]:
    """Make sure all version parts are included."""
    defaults = {
        "parse": config_dict["parse"],
        "serialize": config_dict["serialize"],
        "search": config_dict["search"],
        "replace": config_dict["replace"],
        "ignore_missing_version": config_dict["ignore_missing_version"],
        "regex": config_dict["regex"],
    }
    files = [{k: v for k, v in filecfg.items() if v is not None} for filecfg in config_dict["files"]]
    for f in files:
        f.update({k: v for k, v in defaults.items() if k not in f})
    return [FileChange(**f) for f in files]


def get_all_part_configs(config_dict: dict) -> Dict[str, VersionPartConfig]:
    """Make sure all version parts are included."""
    serialize = config_dict["serialize"]
    parts = config_dict["parts"]
    all_labels = set(itertools.chain.from_iterable([labels_for_format(fmt) for fmt in serialize]))
    return {
        label: VersionPartConfig(**parts[label]) if label in parts else VersionPartConfig()  # type: ignore[call-arg]
        for label in all_labels
    }


def resolve_glob_files(file_cfg: FileChange) -> List[FileChange]:
    """
    Return a list of file configurations that match the glob pattern.

    Args:
        file_cfg: The file configuration containing the glob pattern

    Returns:
        A list of resolved file configurations according to the pattern.
    """
    files = []
    for filename_glob in glob.glob(file_cfg.glob, recursive=True):
        new_file_cfg = file_cfg.model_copy()
        new_file_cfg.filename = filename_glob
        new_file_cfg.glob = None
        files.append(new_file_cfg)
    return files
