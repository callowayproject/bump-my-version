---
title: Command Line Interface
---

# Bump My Version Command Line Interface

Bump My Version is a powerful tool for managing version numbers in your Python projects. This guide provides a comprehensive overview of the command-line interface, explaining all available commands, their options, and usage examples for common scenarios.

## Table of Contents

1. [Installation](#installation)
2. [Basic Usage](#basic-usage)
3. [Commands](#commands)
   - [bump](#bump)
   - [show](#show)
   - [replace](#replace)
   - [sample-config](#sample-config)
   - [show-bump](#show-bump)
4. [Configuration](#configuration)
5. [Examples](#examples)

## Installation

To install Bump My Version, use pip:

```
pip install bump-my-version
```

## Basic Usage

The basic syntax for using Bump My Version is:

```
bump-my-version [OPTIONS] COMMAND [ARGS]...
```

To get help on any command, use the `-h` or `--help` option:

```
bump-my-version -h
bump-my-version COMMAND -h
```

## Commands

### bump

The `bump` command is used to change the version number in your project files.

```
bump-my-version bump [OPTIONS] [ARGS]...
```

#### Options

- `--config-file`: Specify a custom config file.
- `--current-version`: The current version to be updated.
- `--new-version`: The new version to update to.
- `--dry-run`: Don't write any files, just simulate the bump.
- `--verbose`: Increase verbosity of output.
- `--allow-dirty`: Allow bumping versions in a dirty working directory.
- `--commit`: Commit to version control.
- `--tag`: Create a tag in version control.
- `--sign-tags`: Sign tags if created.
- `--tag-name`: Specify the tag name.
- `--tag-message`: Specify the tag message.
- `--message`: Specify the commit message.

#### Usage

```
bump-my-version bump minor
bump-my-version bump --new-version 1.2.3
```

### show

The `show` command displays the current configuration information.

```
bump-my-version show [OPTIONS] [ARGS]...
```

#### Options

- `--config-file`: Specify a custom config file.
- `--format`: Specify the output format (default, yaml, or json).
- `--increment`: Increment a version component and add to the configuration.
- `--current-version`: Specify the current version.

#### Usage

```
bump-my-version show
bump-my-version show current_version
bump-my-version show --format json
```

### replace

The `replace` command replaces version strings in specified files.

```
bump-my-version replace [OPTIONS] [FILES]...
```

#### Options

- `--config-file`: Specify a custom config file.
- `--current-version`: The current version to be updated.
- `--new-version`: The new version to update to.
- `--dry-run`: Don't write any files, just simulate the replacement.
- `--verbose`: Increase verbosity of output.
- `--allow-dirty`: Allow replacing versions in a dirty working directory.

#### Usage

```
bump-my-version replace --new-version 1.2.3 file1.py file2.txt
bump-my-version replace --dry-run --new-version 2.0.0
```

### sample-config

The `sample-config` command generates a sample configuration file.

```
bump-my-version sample-config [OPTIONS]
```

#### Options

- `--prompt/--no-prompt`: Ask the user questions about the configuration.
- `--destination`: Where to write the sample configuration (stdout, .bumpversion.toml, or pyproject.toml).

#### Usage

```
bump-my-version sample-config
bump-my-version sample-config --no-prompt --destination .bumpversion.toml
```

### show-bump

The `show-bump` command visualizes possible version bumps.

```
bump-my-version show-bump [OPTIONS] [VERSION]
```

#### Options

- `--config-file`: Specify a custom config file.
- `--ascii`: Use ASCII characters only in the output.
- `--verbose`: Increase verbosity of output.

#### Usage

```
bump-my-version show-bump
bump-my-version show-bump 1.2.3 --ascii
```

## Configuration

Bump My Version can be configured using a configuration file. By default, it looks for `.bumpversion.toml` or `pyproject.toml` in the current directory or any parent directory.

You can specify a custom configuration file using the `--config-file` option with any command.

## Examples

1. Bump the minor version:

```
bump-my-version bump minor
```

2. Set a specific version:

```
bump-my-version bump --new-version 2.1.0
```

3. Show current configuration:

```
bump-my-version show
```

4. Replace version in specific files:

```
bump-my-version replace --new-version 1.3.0 setup.py README.md
```

5. Generate a sample configuration file:

```
bump-my-version sample-config --destination .bumpversion.toml
```

6. Visualize possible version bumps:

```
bump-my-version show-bump --ascii
```

For more detailed information on each command and its options, refer to the specific command documentation or use the `--help` option.