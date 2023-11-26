"""Contains methods for finding and reading configuration files."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, Union

from bumpversion.ui import print_warning

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
