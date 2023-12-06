"""Contains methods for finding and reading configuration files."""

from __future__ import annotations

import logging
import re
from difflib import context_diff
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, MutableMapping, Union

from bumpversion.ui import print_warning

if TYPE_CHECKING:  # pragma: no-coverage
    from bumpversion.config.models import Config
    from bumpversion.version_part import Version

logger = logging.getLogger(__name__)

CONFIG_FILE_SEARCH_ORDER = (
    Path(".bumpversion.cfg"),
    Path(".bumpversion.toml"),
    Path("setup.cfg"),
    Path("pyproject.toml"),
)


def find_config_file(explicit_file: Union[str, Path, None] = None) -> Union[Path, None]:
    """
    Find the configuration file, if it exists.

    If no explicit configuration file is passed, it will search in several files to
    find its configuration.

    Args:
        explicit_file: The configuration file to explicitly use.

    Returns:
        The configuration file path
    """
    search_paths = [Path(explicit_file)] if explicit_file else CONFIG_FILE_SEARCH_ORDER
    return next(
        (cfg_file for cfg_file in search_paths if cfg_file.exists() and "bumpversion]" in cfg_file.read_text()),
        None,
    )


def read_config_file(config_file: Union[str, Path, None] = None) -> Dict[str, Any]:
    """
    Read the configuration file, if it exists.

    If no explicit configuration file is passed, it will search in several files to
    find its configuration.

    Args:
        config_file: The configuration file to explicitly use.

    Returns:
        A dictionary of read key-values
    """
    if not config_file:
        logger.info("No configuration file found.")
        return {}

    logger.info("Reading config file %s:", config_file)
    config_path = Path(config_file)
    if config_path.suffix == ".cfg":
        print_warning("The .cfg file format is deprecated. Please use .toml instead.")
        return read_ini_file(config_path)
    elif config_path.suffix == ".toml":
        return read_toml_file(config_path)
    return {}


def read_ini_file(file_path: Path) -> Dict[str, Any]:  # noqa: C901
    """
    Parse an INI file and return a dictionary of sections and their options.

    Args:
        file_path: The path to the INI file.

    Returns:
        dict: A dictionary of sections and their options.
    """
    import configparser

    from bumpversion import autocast

    # Create a ConfigParser object and read the INI file
    config_parser = configparser.RawConfigParser()
    if file_path.name == "setup.cfg":
        config_parser = configparser.ConfigParser()

    config_parser.read(file_path)

    # Create an empty dictionary to hold the parsed sections and options
    bumpversion_options: Dict[str, Any] = {"files": [], "parts": {}}

    # Loop through each section in the INI file
    for section_name in config_parser.sections():
        if not section_name.startswith("bumpversion"):
            continue

        section_parts = section_name.split(":")
        num_parts = len(section_parts)
        options = {key: autocast.autocast_value(val) for key, val in config_parser.items(section_name)}

        if num_parts == 1:  # bumpversion section
            bumpversion_options.update(options)
            serialize = bumpversion_options.get("serialize", [])
            if "message" in bumpversion_options and isinstance(bumpversion_options["message"], list):
                bumpversion_options["message"] = ",".join(bumpversion_options["message"])
            if not isinstance(serialize, list):
                bumpversion_options["serialize"] = [serialize]
        elif num_parts > 1 and section_parts[1].startswith("file"):
            file_options = {
                "filename": section_parts[2],
            }
            file_options.update(options)
            if "replace" in file_options and isinstance(file_options["replace"], list):
                file_options["replace"] = "\n".join(file_options["replace"])
            bumpversion_options["files"].append(file_options)
        elif num_parts > 1 and section_parts[1].startswith("glob"):
            file_options = {
                "glob": section_parts[2],
            }
            file_options.update(options)
            if "replace" in file_options and isinstance(file_options["replace"], list):
                file_options["replace"] = "\n".join(file_options["replace"])
            bumpversion_options["files"].append(file_options)
        elif num_parts > 1 and section_parts[1].startswith("part"):
            bumpversion_options["parts"][section_parts[2]] = options

    # Return the dictionary of sections and options
    return bumpversion_options


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
    toml_data = tomlkit.parse(file_path.read_text()).unwrap()

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
    from bumpversion.config.models import FileConfig
    from bumpversion.files import DataFileUpdater

    if not config_file:
        logger.info("No configuration file found to update.")
        return

    config_path = Path(config_file)
    if config_path.suffix != ".toml":
        logger.info("Could not find the current version in the config file: %s.", config_path)
        return

    # TODO: Eventually this should be transformed into another default "files_to_modify" entry
    datafile_config = FileConfig(
        filename=str(config_path),
        key_path="tool.bumpversion.current_version",
        search=config.search,
        replace=config.replace,
        regex=config.regex,
        ignore_missing_version=config.ignore_missing_version,
        serialize=config.serialize,
        parse=config.parse,
    )

    updater = DataFileUpdater(datafile_config, config.version_config.part_configs)
    updater.update_file(current_version, new_version, context, dry_run)


def update_ini_config_file(
    config_file: Union[str, Path], current_version: str, new_version: str, dry_run: bool = False
) -> None:
    """
    Update the current_version key in the configuration file.

    Instead of parsing and re-writing the config file with new information, it will use
    a regular expression to just replace the current_version value. The idea is it will
    avoid unintentional changes (like formatting) to the config file.

    Args:
        config_file: The configuration file to explicitly use.
        current_version: The serialized current version.
        new_version: The serialized new version.
        dry_run: True if the update should be a dry run.
    """
    cfg_current_version_regex = re.compile(
        f"(?P<section_prefix>\\[bumpversion]\n[^[]*current_version\\s*=\\s*)(?P<version>{current_version})",
        re.MULTILINE,
    )

    config_path = Path(config_file)
    existing_config = config_path.read_text()
    if config_path.suffix == ".cfg" and cfg_current_version_regex.search(existing_config):
        sub_str = f"\\g<section_prefix>{new_version}"
        new_config = cfg_current_version_regex.sub(sub_str, existing_config)
    else:
        logger.info("Could not find the current version in the config file: %s.", config_path)
        return

    logger.info(
        "%s to config file %s:",
        "Would write" if dry_run else "Writing",
        config_path,
    )

    logger.info(
        "\n".join(
            list(
                context_diff(
                    existing_config.splitlines(),
                    new_config.splitlines(),
                    fromfile=f"before {config_path}",
                    tofile=f"after {config_path}",
                    lineterm="",
                )
            )
        )
    )

    if not dry_run:
        config_path.write_text(new_config)
