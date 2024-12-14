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
    0: logging.WARNING,
    1: logging.INFO,
    2: logging.DEBUG,
}


def get_indented_logger(name: str) -> "IndentedLoggerAdapter":
    """Get a logger with indentation."""
    return IndentedLoggerAdapter(logging.getLogger(name))


def setup_logging(verbose: int = 0) -> None:
    """Configure the logging."""
    logging.basicConfig(
        level=VERBOSITY.get(verbose, logging.DEBUG),
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                rich_tracebacks=True, show_level=False, show_path=False, show_time=False, tracebacks_suppress=[click]
            )
        ],
    )
    root_logger = get_indented_logger("")
    root_logger.setLevel(VERBOSITY.get(verbose, logging.DEBUG))


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
