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

`.toml` files are recommended. We will likely drop support for `ini`-style formats in the future. You should add your configuration file to your source code management system.

By using a configuration file, you no longer need to specify those options on the command line. The configuration file also allows greater flexibility in specifying how files are modified.

<!--nav-->
## Configuration sections

- [Global](global.md)
- [Version Component](version-component.md)
- [File](file.md)
