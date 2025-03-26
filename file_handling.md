---
title: File Handling in Bump My Version
---

# File Handling in Bump My Version

Bump My Version provides powerful and flexible file handling capabilities to update version numbers across your project files. This document explains how Bump My Version handles file modifications during the version bumping process, including configuration options for file selection, search and replace patterns, and handling of different file types.

## Configuring Files to Update

Bump My Version allows you to specify which files should be updated during the version bumping process. You can configure this in your `pyproject.toml` file or through command-line options.

### Using `pyproject.toml`

To specify files in your `pyproject.toml`, use the `files` key under the `[tool.bumpversion]` section:

```toml
[tool.bumpversion]
current_version = "0.1.0"
files = [
    "setup.py",
    "src/mypackage/__init__.py",
    "docs/conf.py"
]
```

### Using Command-line Options

You can also specify files using the `--files` option when running Bump My Version:

```bash
bumpversion --files setup.py src/mypackage/__init__.py docs/conf.py minor
```

## File Change Configuration

Each file can have its own configuration for how version numbers should be updated. This is done using the `FileChange` model, which includes the following key properties:

- `parse`: Regular expression pattern to parse the current version
- `serialize`: Format string to serialize the new version
- `search`: Pattern to search for in the file
- `replace`: Pattern to replace the found version with
- `regex`: Boolean flag to indicate if the search pattern is a regular expression
- `ignore_missing_version`: Boolean flag to ignore if the version is not found in the file
- `ignore_missing_file`: Boolean flag to ignore if the file is not found

### Example Configuration

```toml
[tool.bumpversion]
current_version = "0.1.0"

[[tool.bumpversion.files]]
filename = "setup.py"
search = "version='{current_version}'"
replace = "version='{new_version}'"
```

## Search and Replace Patterns

Bump My Version uses search and replace patterns to update version numbers in files. These patterns can be simple strings or regular expressions.

### Simple String Patterns

By default, Bump My Version uses simple string patterns:

```toml
search = "version = '{current_version}'"
replace = "version = '{new_version}'"
```

### Regular Expression Patterns

For more complex scenarios, you can use regular expressions by setting `regex = true`:

```toml
regex = true
search = "version\\s*=\\s*['\"](?P<version>[^'\"]+)['\"]"
replace = "version = '{new_version}'"
```

## Handling Different File Types

Bump My Version can handle various file types, including plain text files and structured data files like TOML.

### Plain Text Files

For plain text files, Bump My Version performs a simple search and replace operation based on the configured patterns.

### TOML Files

For TOML files, Bump My Version uses the `tomlkit` library to parse and modify the file contents. This allows for updating nested keys within the TOML structure.

To update a specific key in a TOML file, use the `key_path` configuration:

```toml
[[tool.bumpversion.files]]
filename = "pyproject.toml"
key_path = "tool.poetry.version"
```

## Glob Patterns

You can use glob patterns to match multiple files with a single configuration:

```toml
[[tool.bumpversion.files]]
glob = "src/**/__init__.py"
search = "__version__ = '{current_version}'"
replace = "__version__ = '{new_version}'"
```

## File Update Process

1. Bump My Version resolves the list of files to modify based on the configuration and any glob patterns.
2. For each file, it applies the search and replace patterns to update the version number.
3. If `dry_run` is not enabled, it writes the changes back to the files.
4. Logging is performed to show the changes made to each file.

## Conclusion

Bump My Version's file handling capabilities provide a flexible and powerful way to manage version numbers across your project files. By understanding and utilizing these features, you can automate your version bumping process effectively and consistently.

For more detailed information on configuration options and advanced usage, please refer to the main configuration documentation.