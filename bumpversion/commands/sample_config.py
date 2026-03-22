"""The ``sample-config`` CLI subcommand implementation."""

from pathlib import Path

import questionary
import rich_click as click
from tomlkit import dumps

from bumpversion.config.create import create_configuration
from bumpversion.ui import print_info


@click.command(name="sample-config")
@click.option(
    "--prompt/--no-prompt",
    default=True,
    help="Ask the user questions about the configuration.",
)
@click.option(
    "--destination",
    default="stdout",
    help="Where to write the sample configuration.",
    type=click.Choice(["stdout", ".bumpversion.toml", "pyproject.toml"]),
)
def sample_config(prompt: bool, destination: str) -> None:
    """Print a sample configuration file."""
    if prompt:
        destination = questionary.select(
            "Destination", choices=["stdout", ".bumpversion.toml", "pyproject.toml"], default=destination
        ).ask()

    destination_config = create_configuration(destination, prompt)

    if destination == "stdout":
        print_info(dumps(destination_config))
    else:
        Path(destination).write_text(dumps(destination_config), encoding="utf-8")
