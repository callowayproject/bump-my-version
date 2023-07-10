# Searching and replace configuration

Bump-my-version uses [template strings](https://docs.python.org/3/library/string.html#format-string-syntax) to search the configured files for the old or current version and replace the text with the new version.

You can configure the search or replace templates globally and within each `tool.bumpversion.files` entry in your configuration.

The default search template is `{current_version}` to find the version string within the file and replace it with `{new_version}`.

The search and replace templates can be multiple lines, like so:

```toml
[tool.bumpversion]
current_version = "1.2.3"

[[tool.bumpversion.files]]
filename = "config.ini"
search = "[myproject]\nversion={current_version}"
replace = "[myproject]\nversion={new_version}"
```

Alternatively, using [TOML's multiline strings](https://toml.io/en/v1.0.0#string):

```toml
[tool.bumpversion]
current_version = "1.2.3"

[[tool.bumpversion.files]]
filename = "config.ini"
search = """
[myproject]
version={current_version}"""

replace = """
[myproject]
version={new_version}"""
```

## Avoiding incorrect replacements

In files that have multiple version strings, bump-my-version may find the wrong string and replace it. Given this `requirements.txt` for `MyProject`:

```text
Django>=1.5.6,<1.6
MyProject==1.5.6
```

The default search and replace templates will replace the wrong text. Instead of changing `MyProject`'s version from `1.5.6` to `1.6.0`, it changes `Django`'s version:

```text
Django>=1.6.0,<1.6
MyProject==1.5.6
```

Providing search and replace templates for the `requirements.txt` file will avoid this.

This `.bumpversion.toml` will ensure only the line containing `MyProject` will be changed:

```toml
[tool.bumpversion]
current_version = "1.5.6"

[[tool.bumpversion.files]]
filename = "requirements.txt"
search = "MyProject=={current_version}"
replace = "MyProject=={new_version}"
```



If the string to be replaced includes literal quotes, the search and replace patterns must include them to match. Given the file `version.sh`:

    MY_VERSION="1.2.3"

Then the following search and replace patterns (including quotes) would be required:

```toml
[[tool.bumpversion.files]]
filename = "version.sh"
search = "MY_VERSION=\"{current_version}\""
replace = "MY_VERSION=\"{new_version}\""
```

## Custom version formats in different files

You can use file configurations to replace the version in multiple files, even if each file has the version formatted differently.

In a module-aware Go project, when you create a major version of your module beyond `v1`, your module name must include the major version number (e.g., `github.com/myorg/myproject/v2`). However, you also have the full version in a YAML file named `release-channels.yaml`.

`go.mod` file:

```go
module github.com/myorg/myproject/v2

go 1.12

require (
    ...
)
```

`release-channels.yaml` file:

```yaml
stable: "v2.21.4"
```

You can use bump-my-version to maintain the major version number within the `go.mod` file by using the `parse` and `serialize` options, as in this example:

 `.bumpversion.toml` file:

```toml
[tool.bumpversion]
current_version = "2.21.4"

[[tool.bumpversion.files]]
filename = "go.mod"
parse = "(?P<major>\\d+)"
serialize = "{major}"
search = "module github.com/myorg/myproject/v{current_version}"
replace = "module github.com/myorg/myproject/v{new_version}"

[[tool.bumpversion.files]]
filename = "release-channels.yaml"
```

While all the version bumps are `minor` or `patch`, the `go.mod` file doesn't change, while the `release-channels.yaml` file will. As soon as you do a `major` version bump, the `go.mod` file now contains this module directive:

```go
module github.com/myorg/myproject/v3
```

## Multiple replacements within the same file

To make several replacements in the same file, you must configure multiple `[[tool.bumpversion.files]]` sections for the same file with different configuration options.

In this example, the changelog is generated before the version bump. It uses `Unreleased` as the heading and includes a link to GitHub to compare this version (`HEAD`) with the previous version.

To change `Unreleased ` to the current version, we have an entry with `search` set to `Unreleased`.  The default `replace` value is `{new_version}`, so changing it is unnecessary.

To change the link, another entry has its `search` set to `{current_version}...HEAD` and the `replace` set to `{current_version}...{new_version}`.

```toml
[[tool.bumpversion.files]]
filename = "CHANGELOG.md"
search = "Unreleased"

[[tool.bumpversion.files]]
filename = "CHANGELOG.md"
search = "{current_version}...HEAD"
replace = "{current_version}...{new_version}"
```
