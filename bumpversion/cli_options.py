"""
Shared Click option decorators for bump-my-version commands.

Module-level constants cover options that are identical across every command that
uses them.  Factory functions are provided for options whose type or default
intentionally differs between commands, so divergence cannot happen silently.
"""

from typing import Callable

import rich_click as click

from bumpversion.click_config import config_option

# ---------------------------------------------------------------------------
# Options shared across multiple commands (identical in every command)
# ---------------------------------------------------------------------------

config_file_option: Callable = config_option(
    "--config-file",
    envvar="BUMPVERSION_CONFIG_FILE",
    help="Config file to read most of the variables from.",
)

verbose_option: Callable = click.option(
    "-v",
    "--verbose",
    count=True,
    required=False,
    envvar="BUMPVERSION_VERBOSE",
    help="Print verbose logging to stderr. Can specify several times for more verbosity.",
)

allow_dirty_option: Callable = click.option(
    "--allow-dirty/--no-allow-dirty",
    default=None,
    required=False,
    envvar="BUMPVERSION_ALLOW_DIRTY",
    help="Don't abort if working directory is dirty, or explicitly abort if dirty.",
)

current_version_option: Callable = click.option(
    "--current-version",
    metavar="VERSION",
    required=False,
    envvar="BUMPVERSION_CURRENT_VERSION",
    help="Version that needs to be updated",
)

new_version_option: Callable = click.option(
    "--new-version",
    metavar="VERSION",
    required=False,
    envvar="BUMPVERSION_NEW_VERSION",
    help="New version that should be in the files",
)

parse_option: Callable = click.option(
    "--parse",
    metavar="REGEX",
    required=False,
    envvar="BUMPVERSION_PARSE",
    help="Regex parsing the version string",
)

serialize_option: Callable = click.option(
    "--serialize",
    metavar="FORMAT",
    multiple=True,
    required=False,
    envvar="BUMPVERSION_SERIALIZE",
    help="How to format what is parsed back to a version",
)

search_option: Callable = click.option(
    "--search",
    metavar="SEARCH",
    required=False,
    envvar="BUMPVERSION_SEARCH",
    help="Template for complete string to search",
)

replace_str_option: Callable = click.option(
    "--replace",
    metavar="REPLACE",
    required=False,
    envvar="BUMPVERSION_REPLACE",
    help="Template for complete string to replace",
)

regex_option: Callable = click.option(
    "--regex/--no-regex",
    default=None,
    envvar="BUMPVERSION_REGEX",
    help="Treat the search parameter as a regular expression or explicitly do not treat it as a regular expression.",
)

no_configured_files_option: Callable = click.option(
    "--no-configured-files",
    is_flag=True,
    envvar="BUMPVERSION_NO_CONFIGURED_FILES",
    help=(
        "Only replace the version in files specified on the command line, "
        "ignoring the files from the configuration file."
    ),
)

dry_run_option: Callable = click.option(
    "--dry-run",
    "-n",
    is_flag=True,
    envvar="BUMPVERSION_DRY_RUN",
    help="Don't write any files, just pretend.",
)

# ---------------------------------------------------------------------------
# Options whose type or default intentionally differ between commands
# ---------------------------------------------------------------------------


def ignore_missing_files_option(is_flag: bool = False) -> Callable:
    """Return the ``--ignore-missing-files`` Click option decorator.

    Args:
        is_flag: When ``True``, returns a simple boolean flag with no ``--no-``
            counterpart (used by the ``replace`` command).  When ``False``
            (default), returns a tri-state ``--flag/--no-flag`` option whose
            default is ``None``, letting the config-file value win when the
            flag is omitted (used by the ``bump`` command).

    Returns:
        A Click option decorator ready to be applied with ``@``.
    """
    if is_flag:
        return click.option(
            "--ignore-missing-files",
            is_flag=True,
            envvar="BUMPVERSION_IGNORE_MISSING_FILES",
            help="Ignore any missing files when searching and replacing in files.",
        )
    return click.option(
        "--ignore-missing-files/--no-ignore-missing-files",
        default=None,
        envvar="BUMPVERSION_IGNORE_MISSING_FILES",
        help="Ignore any missing files when searching and replacing in files.",
    )


def ignore_missing_version_option(is_flag: bool = False) -> Callable:
    """Return the ``--ignore-missing-version`` Click option decorator.

    Args:
        is_flag: When ``True``, returns a simple boolean flag with no ``--no-``
            counterpart (used by the ``replace`` command).  When ``False``
            (default), returns a tri-state ``--flag/--no-flag`` option whose
            default is ``None``, letting the config-file value win when the
            flag is omitted (used by the ``bump`` command).

    Returns:
        A Click option decorator ready to be applied with ``@``.
    """
    if is_flag:
        return click.option(
            "--ignore-missing-version",
            is_flag=True,
            envvar="BUMPVERSION_IGNORE_MISSING_VERSION",
            help="Ignore any Version Not Found errors when searching and replacing in files.",
        )
    return click.option(
        "--ignore-missing-version/--no-ignore-missing-version",
        default=None,
        envvar="BUMPVERSION_IGNORE_MISSING_VERSION",
        help="Ignore any Version Not Found errors when searching and replacing in files.",
    )


# ---------------------------------------------------------------------------
# Bump-only options (commit / tag / signing)
# ---------------------------------------------------------------------------

commit_option: Callable = click.option(
    "--commit/--no-commit",
    default=None,
    envvar="BUMPVERSION_COMMIT",
    help="Commit to version control",
)

tag_option: Callable = click.option(
    "--tag/--no-tag",
    default=None,
    envvar="BUMPVERSION_TAG",
    help="Create a tag in version control",
)

sign_tags_option: Callable = click.option(
    "--sign-tags/--no-sign-tags",
    default=None,
    envvar="BUMPVERSION_SIGN_TAGS",
    help="Sign tags if created",
)

tag_name_option: Callable = click.option(
    "--tag-name",
    metavar="TAG_NAME",
    required=False,
    envvar="BUMPVERSION_TAG_NAME",
    help="Tag name (only works with --tag)",
)

tag_message_option: Callable = click.option(
    "--tag-message",
    metavar="TAG_MESSAGE",
    required=False,
    envvar="BUMPVERSION_TAG_MESSAGE",
    help="Tag message",
)

message_option: Callable = click.option(
    "-m",
    "--message",
    metavar="COMMIT_MSG",
    required=False,
    envvar="BUMPVERSION_MESSAGE",
    help="Commit message",
)

commit_args_option: Callable = click.option(
    "--commit-args",
    metavar="COMMIT_ARGS",
    required=False,
    envvar="BUMPVERSION_COMMIT_ARGS",
    help="Extra arguments to commit command",
)
