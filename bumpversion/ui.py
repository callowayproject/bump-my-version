"""Utilities for user interface."""
from click import UsageError, secho


def print_info(msg: str) -> None:
    """Echo a message to the console."""
    secho(msg)


def print_error(msg: str) -> None:
    """Raise an error and exit."""
    raise UsageError(msg)


def print_warning(msg: str) -> None:
    """Echo a warning to the console."""
    secho(f"\nWARNING:\n\n{msg}\n", fg="yellow")
