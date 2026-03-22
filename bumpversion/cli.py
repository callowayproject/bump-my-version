"""bump-my-version Command line interface."""

import rich_click as click
from click.core import Context

from bumpversion import __version__
from bumpversion.commands import bump, replace, sample_config, show, show_bump


@click.group(
    context_settings={
        "help_option_names": ["-h", "--help"],
    },
    add_help_option=True,
)
@click.version_option(version=__version__)
@click.pass_context
def cli(ctx: Context) -> None:
    """Version bump your Python project."""
    pass


click.rich_click.OPTION_GROUPS = {
    "bumpversion bump": [
        {
            "name": "Configuration",
            "options": [
                "--config-file",
                "--current-version",
                "--new-version",
                "--parse",
                "--serialize",
                "--search",
                "--replace",
                "--no-configured-files",
                "--ignore-missing-files",
                "--ignore-missing-version",
            ],
        },
        {
            "name": "Output",
            "options": ["--dry-run", "--verbose"],
        },
        {
            "name": "Committing and tagging",
            "options": [
                "--allow-dirty",
                "--commit",
                "--commit-args",
                "--message",
                "--tag",
                "--tag-name",
                "--tag-message",
                "--sign-tags",
            ],
        },
    ]
}

cli.add_command(bump)
cli.add_command(show)
cli.add_command(replace)
cli.add_command(sample_config)
cli.add_command(show_bump)
