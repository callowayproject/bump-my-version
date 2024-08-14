---
title: File-specific Configuration
description: Configuration for changing files
icon:
date: 2024-08-11
comments: true
---
# File-specific configuration

This section configures which files Bump My Version should update by replacing their current version with the newly bumped version.

## filename

::: field-list
    required
    : **Yes‡**
    
    default
    : empty
    
    type
    : string

The name of the file to modify.

!!! note

    ‡ This is only used with TOML configuration and is only required if [`glob`](#glob) is _not_ specified. INI-style configuration files specify the file name as part of the grouping.


## glob

::: field-list
    required
    : **Yes‡**
    

    default
    : empty
    
    type
    : string

The glob pattern specifying the files to modify.

!!! note

    ‡ This is only used with TOML configuration, and is only required if [`filename`](#filename) is _not_ specified. INI-style configuration files specify the glob pattern as part of the grouping.

## glob_exclude

::: field-list
    required
    : No
    
    default
    : empty
    
    type
    : list of string

A list of glob patterns to exclude from the files found via the `glob` parameter. Does nothing if `filename` is specified.


## parse

::: field-list

    required
    : No
    
    default
    : the value configured in the global `parse` field
    
    type
    : string

This is an override to the default pattern to parse the version number from this file.

## serialize

::: field-list

    required
    : No
    
    default
    : the value configured in the global `serialize` field
    
    type
    : an array of strings

This is an override to the default templates to serialize the new version number in this file.

## search

::: field-list

    required
    : No
    
    default
    : the value configured in the global `search` field
    
    type
    : string

This is an override to the default template string how to search for the string to be replaced in the file.

## regex

::: field-list

    required
    : No
    
    default
    : the value configured in the global `regex` field
    
    type
    : boolean

If `True`, treat the `search` parameter as a regular expression.

## replace

::: field-list

    required
    : No
    
    default
    : the value configured in the global `replace` field
    
    type
    : string

This is an override to the template to create the string that will replace the current version number in the file.

## ignore_missing_version

::: field-list

    required
    : No
    
    default
    : The value configured in the global `ignore_missing_version` field
    
    type
    : boolean

If `True`, don't fail if the version string to be replaced is not found in the file.

## ignore_missing_file

::: field-list

    required
    : No
    
    default
    : The value configured in the global `ignore_missing_file` field
    
    type
    : boolean

if `True`, don't fail if the configured file is missing.

## include_bumps

::: field-list

    required
    : No
    
    default
    : all version components
    
    type
    : list of strings

The `include_bumps` file configuration allows you to control when bump-my-version includes this file for changes. Its alternative is the `exclude_bumps` configuration. When a `bump <version component>` command is issued, this file is changed only if the version component is in this list and not in [`exclude_bumps`](#exclude_bumps). The [parse](#parse) configuration defines version components.

The default value, or an empty list, includes all version components.

## exclude_bumps

::: field-list

     required
     : No
     
     default
     : `[]`
     
     type
     : list of strings

The `exclude_bumps` file configuration allows you to control when bump-my-version excludes this file for changes. Its alternative is the `include_bumps` configuration. When a `bump <version component>` command is issued, this file is only changed if the version component is *not in this list.* The [parse](#parse) configuration defines version components.

The default value does not exclude anything.

## Examples

=== "TOML"

    TOML allows us to specify the files using an [array of tables.](https://toml.io/en/v1.0.0#array-of-tables) TOML configuration adds two fields to each file configuration: `filename` and `glob`. These fields are mutually exclusive: if you specify a value for both, only the `glob` value is used.
    
    For example, to change `coolapp/__init__.py` with the defaults and alter `CHANGELOG.md` twice:
    
    ```toml
    [[tool.bumpversion.files]]
    filename = "coolapp/__init__.py"
    
    [[tool.bumpversion.files]]
    filename = "CHANGELOG.md"
    search = "Unreleased"
    
    [[tool.bumpversion.files]]
    filename = "CHANGELOG.md"
    search = "{current_version}...HEAD"
    replace = "{current_version}...{new_version}"
    ```

=== "CFG"

    INI-style configuration is in the section: `[bumpversion:file:<filename>]` or `[bumpversion:glob:<glob pattern>]`.
    
    Both, `file:` and `glob:` are configured the same. Their difference is that file will match file names directly like `requirements.txt`. While glob also matches multiple files via wildcards like `**/pom.xml`.
    
    !!! note
    
        The configuration file format requires each section header to be unique. If you want to process a certain file multiple times, you may append a description between parens to the `file` keyword: `[bumpversion:file (special one):…]`.


    
    For example, to change `coolapp/__init__.py` with the defaults and alter `CHANGELOG.md` twice:
    
    ```ini
    [bumpversion:file:coolapp/__init__.py]
    
    [bumpversion:file(version heading):CHANGELOG.md]
    search = Unreleased
    
    [bumpversion:file(previous version):CHANGELOG.md]
    search = {current_version}...HEAD
    replace = {current_version}...{new_version}
    ```
