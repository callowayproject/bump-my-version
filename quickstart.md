---
title: Quickstart Guide
---

# Quickstart Guide

This guide will help you get started with Bump My Version quickly. You'll learn how to install the tool, create an initial configuration file, and perform basic version bumping operations.

## Installation

Bump My Version can be easily installed using [uv](https://docs.astral.sh/uv/getting-started/installation/), a fast Python package installer and resolver.

```console
uv tool install bump-my-version
```

## Creating a Configuration File

Before you can start using Bump My Version, you need to create a configuration file. The tool provides a convenient command to generate a sample configuration:

```console
bump-my-version sample-config
```

This command will prompt you with questions about your desired configuration. If you prefer to use default settings without prompts, you can use:

```console
bump-my-version sample-config --no-prompt
```

By default, this will print the configuration to stdout. To save it directly to a file, use the `--destination` option:

```console
bump-my-version sample-config --destination .bumpversion.toml
```

## Basic Usage

Once you have your configuration file set up, you can start using Bump My Version to manage your project's versioning.

### Viewing the Current Version

To see the current version of your project:

```console
bump-my-version show current_version
```

### Bumping the Version

To increment a specific part of the version (e.g., major, minor, or patch):

```console
bump-my-version bump patch
```

This command will increment the patch version, update all configured files, and (if configured) create a commit and tag in your version control system.

### Dry Run

If you want to see what changes would be made without actually making them, use the `--dry-run` option:

```console
bump-my-version bump minor --dry-run
```

### Specifying Files

By default, Bump My Version will update all files specified in your configuration. If you want to update only specific files, you can list them after the version part:

```console
bump-my-version bump patch setup.py README.md
```

## Visualizing Version Bumps

To see the potential version bumps from your current version:

```console
bump-my-version show-bump
```

This will display a tree-like structure showing the possible version increments.

## Next Steps

Now that you're familiar with the basics of Bump My Version, you can explore more advanced features such as:

- Customizing version parsing and serialization
- Configuring commit messages and tag formats
- Setting up pre-release and build number support

For more detailed information on these topics and other features, refer to the full documentation.