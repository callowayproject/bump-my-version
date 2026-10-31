---
title: Configuration
description: How to configure Bump My Version
icon:
date: 2024-08-11
comments: true
---

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

Items 3-6 are searched for in the current directory, then, when inside a git or mercurial repository, in each parent directory up to the repository root. The nearest directory containing a configuration file wins. Outside a repository, only the current directory is searched.

A `.toml` file counts as a configuration file when it is valid TOML and contains a `[tool.bumpversion]` table. A table that only holds `[[tool.bumpversion.files]]` is enough. Invalid TOML is skipped, not reported as an error. `.cfg` files must contain a `bumpversion` section.

If no file with Bump My Version configuration is found, the nearest `pyproject.toml` with a static `project.version` ([PEP 621](https://peps.python.org/pep-0621/)) is used instead, and that version becomes the current version. A `pyproject.toml` that lists `version` in `project.dynamic` is ignored.

`.toml` files are recommended. We will likely drop support for `ini`-style formats in the future. You should add your configuration file to your source code management system.

By using a configuration file, you no longer need to specify those options on the command line. The configuration file also allows greater flexibility in specifying how files are modified.

<!--nav-->
## Configuration sections

- [Global](global.md)
- [Version Component](version-component.md)
- [File](file.md)
