"""Configuration management."""
from __future__ import annotations

import itertools
import logging
import re
from difflib import context_diff
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from bumpversion.utils import labels_for_format

if TYPE_CHECKING:  # pragma: no-coverage
    from bumpversion.scm import SCMInfo
    from bumpversion.version_part import VersionConfig

from pydantic import BaseModel, BaseSettings, Field

from bumpversion.exceptions import ConfigurationError

logger = logging.getLogger(__name__)


class VersionPartConfig(BaseModel):
    """Configuration of a part of the version."""

    values: Optional[list]  # Optional. Numeric is used if missing or no items in list
    optional_value: Optional[str]  # Optional.
    # Defaults to first value. 0 in the case of numeric. Empty string means nothing is optional.
    first_value: Optional[str]  # Optional. Defaults to first value in values
    independent: bool = False


class FileConfig(BaseModel):
    """Search and replace file config."""

    filename: Optional[str]
    glob: Optional[str]  # Conflicts with filename. If both are specified, glob wins
    parse: Optional[str]  # If different from outer scope
    serialize: Optional[List[str]]  # If different from outer scope
    search: Optional[str]  # If different from outer scope
    replace: Optional[str]  # If different from outer scope
    ignore_missing_version: Optional[bool]


class Config(BaseSettings):
    """Bump Version configuration."""

    current_version: Optional[str]
    parse: str
    serialize: List[str] = Field(min_items=1)
    search: str
    replace: str
    ignore_missing_version: bool
    tag: bool
    sign_tags: bool
    tag_name: str
    tag_message: Optional[str]
    allow_dirty: bool
    commit: bool
    message: str
    commit_args: Optional[str]
    scm_info: Optional["SCMInfo"]
    parts: Dict[str, VersionPartConfig]
    files: List[FileConfig]

    class Config:
        env_prefix = "bumpversion_"

    def add_files(self, filename: Union[str, List[str]]) -> None:
        """Add a filename to the list of files."""
        filenames = [filename] if isinstance(filename, str) else filename
        self.files.extend([FileConfig(filename=name) for name in filenames])  # type: ignore[call-arg]

    @property
    def version_config(self) -> "VersionConfig":
        """Return the version configuration."""
        from bumpversion.version_part import VersionConfig

        return VersionConfig(self.parse, self.serialize, self.search, self.replace, self.parts)


DEFAULTS = {
    "current_version": None,
    "parse": r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)",
    "serialize": ["{major}.{minor}.{patch}"],
    "search": "{current_version}",
    "replace": "{new_version}",
    "ignore_missing_version": False,
    "tag": False,
    "sign_tags": False,
    "tag_name": "v{new_version}",
    "tag_message": "Bump version: {current_version} → {new_version}",
    "allow_dirty": False,
    "commit": False,
    "message": "Bump version: {current_version} → {new_version}",
    "commit_args": None,
    "scm_info": None,
    "parts": {},
    "files": [],
}

CONFIG_FILE_SEARCH_ORDER = (
    Path(".bumpversion.cfg"),
    Path(".bumpversion.toml"),
    Path("setup.cfg"),
    Path("pyproject.toml"),
)


def get_all_file_configs(config_dict: dict) -> List[FileConfig]:
    """Make sure all version parts are included."""
    defaults = {
        "parse": config_dict["parse"],
        "serialize": config_dict["serialize"],
        "search": config_dict["search"],
        "replace": config_dict["replace"],
        "ignore_missing_version": config_dict["ignore_missing_version"],
    }
    files = [{k: v for k, v in filecfg.items() if v} for filecfg in config_dict["files"]]
    for f in files:
        f.update({k: v for k, v in defaults.items() if k not in f})
    return [FileConfig(**f) for f in files]


def get_configuration(config_file: Union[str, Path, None] = None, **overrides) -> Config:
    """
    Return the configuration based on any configuration files and overrides.

    Args:
        config_file: An explicit configuration file to use, otherwise search for one
        **overrides: Specific configuration key-values to override in the configuration

    Returns:
        The configuration
    """
    from bumpversion.scm import SCMInfo, get_scm_info

    config_dict = DEFAULTS.copy()
    parsed_config = read_config_file(config_file) if config_file else {}

    # We want to strip out unrecognized key-values to avoid inadvertent issues
    config_dict.update({key: val for key, val in parsed_config.items() if key in DEFAULTS.keys()})

    allowed_overrides = set(DEFAULTS.keys())
    config_dict.update({key: val for key, val in overrides.items() if key in allowed_overrides})

    # Set any missing version parts
    config_dict["parts"] = get_all_part_configs(config_dict)

    # Set any missing file configuration
    config_dict["files"] = get_all_file_configs(config_dict)

    # Resolve the SCMInfo class for Pydantic's BaseSettings
    Config.update_forward_refs(SCMInfo=SCMInfo)
    config = Config(**config_dict)  # type: ignore[arg-type]

    # Get the information about the SCM
    tag_pattern = config.tag_name.replace("{new_version}", "*")
    scm_info = get_scm_info(tag_pattern)
    config.scm_info = scm_info

    # Update and verify the current_version
    config.current_version = check_current_version(config)

    return config


def get_all_part_configs(config_dict: dict) -> Dict[str, VersionPartConfig]:
    """Make sure all version parts are included."""
    serialize = config_dict["serialize"]
    parts = config_dict["parts"]
    all_labels = set(itertools.chain.from_iterable([labels_for_format(fmt) for fmt in serialize]))
    return {
        label: VersionPartConfig(**parts[label]) if label in parts else VersionPartConfig()  # type: ignore[call-arg]
        for label in all_labels
    }


def check_current_version(config: Config) -> str:
    """
    Returns the current version.

    If the current version is not specified in the config file, command line or env variable,
    it attempts to retrieve it via a tag.

    Args:
        config: The current configuration dictionary.

    Returns:
        The version number

    Raises:
        ConfigurationError: If it can't find the current version
    """
    current_version = config.current_version
    scm_info = config.scm_info

    if current_version is None and scm_info.current_version:
        return scm_info.current_version
    elif current_version and scm_info.current_version and current_version != scm_info.current_version:
        logger.warning(
            "Specified version (%s) does not match last tagged version (%s)",
            current_version,
            scm_info.current_version,
        )
        return current_version
    elif current_version:
        return current_version

    raise ConfigurationError("Unable to determine the current version.")


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
    config_file: Union[str, Path, None], current_version: str, new_version: str, dry_run: bool = False
) -> None:
    """
    Update the current_version key in the configuration file.

    If no explicit configuration file is passed, it will search in several files to
    find its configuration.

    Instead of parsing and re-writing the config file with new information, it will use
    a regular expression to just replace the current_version value. The idea is it will
    avoid unintentional changes (like formatting) to the config file.

    Args:
        config_file: The configuration file to explicitly use.
        current_version: The serialized current version.
        new_version: The serialized new version.
        dry_run: True if the update should be a dry run.
    """
    toml_current_version_regex = re.compile(
        f'(?P<section_prefix>\\[tool\\.bumpversion]\n[^[]*current_version\\s*=\\s*)(\\"{current_version}\\")',
        re.MULTILINE,
    )
    cfg_current_version_regex = re.compile(
        f"(?P<section_prefix>\\[bumpversion]\n[^[]*current_version\\s*=\\s*)(?P<version>{current_version})",
        re.MULTILINE,
    )

    if not config_file:
        logger.info("No configuration file found to update.")
        return

    config_path = Path(config_file)
    existing_config = config_path.read_text()
    if config_path.suffix == ".cfg" and cfg_current_version_regex.search(existing_config):
        sub_str = f"\\g<section_prefix>{new_version}"
        new_config = cfg_current_version_regex.sub(sub_str, existing_config)
    elif config_path.suffix == ".toml" and toml_current_version_regex.search(existing_config):
        sub_str = f'\\g<section_prefix>"{new_version}"'
        new_config = toml_current_version_regex.sub(sub_str, existing_config)
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
