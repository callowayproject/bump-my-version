"""Say 'Hello'."""
import rich_click as click


def say_hello(name: str):
    """Output a greeting to the console."""
    click.echo(f"{name} says 'hello'")
