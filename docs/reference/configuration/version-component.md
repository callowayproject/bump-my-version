---
title: Version component-specific configuration
description: Configuration options for a specific version part
icon:
date: 2024-08-11
comments: true
---
# Version component-specific configuration

Version component configuration is grouped in a `[tool.bumpversion.parts.<partname>]` or  `[bumpversion:part:<partname>]` section, depending on if it is a TOML or INI file, respectfully.

You only need to configure version parts if they deviate from the default, and then you only need to specify the overridden options.

## values

::: field-list
    required
    : No
    
    default
    : numeric (i.e. `0`, `1`, `2`, …)
    
    type
    : array of strings

An explicit list of all values to iterate through when bumping this part. An empty array is treated as indicating `numeric` values.

## optional_value

::: field-list
    required
    : No
    
    default
    : The first entry in `values`, `0` when using numeric values
    
    type
    : string

When the version part matches this value, it is considered optional when serializing the final version string.

!!! note

    Numeric values are still treated as strings internally, so when specifying an optional value, you must use a string.


## first_value

::: field-list
    required
    : No

    default
    : The first entry in `values`, `0` when using numeric values
    
    type
    : string

When the part is reset, the value will be set to the value specified here.

!!! note

    Numeric values are still treated as strings internally, so when specifying a first value, you must use a string.


## independent

::: field-list
    required
    : No
    
    default
    : `False`
    
    type
    : boolean

When this value is set to `True`, the part is not reset when other parts are incremented. Its incrementation is
independent of the other parts. It is useful when you have a build number in your version that is incremented independently of the actual version.

## always_increment

::: field-list
    required
    : No

    default
    : `False` (`True` if `calver_format` is set)
    
    type
    : boolean

When this value is set to `True`, the part is always incremented when the version is bumped, regardless of the target part.


## calver_format

::: field-list
    required
    : No
    
    default
    : empty
    
    type
    : string

The `calver_format` is a string that specifies the format of the version part. It is used to determine the next value when bumping the version. The format is a string that uses the placeholders defined in the [CalVer reference](../calver_reference.md#calendar-versioning-codes).

## Examples

=== "TOML"

    ```toml
    [tool.bumpversion.parts.release]
    values = [
        "alpha",
        "beta",
        "gamma"
    ]
    optional_value = "gamma"
    ```

=== "CFG"

    ```ini
    [bumpversion:part:release]
    optional_value = gamma
    values =
        alpha
        beta
        gamma
    ```
