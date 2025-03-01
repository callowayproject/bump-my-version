---
title: Global Configuration
description: Configuration values that affect all of Bump My Version
icon:
date: 2024-08-11
comments: true
---
# Global Configuration

The general configuration is grouped in a `[tool.bumpversion]` or  `[bumpversion]` section, depending on if it is a TOML or INI file, respectfully.

## allow_dirty

::: field-list
    required
    :   No
    
    default
    :   `False` 
    
    type
    :   boolean
    
    command line option
    :   `--allow-dirty | --no-allow-dirty`
    
    environment var
    :   `BUMPVERSION_ALLOW_DIRTY`


Bump-my-version's default behavior is to abort if the working directory has uncommitted changes. This protects you from releasing unversioned files and overwriting unsaved changes.

## commit

::: field-list
    required
    :   No
    
    default
    :   `False` (Don't create a commit)
    
    type
    :   boolean
    
    command line option
    :   `--commit | --no-commit`
    
    environment var
    :   `BUMPVERSION_COMMIT`

Whether to create a commit using git or Mercurial.

If you have pre-commit hooks, add an option to [`commit_args`](global.md#commit_args) to turn off your pre-commit hooks. For Git, use `--no-verify` and use `--config hooks.pre-commit=` for Mercurial.

## commit_args

::: field-list

    required
    : No
    
    default
    : `""`
    
    type
    : string
    
    command line option
    : `--commit-args`
    
    environment var
    : `BUMPVERSION_COMMIT_ARGS`

Extra arguments to pass to commit command. This is only used when the [`commit`](global.md#commit) option is set to `True`.

If you have pre-commit hooks, add an option to turn off your pre-commit hooks. For Git, use `--no-verify` and use `--config hooks.pre-commit=` for Mercurial.

## current_version

::: field-list

    required
    : **Yes‡**
    
    default
    : `""`
    
    type
    : string
    
    command line option
    : `--current-version`
    
    environment var
    : `BUMPVERSION_CURRENT_VERSION`

The current version of the software package before bumping. A value for this is required, unless a fallback value is found.

!!! note

    ‡ If `pyproject.toml` exists, then `current_version` falls back to `project.version` in `pyproject.toml`. This only works if `project.version` is statically set.

## ignore_missing_files

::: field-list

    required
    : No
    
    default
    : `False`
    
    type
    : boolean
    
    command line option
    : `--ignore-missing-files`
    
    environment var
    : `BUMPVERSION_IGNORE_MISSING_FILES`

If `True`, don't fail if the configured file is missing.

## ignore_missing_version

::: field-list
    required
    : No
    
    default
    : `False`
    
    type
    : boolean
    
    command line option
    : `--ignore-missing-version`
    
    environment var
    : `BUMPVERSION_IGNORE_MISSING_VERSION`

If `True`, don't fail if the version string to be replaced is not found in the file.

## message

::: field-list

    required
    :   No
    
    default
    :   `Bump version: {current_version} → {new_version}`
    
    type
    :   string
    
    command line option
    :   `--message`
    
    environment var
    :   `BUMPVERSION_MESSAGE`

The commit message template to use when creating a commit. This is only used when the [`commit`](global.md#commit) option is set to `True`.

This string is templated using the [Python Format String Syntax](https://docs.python.org/3/library/string.html#format-string-syntax). The [formatting context reference](../formatting-context.md) describes the available variables.

## parse

::: field-list
    required
    : No
    
    default
    : `(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)`
    
    type
    : string
    
    command line option
    : `--parse`
    
    environment var
    : `BUMPVERSION_PARSE`

This is the default regular expression ([Python regular expression syntax](https://docs.python.org/3/library/re.html#regular-expression-syntax)) for finding and parsing the version string into its components. Individual part or file configurations may override this.

The regular expression must be able to parse all strings produced by the configured [`serialize`](global.md#serialize) value. Named matching groups ("`(?P<name>...)`") indicate the version part the matched value belongs to.

## regex

::: field-list

    required
    : No
    
    default
    : `False`
    
    type
    : boolean
    
    command line option
    : `--regex | --no-regex`
    
    environment var
    : `BUMPVERSION_REGEX`

Treat the `search` string as a regular expression.

## replace

::: field-list
    required
    : No
    
    default
    : `{new_version}`
    
    type
    : string
    
    command line option
    : `--replace`
    
    environment var
    : `BUMPVERSION_REPLACE`

This is the template to create the string that will replace the current version number in the file.

## search

::: field-list
    required
    : No
    
    default
    : `{current_version}`
    
    type
    : string
    
    command line option
    : `--search`
    
    environment var
    : `BUMPVERSION_SEARCH`

This is the template string for searching. It is rendered using the [formatting context](../formatting-context.md) for searching in the file. Individual file configurations may override this. This can span multiple lines and is templated using [Python Format String Syntax](https://docs.python.org/3/library/string.html#format-string-syntax). The [formatting context reference](../formatting-context.md) describes the available variables.

This is useful if there is the remotest possibility that the current version number might be present multiple times in the file and you mean to bump only one of the occurrences.

## serialize

::: field-list
    required
    : No
    
    default
    : `["{major}.{minor}.{patch}"]`
    
    type
    : an array of strings
    
    command line option
    : `--serialize`
    
    environment var
    : `BUMPVERSION_SERIALIZE`

This is the default list of templates specifying how to serialize the version parts back to a version string. Individual part or file configurations may override this.

Since version parts can be optional, bumpversion will try the serialization formats beginning with the first and choose the last one where all values can all non-optional values are represented.

In this example (in TOML):

```toml
serialize = [
    "{major}.{minor}.{patch}",
    "{major}.{minor}",
    "{major}"
]
```

Since `0` is optional by default, Version `1.8.9` will serialize to  `1.8.9`, `1.9.0` will serialize to `1.9`, and version `2.0.0` will serialize as `2`. 

Each string is templated using the [Python Format String Syntax](https://docs.python.org/3/library/string.html#format-string-syntax). The [formatting context reference](../formatting-context.md) describes the available variables.

## sign_tags

::: field-list

    required
    : No
    
    default
    : `False` (Don't sign tags)
    
    type
    : boolean
    
    command line option
    : `--sign-tags | --no-sign-tags`
    
    environment var
    : `BUMPVERSION_SIGN_TAGS`

If `True`, sign the created tag, when [`tag`](global.md#tag) is `True`.

## tag

::: field-list

    required
    : No
    
    default
    : `False` (Don't create a tag)
    
    type
    : boolean
    
    command line option
    : `--tag | --no-tag`
    
    environment var
    : `BUMPVERSION_TAG`

If `True`, create a tag after committing the changes. The tag is named using the [`tag_name`](global.md#tag_name) option. 

If you are using `git`, don't forget to `git-push` with the `--tags` flag when you are done.

## tag_message

::: field-list
    required
    : No
    
    default
    : `Bump version: {current_version} → {new_version}`
    
    type
    : string
    
    command line option
    : `--tag-message`
    
    environment var
    : `BUMPVERSION_TAG_MESSAGE`

The tag message template to use when creating a tag when [`tag`](global.md#tag) is `True`

This string is templated using the [Python Format String Syntax](https://docs.python.org/3/library/string.html#format-string-syntax). The [formatting context reference](../formatting-context.md) describes the available variables.

Bump My Version creates an *annotated* tag in Git by default. To turn this off and create a *lightweight* tag, you must explicitly set an empty `tag_message` value.

## tag_name

::: field-list

    required
    : No
    
    default
    : `v{new_version}`
    
    type
    : string
    
    command line option
    : `--tag-name`
    
    environment var
    : `BUMPVERSION_TAG_NAME`

The template used to render the tag when [`tag`](global.md#tag) is `True`.

This string is templated using the [Python Format String Syntax](https://docs.python.org/3/library/string.html#format-string-syntax). The [formatting context reference](../formatting-context.md) describes the available variables.

## Examples

=== "TOML"

    ```toml
    [tool.bumpversion]
    allow_dirty = false
    commit = false
    message = "Bump version: {current_version} → {new_version}"
    commit_args = ""
    tag = false
    sign_tags = false
    tag_name = "v{new_version}"
    tag_message = "Bump version: {current_version} → {new_version}"
    current_version = "1.0.0"
    parse = "(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+)"
    serialize = [
        "{major}.{minor}.{patch}"
    ]
    search = "{current_version}"
    replace = "{new_version}"
    ```

=== "CFG"

    ```ini
    [bumpversion]
    allow_dirty = False
    commit = False
    message = Bump version: {current_version} → {new_version}
    commit_args = 
    tag = False
    sign_tags = False
    tag_name = v{new_version}
    tag_message = Bump version: {current_version} → {new_version}
    current_version = 1.0.0
    parse = (?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)
    serialize =
        {major}.{minor}.{patch}
    search = {current_version}
    replace = {new_version}
    ```
