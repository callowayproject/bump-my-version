"""The ``check`` CLI subcommand implementation."""

from typing import Optional

import rich_click as click

from bumpversion import __version__, cli_options
from bumpversion.check import do_check
from bumpversion.config import get_configuration
from bumpversion.config.files import find_config_file
from bumpversion.ui import get_indented_logger, print_info, setup_logging
from bumpversion.utils import get_overrides

logger = get_indented_logger(__name__)


@click.command()
@cli_options.config_file_option
@cli_options.verbose_option
@cli_options.current_version_option
@click.option(
    "--release-tag",
    metavar="TAG",
    required=False,
    envvar="BUMPVERSION_RELEASE_TAG",
    help="The tag being released. Fail unless it matches `tag_name` rendered with the current version.",
)
@click.pass_context
def check(
    ctx: click.Context,
    config_file: Optional[str],
    verbose: int,
    current_version: Optional[str],
    release_tag: Optional[str],
) -> None:
    """
    Check that every configured file contains the current version.

    Nothing is changed. Exits with a non-zero status when a file does not contain the version
    (as the next `bump` would search for it), or when `--release-tag` does not match it.

    Useful in CI/CD to block a release whose files were not bumped, ex.
    `bump-my-version check --release-tag "$GITHUB_REF_NAME"`.
    """
    setup_logging(verbose)

    logger.info("Starting BumpVersion %s", __version__)

    found_config_file = find_config_file(config_file)
    config = get_configuration(found_config_file, **get_overrides(current_version=current_version))

    if problems := do_check(config, release_tag):
        for problem in problems:
            click.secho(problem, fg="red", err=True)
        ctx.exit(1)

    print_info(f"Version {config.current_version} is consistent across the configured files.")
