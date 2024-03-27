# Configuration

Bump My Version looks in three places for configuration information (in order of precedence):

1. command line
2. configuration file
3. environment variables


## Configuration files

Bump My Version looks in four places for the configuration file to parse (in order of precedence):

1. `--config-file <FILE>` _(command line argument)_
2. `BUMPVERSION_CONFIG_FILE=file` _(environment variable)_
3. `.bumpversion.cfg` _(legacy)_
4. `.bumpversion.toml`
5. `setup.cfg` _(legacy)_
6. `pyproject.toml`

`.toml` files are recommended. We will likely drop support for `ini`-style formats in the future. You should add your configuration file to your source code management system.

By using a configuration file, you no longer need to specify those options on the command line. The configuration file also allows greater flexibility in specifying how files are modified.


## Global Configuration

The general configuration is grouped in a `[tool.bumpversion]` or  `[bumpversion]` section, depending on if it is a TOML or INI file respectfully.

### allow_dirty

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


Bump-my-version's default behavior is to abort if the working directory has uncommitted changes. This is to protect you from releasing unversioned files and/or overwriting unsaved changes.

### commit

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

If you have pre-commit hooks, you might also want to add an option to [`commit_args`](configuration.md#commit-args) to disable your pre-commit hooks. For Git use `--no-verify` and use `--config hooks.pre-commit=` for Mercurial.

### commit_args

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

Extra arguments to pass to commit command. This is only used when the [`commit`](configuration.md#commit) option is set to `True`.

If you have pre-commit hooks, you might also want to add an option to disable your pre-commit hooks. For Git use `--no-verify` and use `--config hooks.pre-commit=` for Mercurial.

### current_version

::: field-list

    required
    : **Yes**
    
    default
    : `""`
    
    type
    : string
    
    command line option
    : `--current-version`
    
    environment var
    : `BUMPVERSION_CURRENT_VERSION`

The current version of the software package before bumping. A value for this is required.

### ignore_missing_files

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

### ignore_missing_version

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

### message

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

The commit message template to use when creating a commit. This is only used when the [`commit`](configuration.md#commit) option is set to `True`.

This string is templated using the [Python Format String Syntax](https://docs.python.org/3/library/string.html#format-string-syntax). The [formatting context reference](formatting-context.md) describes the available variables.

### parse

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

This is the default regular expression (using [Python regular expression syntax](https://docs.python.org/3/library/re.html#regular-expression-syntax)) for finding and parsing the version string into its components. Individual part or file configurations may override this.

The regular expression must be able to parse all strings produced by the configured [`serialize`](configuration.md#serialize) value. Named matching groups ("`(?P<name>...)`") indicate the version part the matched value belongs to.

### regex

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

### replace

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

### search

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

This is the template string how to search for the string to be replaced in the file. Individual file configurations may override this. This can span multiple lines, and is templated using [Python Format String Syntax](https://docs.python.org/3/library/string.html#format-string-syntax). The [formatting context reference](formatting-context.md) describes the available variables.

This is useful if there is the remotest possibility that the current version number might be present multiple times in the file and you mean to only bump one of the occurrences. 

### serialize

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

Each string is templated using the [Python Format String Syntax](https://docs.python.org/3/library/string.html#format-string-syntax). The [formatting context reference](formatting-context.md) describes the available variables.

### sign_tags

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

If `True`, sign the created tag, when [`tag`](configuration.md#tag) is `True`.

### tag

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

If `True`, create a tag after committing the changes. The tag is named using the [`tag_name`](configuration.md#tag-name) option. 

If you are using `git`, don't forget to `git-push` with the `--tags` flag when you are done.

### tag_message

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

The tag message template to use when creating a tag, when [`tag`](configuration.md#tag) is `True`

This string is templated using the [Python Format String Syntax](https://docs.python.org/3/library/string.html#format-string-syntax). The [formatting context reference](formatting-context.md) describes the available variables.

Bump My Version creates an *annotated* tag in Git by default. To disable this and create a *lightweight* tag, you must explicitly set an empty `tag_message` value.

### tag_name

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

The name template used to render the tag, when [`tag`](configuration.md#tag) is `True`.

This string is templated using the [Python Format String Syntax](https://docs.python.org/3/library/string.html#format-string-syntax). The [formatting context reference](formatting-context.md) describes the available variables.

### Examples

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

## Version part-specific configuration

Version part configuration is grouped in a `[tool.bumpversion.parts.<partname>]` or  `[bumpversion:part:<partname>]` section, depending on if it is a TOML or INI file, respectfully.

You only need to configure version parts if they deviate from the default, and then you only need to specify the overridden options.

### values

::: field-list
    required
    : No
    
    default
    : numeric (i.e. `0`, `1`, `2`, …)
    
    type
    : array of strings

An explicit list of all values to iterate through when bumping this part. An empty array is treated as indicating `numeric` values.

### optional_value

::: field-list
    required
    : No
    
    default
    : The first entry in `values`, `0` when using numeric values
    
    type
    : string

When the version part matches this value it is considered optional when serializing the final version string.

!!! note

    Numeric values are still treated as strings internally, so when specifying an optional value, you must use a string.


### first_value

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


### independent

::: field-list
    required
    : No
    
    default
    : `False`
    
    type
    : boolean

When this value is set to `True`, the part is not reset when other parts are incremented. Its incrementation is
independent of the other parts. It is useful when you have a build number in your version that is incremented independently of the actual version.

### always_increment

::: field-list
    required
    : No

    default
    : `False` (`True` if `calver_format` is set)

    type
    : boolean

When this value is set to `True`, the part is always incremented when the version is bumped, regardless of the target part.


### calver_format

::: field-list
    required
    : No
    
    default
    : empty
    
    type
    : string

The `calver_format` is a string that specifies the format of the version part. It is used to determine the next value when bumping the version. The format is a string that uses the placeholders defined in the [CalVer reference](calver_reference.md#calver-format).

### Examples

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


## File-specific configuration

This section configures which files Bump My Version should update by replacing their current version with the newly bumped version.

### filename

::: field-list
    required
    : **Yes‡**
    
    default
    : empty
    
    type
    : string

The name of the file to modify.

!!! note

    ‡ This is only used with TOML configuration, and is only required if [`glob`](#glob) is _not_ specified. INI-style configuration files specify the file name as part of the grouping.


### glob

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


### parse

::: field-list

    required
    : No
    
    default
    : the value configured in the global `parse` field
    
    type
    : string

This is an override to the default pattern to parse the version number from this file.

### serialize

::: field-list

    required
    : No
    
    default
    : the value configured in the global `serialize` field
    
    type
    : an array of strings

This is an override to the default templates to serialize the new version number in this file.

### search

::: field-list

    required
    : No
    
    default
    : the value configured in the global `search` field
    
    type
    : string

This is an override to the default template string how to search for the string to be replaced in the file.

### regex

::: field-list

    required
    : No
    
    default
    : the valued configured in the global `regex` field
    
    type
    : boolean

If `True`, treat the `search` parameter as a regular expression.

### replace

::: field-list

    required
    : No
    
    default
    : the value configured in the global `replace` field
    
    type
    : string

This is an override to the template to create the string that will replace the current version number in the file.

### ignore_missing_version

::: field-list

    required
    : No
    
    default
    : The value configured in the global `ignore_missing_version` field
    
    type
    : boolean

If `True`, don't fail if the version string to be replaced is not found in the file.

### ignore_missing_file

::: field-list

    required
    : No
    
    default
    : The value configured in the global `ignore_missing_file` field
    
    type
    : boolean

if `True`, don't fail if the configured file is missing.

### Examples

=== "TOML"

    TOML allows us to specify the files using an [array of tables.](https://toml.io/en/v1.0.0#array-of-tables) TOML configuration files add two configuration fields to each file configuration: `filename` and `glob`. These fields are mutually exclusive: if you specify a value for both, only the `glob` value is used.
    
    For example, to change `coolapp/__init__.py` with the defaults, and alter `CHANGELOG.md` in twice:
    
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
    
    
    For example, to change `coolapp/__init__.py` with the defaults, and alter `CHANGELOG.md` in twice:
    
    ```ini
    [bumpversion:file:coolapp/__init__.py]
    
    [bumpversion:file(version heading):CHANGELOG.md]
    search = Unreleased
    
    [bumpversion:file(previous version):CHANGELOG.md]
    search = {current_version}...HEAD
    replace = {current_version}...{new_version}
    ```
