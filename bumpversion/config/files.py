"""Contains methods for finding and reading configuration files."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, MutableMapping, Optional, Union

from bumpversion.config.files_legacy import read_ini_file
from bumpversion.config.models import PEP621Info
from bumpversion.ui import get_indented_logger, print_warning
from bumpversion.utils import find_repo_root

if TYPE_CHECKING:  # pragma: no-coverage
    from bumpversion.config.models import Config
    from bumpversion.utils import Pathlike
    from bumpversion.versioning.models import Version

logger = get_indented_logger(__name__)

CONFIG_FILE_SEARCH_ORDER = (
    ".bumpversion.cfg",
    ".bumpversion.toml",
    "setup.cfg",
    "pyproject.toml",
)


def get_pep621_info(config_file: Optional[Pathlike] = None) -> Optional[PEP621Info]:
    """Retrieve the PEP 621 `project` table.

    At the moment, only the `project.version` key is handled. Additionally, if the
    version is marked as dynamic, then it is explicitly returned as `None`.

    Args:
        config_file:
            The configuration file to explicitly use. Per PEP 621, this file must be
            named `pyproject.toml`.

    Returns:
        A `PEP621Info` structure, if given a `pyproject.toml` file to parse, else `None`.

    """
    # We repeat the steps of read_config_file here, except hardcoded to TOML files, and
    # without additional error reporting.  Then we reimplement read_toml_file, but
    # without limiting ourselves to the tool.bumpversion subtable.
    if not config_file:
        return None

    config_path = Path(config_file)
    if not config_path.exists():
        return None

    # PEP 621 explicitly requires pyproject.toml
    if config_path.name != "pyproject.toml":
        return None

    project = _load_toml_mapping(config_path).get("project")
    if not isinstance(project, dict):
        return PEP621Info(version=None)
    dynamic = project.get("dynamic")
    if isinstance(dynamic, list) and "version" in dynamic:
        return PEP621Info(version=None)
    version = project.get("version")
    return PEP621Info(version=version if isinstance(version, str) else None)


def find_config_file(explicit_file: Optional[Pathlike] = None) -> Union[Path, None]:
    """
    Find the configuration file if it exists.

    If no explicit configuration file is passed, it will search in several files to
    find its configuration.

    Args:
        explicit_file: The configuration file to explicitly use.

    Returns:
        The configuration file path
    """
    if explicit_file:
        search_paths = [Path(explicit_file)]
    else:
        cwd = Path.cwd()
        repo_root = find_repo_root(cwd)
        # Inside a repo, walk up to the repo root; otherwise only look in the cwd.
        dirs = [cwd]
        if repo_root:
            resolved = cwd.resolve()
            dirs = [resolved, *resolved.parents][: len(resolved.parts) - len(repo_root.parts) + 1]
        search_paths = [d / name for d in dirs for name in CONFIG_FILE_SEARCH_ORDER]
    existing = [f for f in search_paths if f.exists()]
    match = next((f for f in existing if _has_bumpversion_config(f)), None)
    # A bare pyproject.toml with a static PEP 621 version is the last resort
    return match or next((f for f in existing if _has_static_pep621_version(f)), None)


def _load_toml_mapping(path: Path) -> Dict[str, Any]:
    """Parse a TOML file, returning `{}` if it is invalid or not a mapping."""
    import tomlkit
    from tomlkit.exceptions import TOMLKitError

    try:
        data = tomlkit.parse(path.read_text(encoding="utf-8")).unwrap()
    except TOMLKitError:
        return {}
    return data if isinstance(data, dict) else {}


def _has_bumpversion_config(path: Path) -> bool:
    """Does the file contain bump-my-version configuration?"""
    if path.suffix != ".toml":
        return "bumpversion]" in path.read_text(encoding="utf-8")
    tool = _load_toml_mapping(path).get("tool")
    return isinstance(tool, dict) and isinstance(tool.get("bumpversion"), dict)


def _has_static_pep621_version(path: Path) -> bool:
    """Is the file a `pyproject.toml` with a static `project.version`?"""
    info = get_pep621_info(path)
    return info is not None and bool(info.version)


def read_config_file(config_file: Optional[Pathlike] = None) -> Dict[str, Any]:
    """
    Read the configuration file if it exists.

    If no explicit configuration file is passed, it will search in several files to
    find its configuration.

    Args:
        config_file: The configuration file to explicitly use.

    Returns:
        A dictionary of read key-values
    """
    if not config_file:
        logger.warning("No configuration file found.")
        return {}

    config_path = Path(config_file)
    if not config_path.exists():
        logger.warning("Configuration file not found: %s.", config_path)
        return {}

    logger.info("Reading config file: %s", config_file)

    if config_path.suffix == ".cfg":
        print_warning("The .cfg file format is deprecated. Please use .toml instead.")
        return read_ini_file(config_path)
    elif config_path.suffix == ".toml":
        return read_toml_file(config_path)
    else:
        logger.warning("Unknown config file suffix: %s. Using defaults.", config_path.suffix)
        return {}


def read_toml_file(file_path: Path) -> Dict[str, Any]:
    """
    Parse a TOML file and return the `bumpversion` section.

    Args:
        file_path: The path to the TOML file.

    Returns:
        dict: A dictionary of the `bumpversion` section.
    """
    import tomlkit

    # Load the TOML file
    toml_data = tomlkit.parse(file_path.read_text(encoding="utf-8")).unwrap()

    return toml_data.get("tool", {}).get("bumpversion", {})


def update_config_file(
    config_file: Union[str, Path],
    config: Config,
    current_version: Version,
    new_version: Version,
    context: MutableMapping,
    dry_run: bool = False,
) -> None:
    """
    Update the current_version key in the configuration file.

    Args:
        config_file: The configuration file to explicitly use.
        config: The configuration to use.
        current_version: The current version.
        new_version: The new version.
        context: The context to use for serialization.
        dry_run: True if the update should be a dry run.
    """
    from bumpversion.config.models import FileChange
    from bumpversion.files import DataFileUpdater

    if not config_file:
        logger.info("\n%sNo configuration file found to update.", logger.indent_str)
        return
    else:
        logger.info("\n%sProcessing config file: %s", logger.indent_str, config_file)
    logger.indent()
    config_path = Path(config_file).resolve()

    if config.scm_info.tool and not config.scm_info.path_in_repo(config_path):
        logger.info("\n%sConfiguration file is outside of the repo. Not going to change.", logger.indent_str)
        return

    if config_path.suffix != ".toml":
        logger.info("You must have a `.toml` suffix to update the config file: %s.", config_path)
        return

    # TODO: Eventually this config (and datafile_config_pyprojecttoml below) should be
    # transformed into another default "files_to_modify" entry
    datafile_config = FileChange(
        filename=str(config_path),
        key_path="tool.bumpversion.current_version",
        search=config.search,
        replace=config.replace,
        regex=config.regex,
        ignore_missing_version=True,
        ignore_missing_file=True,
        serialize=config.serialize,
        parse=config.parse,
    )

    updater = DataFileUpdater(datafile_config, config.version_config.part_configs)
    updater.update_file(current_version, new_version, context, dry_run)

    # Keep PEP 621 `project.version` consistent with `tool.bumpversion.current_version`.
    # (At least, if PEP 621 static `project.version` is in use at all.)
    if (
        config_path.name == "pyproject.toml"
        and config.pep621_info is not None
        and config.pep621_info.version is not None
    ):
        datafile_config_pyprojecttoml = FileChange(
            filename=str(config_path),
            key_path="project.version",
            search=config.search,
            replace=config.replace,
            regex=config.regex,
            ignore_missing_version=True,
            ignore_missing_file=True,
            serialize=config.serialize,
            parse=config.parse,
        )
        updater2 = DataFileUpdater(datafile_config_pyprojecttoml, config.version_config.part_configs)
        updater2.update_file(current_version, new_version, context, dry_run)

    logger.dedent()
