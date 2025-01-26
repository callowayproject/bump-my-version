"""Utilities for user interface."""

import logging
import sys

import click
from click import UsageError, secho
from rich.logging import RichHandler
from rich.padding import Padding
from rich.panel import Panel
from rich_click.rich_help_formatter import RichHelpFormatter

from bumpversion.indented_logger import IndentedLoggerAdapter

logger = logging.getLogger("bumpversion")

VERBOSITY = {
    0: (logging.WARNING, "%(message)s"),
    1: (logging.INFO, "%(message)s"),
    2: (logging.DEBUG, "%(message)s"),
    3: (logging.DEBUG, "%(message)s %(pathname)s:%(lineno)d"),
}


def get_indented_logger(name: str) -> "IndentedLoggerAdapter":
    """Get a logger with indentation."""
    return IndentedLoggerAdapter(logging.getLogger(name))


def setup_logging(verbose: int = 0) -> None:
    """Configure the logging."""
    verbosity, log_format = VERBOSITY.get(verbose, VERBOSITY[3])
    logging.basicConfig(
        level=verbosity,
        format=log_format,
        datefmt="[%X]",
        handlers=[
            RichHandler(
                rich_tracebacks=True, show_level=False, show_path=False, show_time=False, tracebacks_suppress=[click]
            )
        ],
    )
    root_logger = get_indented_logger("")
    root_logger.setLevel(verbosity)


def print_info(msg: str) -> None:
    """Echo a message to the console."""
    secho(msg)


def print_error(msg: str) -> None:
    """Raise an error and exit."""
    raise UsageError(msg)


def print_warning(msg: str) -> None:
    """Echo a warning to the console."""
    formatter = RichHelpFormatter(file=sys.stderr)
    config = formatter.config

    formatter.write(
        Padding(
            Panel(
                formatter.highlighter(msg),
                border_style="yellow",
                title="Warning",
                title_align=config.align_errors_panel,
            ),
            (0, 0, 1, 0),
        )
    )
