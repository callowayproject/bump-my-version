"""bump-my-version Command line interface."""
import logging
from typing import Optional

import rich_click as click

# from click.core import Context
from bumpversion import __version__

# from bumpversion.aliases import AliasedGroup
from bumpversion.bump import do_bump
from bumpversion.config import find_config_file, get_configuration
from bumpversion.logging import setup_logging
from bumpversion.utils import get_overrides

logger = logging.getLogger(__name__)


# @click.group(cls=AliasedGroup)
# @click.version_option(version=__version__)
# @click.pass_context
# def cli(ctx: Context) -> None:
#     """Version bump your Python project."""
#     if ctx.invoked_subcommand is None:
#         ctx.invoke(bump)


@click.command(context_settings={"ignore_unknown_options": True})
@click.version_option(version=__version__)
@click.argument("version_part")
@click.argument("files", nargs=-1, type=click.Path())
@click.option(
    "--config-file",
    metavar="FILE",
    required=False,
    type=click.Path(exists=True),
    help="Config file to read most of the variables from.",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    required=False,
    help="Print verbose logging to stderr",
)
@click.option(
    "--allow-dirty/--no-allow-dirty",
    default=None,
    required=False,
    help="Don't abort if working directory is dirty, or explicitly abort if dirty.",
)
@click.option(
    "--current-version",
    metavar="VERSION",
    required=False,
    help="Version that needs to be updated",
)
@click.option(
    "--new-version",
    metavar="VERSION",
    required=False,
    help="New version that should be in the files",
)
@click.option(
    "--parse",
    metavar="REGEX",
    required=False,
    help="Regex parsing the version string",
)
@click.option(
    "--serialize",
    metavar="FORMAT",
    multiple=True,
    required=False,
    help="How to format what is parsed back to a version",
)
@click.option(
    "--search",
    metavar="SEARCH",
    required=False,
    help="Template for complete string to search",
)
@click.option(
    "--replace",
    metavar="REPLACE",
    required=False,
    help="Template for complete string to replace",
)
@click.option(
    "--no-configured-files",
    is_flag=True,
    help=(
        "Only replace the version in files specified on the command line, "
        "ignoring the files from the configuration file."
    ),
)
@click.option(
    "--dry-run",
    "-n",
    is_flag=True,
    help="Don't write any files, just pretend.",
)
@click.option(
    "--commit/--no-commit",
    default=None,
    help="Commit to version control",
)
@click.option(
    "--tag/--no-tag",
    default=None,
    help="Create a tag in version control",
)
@click.option(
    "--sign-tags/--no-sign-tags",
    default=None,
    help="Sign tags if created",
)
@click.option(
    "--tag-name",
    metavar="TAG_NAME",
    required=False,
    help="Tag name (only works with --tag)",
)
@click.option(
    "--tag-message",
    metavar="TAG_MESSAGE",
    required=False,
    help="Tag message",
)
@click.option(
    "-m",
    "--message",
    metavar="COMMIT_MSG",
    required=False,
    help="Commit message",
)
@click.option(
    "--commit-args",
    metavar="COMMIT_ARGS",
    required=False,
    help="Extra arguments to commit command",
)
def cli(
    version_part: str,
    files: list,
    config_file: Optional[str],
    verbose: int,
    allow_dirty: Optional[bool],
    current_version: Optional[str],
    new_version: Optional[str],
    parse: Optional[str],
    serialize: Optional[list[str]],
    search: Optional[str],
    replace: Optional[str],
    no_configured_files: bool,
    dry_run: bool,
    commit: Optional[bool],
    tag: Optional[bool],
    sign_tags: Optional[bool],
    tag_name: Optional[str],
    tag_message: Optional[str],
    message: Optional[str],
    commit_args: Optional[str],
) -> None:
    """Change the version."""
    setup_logging(verbose)

    logger.info("Starting BumpVersion %s", __version__)

    overrides = get_overrides(
        allow_dirty=allow_dirty,
        current_version=current_version,
        parse=parse,
        serialize=serialize or None,
        search=search,
        replace=replace,
        commit=commit,
        tag=tag,
        sign_tags=sign_tags,
        tag_name=tag_name,
        tag_message=tag_message,
        message=message,
        commit_args=commit_args,
    )

    found_config_file = find_config_file(config_file)
    config = get_configuration(found_config_file, **overrides)

    config.allow_dirty = allow_dirty if allow_dirty is not None else config.allow_dirty
    if not config.allow_dirty and config.scm_info.tool:
        config.scm_info.tool.assert_nondirty()

    if no_configured_files:
        config.files = []

    if files:
        config.add_files(files)

    do_bump(version_part, new_version, config, found_config_file, dry_run)


def _log_list(config: dict, new_version: str) -> None:
    """Output configuration with new version."""
    logger.info("new_version=%s", new_version)
    for key, value in config.items():
        logger.info("%s=%s", key, value)
