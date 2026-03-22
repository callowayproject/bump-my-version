"""The ``replace`` CLI subcommand implementation."""

from typing import List, Optional

import rich_click as click

from bumpversion import __version__, cli_options
from bumpversion.config import get_configuration
from bumpversion.config.files import find_config_file
from bumpversion.context import get_context
from bumpversion.files import ConfiguredFile, modify_files
from bumpversion.ui import get_indented_logger, setup_logging
from bumpversion.utils import get_overrides

logger = get_indented_logger(__name__)


@click.command()
@click.argument("files", nargs=-1, type=str)
@cli_options.config_file_option
@cli_options.verbose_option
@cli_options.allow_dirty_option
@cli_options.current_version_option
@click.option(
    "--new-version",
    metavar="VERSION",
    required=False,
    envvar="BUMPVERSION_NEW_VERSION",
    help="New version that should be in the files. If not specified, it will be None.",
)
@cli_options.parse_option
@cli_options.serialize_option
@cli_options.search_option
@cli_options.replace_str_option
@cli_options.regex_option
@cli_options.no_configured_files_option
@cli_options.ignore_missing_version_option(is_flag=True)
@cli_options.ignore_missing_files_option(is_flag=True)
@cli_options.dry_run_option
def replace(
    files: list,
    config_file: Optional[str],
    verbose: int,
    allow_dirty: Optional[bool],
    current_version: Optional[str],
    new_version: Optional[str],
    parse: Optional[str],
    serialize: Optional[List[str]],
    search: Optional[str],
    replace: Optional[str],
    regex: Optional[bool],
    no_configured_files: bool,
    ignore_missing_version: bool,
    ignore_missing_files: bool,
    dry_run: bool,
) -> None:
    """
    Replace the version in files.

    FILES are additional file(s) to modify.
    If you want to rewrite only files specified on the command line, use with the
    `--no-configured-files` option.
    """
    setup_logging(verbose)

    logger.info("Starting BumpVersion %s", __version__)

    overrides = get_overrides(
        allow_dirty=allow_dirty,
        current_version=current_version,
        new_version=new_version,
        parse=parse,
        serialize=serialize or None,
        commit=False,
        tag=False,
        sign_tags=False,
        tag_name=None,
        tag_message=None,
        message=None,
        commit_args=None,
        ignore_missing_version=ignore_missing_version,
        ignore_missing_files=ignore_missing_files,
        regex=regex,
    )

    found_config_file = find_config_file(config_file)
    config = get_configuration(found_config_file, **overrides)

    config.allow_dirty = allow_dirty if allow_dirty is not None else config.allow_dirty
    if not config.allow_dirty and config.scm_info.tool:
        config.scm_info.tool.assert_nondirty()

    if no_configured_files:
        config.excluded_paths = list(config.resolved_filemap.keys())

    if files:
        config.add_files(files)
        config.included_paths = files

    configured_files = [
        ConfiguredFile(file_cfg, config.version_config, search, replace) for file_cfg in config.files_to_modify
    ]

    version = config.version_config.parse(config.current_version)
    if new_version:
        next_version = config.version_config.parse(new_version)
    else:
        next_version = None

    ctx = get_context(config, version, next_version)

    modify_files(configured_files, version, next_version, ctx, dry_run)
