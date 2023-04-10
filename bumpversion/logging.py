"""Logging configuration for bumpversion."""
import logging

import click
from rich.logging import RichHandler

logger = logging.getLogger("bumpversion")

VERBOSITY = {
    0: logging.WARNING,
    1: logging.INFO,
    2: logging.DEBUG,
}


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
    root_logger = logging.getLogger("")
    root_logger.setLevel(VERBOSITY.get(verbose, logging.DEBUG))
