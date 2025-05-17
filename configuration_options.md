---
title: Configuration Options
---

# Configuration Options

Bump My Version offers a flexible configuration system that allows you to customize its behavior to suit your project's needs. This guide will walk you through the available configuration options, how to set them up, and provide examples for common scenarios.

## Configuration File

Bump My Version uses a configuration file to define its behavior. By default, it looks for a `pyproject.toml` file in your project root. You can also specify a custom configuration file using the `--config-file` command-line option.

### Configuration File Format

The configuration should be placed under the `[tool.bumpversion]` section in your `pyproject.toml` file. Here's an example of a basic configuration:

```toml
[tool.bumpversion]
current_version = "1.0.0"
commit = true
tag = true
```

## Available Configuration Options

Here's a comprehensive list of configuration options available in Bump My Version:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `current_version` | string | None | The current version of your project |
| `parse` | string | `"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)"` | Regular expression to parse the version string |
| `serialize` | list of strings | `["{major}.{minor}.{patch}"]` | Format string(s) to serialize the version |
| `search` | string | `"{current_version}"` | Template to search for the current version |
| `replace` | string | `"{new_version}"` | Template to replace the current version |
| `regex` | boolean | `false` | Whether to treat search and replace as regular expressions |
| `ignore_missing_version` | boolean | `false` | Whether to ignore missing version in files |
| `ignore_missing_files` | boolean | `false` | Whether to ignore missing files |
| `tag` | boolean | `false` | Whether to create a git tag |
| `sign_tags` | boolean | `false` | Whether to sign git tags |
| `tag_name` | string | `"v{new_version}"` | Template for the git tag name |
| `tag_message` | string | `"Bump version: {current_version} → {new_version}"` | Template for the git tag message |
| `allow_dirty` | boolean | `false` | Whether to allow dirty git working directory |
| `commit` | boolean | `false` | Whether to commit changes |
| `message` | string | `"Bump version: {current_version} → {new_version}"` | Template for the commit message |
| `commit_args` | string | None | Additional arguments to pass to git commit |
| `files` | list of objects | `[]` | List of files to update |
| `parts` | object | `{}` | Version part configurations |
| `moveable_tags` | list of strings | `[]` | List of moveable tags |
| `setup_hooks` | list of strings | `[]` | Setup hooks to run before version bump |
| `pre_commit_hooks` | list of strings | `[]` | Hooks to run before commit |
| `post_commit_hooks` | list of strings | `[]` | Hooks to run after commit |

## Environment Variables

You can override configuration options using environment variables. The environment variables should be prefixed with `BUMPVERSION_` and use uppercase. For example:

```sh
export BUMPVERSION_CURRENT_VERSION="1.2.3"
export BUMPVERSION_COMMIT=true
```

## Command-line Options

Many configuration options can also be set or overridden via command-line options. For example:

```sh
bump-my-version bump --current-version 1.2.3 --commit
```

Command-line options take precedence over environment variables and configuration file settings.

## Examples

### Basic Configuration

```toml
[tool.bumpversion]
current_version = "1.0.0"
commit = true
tag = true
parse = "(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+)"
serialize = [
    "{major}.{minor}.{patch}"
]

[[tool.bumpversion.files]]
filename = "myproject/__init__.py"
```

### Custom Version Format

```toml
[tool.bumpversion]
current_version = "2021.1.15"
parse = "(?P<year>\\d+)\\.(?P<release>\\d+)\\.(?P<build>\\d+)"
serialize = [
    "{year}.{release}.{build}"
]

[tool.bumpversion.parts.year]
independent = true

[tool.bumpversion.parts.release]
independent = true

[tool.bumpversion.parts.build]
independent = true
```

### Multiple Files and Complex Replacements

```toml
[tool.bumpversion]
current_version = "1.2.3"
commit = true
tag = true

[[tool.bumpversion.files]]
filename = "setup.py"
search = "version='{current_version}'"
replace = "version='{new_version}'"

[[tool.bumpversion.files]]
filename = "docs/conf.py"
search = "release = '{current_version}'"
replace = "release = '{new_version}'"

[[tool.bumpversion.files]]
filename = "src/mypackage/__init__.py"
search = "__version__ = '{current_version}'"
replace = "__version__ = '{new_version}'"
```

### Using Glob Patterns

```toml
[tool.bumpversion]
current_version = "0.1.0"

[[tool.bumpversion.files]]
glob = "**/*.py"
search = "__version__ = '{current_version}'"
replace = "__version__ = '{new_version}'"
```

Remember to adjust these configurations to match your project's specific needs. The flexibility of Bump My Version allows you to create a versioning strategy that works best for your development workflow.