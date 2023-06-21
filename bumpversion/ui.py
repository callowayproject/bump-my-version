"""Utilities for user interface."""
from click import UsageError, echo


def print_info(msg: str) -> None:
    """Echo a message to the console."""
    echo(msg)


def print_error(msg: str) -> None:
    """Raise an error and exit."""
    raise UsageError(msg)
