"""The ``bump`` CLI subcommand implementation."""

from typing import List, Optional

import rich_click as click

from bumpversion import __version__, cli_options
from bumpversion.bump import do_bump
from bumpversion.config import get_configuration
from bumpversion.config.files import find_config_file
from bumpversion.ui import get_indented_logger, setup_logging
from bumpversion.utils import get_overrides

logger = get_indented_logger(__name__)


@click.command(context_settings={"ignore_unknown_options": True})
@click.argument("args", nargs=-1, type=str)
@cli_options.config_file_option
@cli_options.verbose_option
@cli_options.allow_dirty_option
@cli_options.current_version_option
@cli_options.new_version_option
@cli_options.parse_option
@cli_options.serialize_option
@cli_options.search_option
@cli_options.replace_str_option
@cli_options.regex_option
@cli_options.no_configured_files_option
@cli_options.ignore_missing_files_option()
@cli_options.ignore_missing_version_option()
@cli_options.dry_run_option
@cli_options.commit_option
@cli_options.tag_option
@cli_options.sign_tags_option
@cli_options.tag_name_option
@cli_options.tag_message_option
@cli_options.message_option
@cli_options.commit_args_option
def bump(
    args: list,
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
    ignore_missing_files: bool,
    ignore_missing_version: bool,
    dry_run: bool,
    commit: Optional[bool],
    tag: Optional[bool],
    sign_tags: Optional[bool],
    tag_name: Optional[str],
    tag_message: Optional[str],
    message: Optional[str],
    commit_args: Optional[str],
) -> None:
    """
    Change the version.

    ARGS may contain any of the following:

    VERSION_PART is the part of the version to increase, e.g. `minor`.
    Valid values include those given in the `--serialize` / `--parse` option.

    FILES are additional file(s) to modify.
    If you want to rewrite only files specified on the command line, use with the
    `--no-configured-files` option.
    """
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
        ignore_missing_files=ignore_missing_files,
        ignore_missing_version=ignore_missing_version,
        regex=regex,
    )

    found_config_file = find_config_file(config_file)
    config = get_configuration(found_config_file, **overrides)
    if args:
        if args[0] not in config.parts.keys():
            raise click.BadArgumentUsage(f"Unknown version component: {args[0]}")
        version_part = args[0]
        files = args[1:]
    else:
        version_part = None
        files = args

    config.allow_dirty = allow_dirty if allow_dirty is not None else config.allow_dirty
    if not config.allow_dirty and config.scm_info.tool:
        config.scm_info.tool.assert_nondirty()

    if no_configured_files:
        config.excluded_paths = list(config.resolved_filemap.keys())

    if files:
        config.add_files(files)
        config.included_paths = files

    logger.dedent()
    do_bump(version_part, new_version, config, found_config_file, dry_run)
