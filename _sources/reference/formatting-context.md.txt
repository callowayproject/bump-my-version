# Formatting context

These fields are available for

- version serializing
- searching and replacing in files
- commit messages
- tag names
- tag annotations

## Escaped characters

**`#`** The literal hash or [octothorpe](https://www.merriam-webster.com/dictionary/octothorpe) character.

**`;`** The literal semicolon character.


## Date and time fields

**`now`** A Python datetime object representing the current local time, without a time zone reference.

**`utcnow`** A Python datetime object representing the current local time in the UTC time zone.

You can provide [additional formatting guidance](https://docs.python.org/3.11/library/datetime.html#strftime-and-strptime-format-codes) for datetime objects using formatting codes. Put the formatting codes after the field and a colon. For example, `{now:%Y-%m-%d}` would output the current local time as `2023-04-20`.

## Source code management fields

These fields will only have values if the code is in a Git or Mercurial repository.

**`commit_sha`** The latest commit reference.

**`distance_to_latest_tag`** The number of commits since the latest tag.

**`dirty`** A boolean indicating if the current repository has pending changes.

**`branch_name`** The current branch name.

**`short_branch_name`** The current branch name, converted to lowercase, with non-alphanumeric characters removed and truncated to 20 characters. For example, `feature/MY-long_branch-name` would become `featuremylongbranchn`.

## Version fields

**`current_version`** The current version serialized as a string

**`current_<version part>`** Each version part defined by the [version configuration parsing regular expression](version-parts.md#version-configuration). The default configuration would have `current_major`, `current_minor`, and `current_patch` available.

**`new_version`** The new version serialized as a string

**`new_<version part>`** Each version part defined by the [version configuration parsing regular expression](version-parts.md#version-configuration). The default configuration would have `new_major`, `new_minor`, and `new_patch` available.

:::{note}
The following fields are only available when serializing a version.
:::

**`<version part>`** Each version part defined by the [version configuration parsing regular expression](version-parts.md#version-configuration). The default configuration would have `major`, `minor`, and `patch` available.

## Environment variables

Every environment variable available at runtime is included with a `$` prefix. For example if `USER` was in the environment, `{$USER}` would render that value.

If you use environment variables in your version serialization, you might want to ensure they are set by executing `export VAR=value` before running the `bump-my-version` command.
