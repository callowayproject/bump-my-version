"""The ``show-bump`` CLI subcommand implementation."""

from typing import Optional

import rich_click as click

from bumpversion import cli_options
from bumpversion.config import get_configuration
from bumpversion.config.files import find_config_file
from bumpversion.ui import setup_logging
from bumpversion.visualize import visualize


@click.command(name="show-bump")
@click.argument("version", nargs=1, type=str, required=False, default="")
@cli_options.config_file_option
@click.option("--ascii", is_flag=True, help="Use ASCII characters only.")
@cli_options.verbose_option
def show_bump(version: str, config_file: Optional[str], ascii: bool, verbose: int) -> None:
    """Show the possible versions resulting from the bump subcommand."""
    setup_logging(verbose)
    found_config_file = find_config_file(config_file)
    config = get_configuration(found_config_file)
    if not version:
        version = config.current_version
    box_style = "ascii" if ascii else "light"
    visualize(config=config, version_str=version, box_style=box_style)
