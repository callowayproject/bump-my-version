"""The ``show`` CLI subcommand implementation."""

from typing import List, Optional

import rich_click as click

from bumpversion import cli_options
from bumpversion.config import get_configuration
from bumpversion.config.files import find_config_file
from bumpversion.show import do_show


@click.command()
@click.argument("args", nargs=-1, type=str)
@cli_options.config_file_option
@click.option(
    "-f",
    "--format",
    "format_",
    required=False,
    envvar="BUMPVERSION_FORMAT",
    type=click.Choice(["default", "yaml", "json"], case_sensitive=False),
    default="default",
    help="Specify the output format.",
)
@click.option(
    "-i",
    "--increment",
    required=False,
    envvar="BUMPVERSION_INCREMENT",
    type=str,
    help="Increment the version component and add `new_version` to the configuration.",
)
@cli_options.current_version_option
def show(
    args: List[str], config_file: Optional[str], format_: str, increment: Optional[str], current_version: Optional[str]
) -> None:
    """
    Show current configuration information.

    ARGS may contain one or more configuration attributes. For example:

    - `bump-my-version show current_version`

    - `bump-my-version show files.0.filename`

    - `bump-my-version show scm_info.branch_name`

    - `bump-my-version show current_version scm_info.distance_to_latest_tag`
    """
    found_config_file = find_config_file(config_file)
    config = get_configuration(found_config_file)

    if not args:
        do_show("all", config=config, format_=format_, increment=increment, current_version=current_version)
    else:
        do_show(*args, config=config, format_=format_, increment=increment, current_version=current_version)
