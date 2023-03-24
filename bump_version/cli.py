"""bump-my-version Command line interface."""

import logging

import rich_click as click
from bump_version import __version__

LOGGING_LEVELS = {
    0: logging.NOTSET,
    1: logging.ERROR,
    2: logging.WARN,
    3: logging.INFO,
    4: logging.DEBUG,
}  #: a mapping of `verbose` option counts to logging levels


class Info:
    """An information object to pass data between CLI functions."""

    def __init__(self):  # Note: This constructor must not accept parameters
        """Create a new instance."""
        self.verbose: int = 0


# pass_info is a decorator for functions that pass 'Info' objects.
#: pylint: disable=invalid-name
pass_info = click.make_pass_decorator(Info, ensure=True)


@click.group()
@click.option("--verbose", "-v", count=True, help="Enable verbose output.")
@click.version_option(version=__version__)
@pass_info
def cli(info: Info, verbose: int):
    """Version bump your Python project."""
    # Use the verbosity count to determine the logging level...
    if verbose > 0:
        logging.basicConfig(level=LOGGING_LEVELS[verbose] if verbose in LOGGING_LEVELS else logging.DEBUG)
        click.echo(
            click.style(
                f"Verbose logging is enabled. (LEVEL={logging.getLogger().getEffectiveLevel()})",
                fg="yellow",
            )
        )
    info.verbose = verbose


@cli.command()
@pass_info
def hello(_: Info):
    """Say 'hello' to the nice people."""
    from bump_version.commands import say_hello

    say_hello.say_hello("bump-my-version")
