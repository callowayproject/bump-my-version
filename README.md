# Bump My Version

[![image](https://img.shields.io/pypi/v/bump-my-version.svg)](https://pypi.org/project/bump-my-version/)
[![image](https://img.shields.io/pypi/l/bump-my-version.svg)](https://pypi.org/project/bump-my-version/)
[![image](https://img.shields.io/pypi/pyversions/bump-my-version.svg)](https://pypi.org/project/bump-my-version/)
[![codecov](https://codecov.io/gh/callowayproject/bump-my-version/branch/master/graph/badge.svg?token=D1GSOtWEPU)](https://codecov.io/gh/callowayproject/bump-my-version)
[![GitHub Actions](https://github.com/callowayproject/bump-my-version/workflows/CI/badge.svg)](https://github.com/callowayproject/bump-my-version/actions)

> **NOTE**
>
> This is a maintained refactor of the [bump2version fork](https://github.com/c4urself/bump2version) of the excellent [bumpversion project](https://github.com/peritus/bumpversion). The main goals of this refactor were:
>
> - Add support for `pyproject.toml` configuration files.
> - Convert to [click](https://click.palletsprojects.com/en/8.1.x/) for and [rich](https://rich.readthedocs.io/en/stable/index.html) for the CLI interface
> - Add better configuration validation using [Pydantic](https://docs.pydantic.dev)
> - Make the code and tests easier to read and maintain


## Overview

Version-bump your software with a single command!

A small command line tool to simplify releasing software by updating all version strings in your source code by the correct increment and optionally commit and tag the changes.

* version formats are highly configurable
* works without any source code manager, but happily reads tag information from and writes
  commits and tags to Git and Mercurial if available
* just handles text files, so it's not specific to any programming language
* supports Python 3.8+ and PyPy3. Python 3.7 should work but isn't actively tested.

## Future Direction

- Make it easier to get the current version
- Switch having both the version part and files to change as arguments on the command line.
- Make the version part argument _truly_ optional when `--new-version` is specified
- Allow for multiple tags, including one that moves for having a `v2` that always points to the latest version of version 2. [For example](https://github.com/actions/toolkit/blob/master/docs/action-versioning.md#recommendations)
- Better UI with [Rich](https://rich.readthedocs.io/en/stable/index.html)

## Installation

You can download and install the latest version of this software from the Python package index (PyPI) as follows:

```console
pip install --upgrade bump-my-version
```

## Changelog

Please find the changelog here: [CHANGELOG.md](CHANGELOG.md)

## Usage for version incrementing

> **NOTE:** 
>
> Throughout this document, you can use `bumpversion` or `bump-my-version` interchangeably.

There are two modes of operation: On the command line for single-file operation and using a configuration file (`pyproject.toml` or `.bumpversion.toml`) for more complex multi-file operations.

> **WARNING:**
> 
> The invocation of `bump-my-version` changed in version 0.6.0. It split functionality into sub-commands. It remains backward-compatible with previous versions. Previous usage is discouraged and may be removed in a 1.0 release.

    bump-my-version bump [options] [part] [file]

### `part`

_**required**_

The part of the version to increase, e.g. `minor`.

Valid values include the named groups defined in the `parse` configuration.

Example bumping 0.5.1 to 0.6.0:

    bump-my-version bump --current-version 0.5.1 minor

### `file`

_**[optional]**_<br />
**default**: none

Additional files to modify.

These files are added to the list of files specified in your configuration file. If you want to rewrite only files specified on the command line, also use `--no-configured-files`.

Example bumping 1.1.9 to 2.0.0:

    bump-my-version bump --current-version 1.1.9 major setup.py

## Configuration file

`bump-my-version` looks in four places for the configuration file to parse (in order of precedence):

1. `--config-file <FILE>` _(command line argument)_
2. `BUMPVERSION_CONFIG_FILE=file` _(environment variable)_
3. `.bumpversion.cfg` _(legacy)_
4. `.bumpversion.toml`
5. `setup.cfg` _(legacy)_
6. `pyproject.toml`

`.toml` files are recommended due to their type handling. We will likely drop support for `ini`-style formats in the future due to issues with formatting and parsing. You should add your configuration file to your source code management system.

By using a configuration file, you no longer need to specify those options on the command line. The configuration file also allows greater flexibility in specifying how files are modified.

## Command-line Options

Most of the configuration values above can also be given as an option on the command line.
Additionally, the following options are available:

`--dry-run, -n`
Don't touch any files, just pretend. Best used with `--verbose`.

`--no-configured-files`
Will not update/check files specified in the configuration file.

Similar to dry-run, but will also avoid checking the files. Also useful when you want to update just one file with e.g., `bump-my-version --no-configured-files major my-file.txt`

`--verbose, -v`
Print useful information to stderr. If specified more than once, it will output more information.

`--list`
_DEPRECATED. Use `bump-my-version show` instead._ List machine-readable information to stdout for consumption by other programs.

Example output:

    current_version=0.0.18
    new_version=0.0.19

`-h, --help`
Print help and exit

## Using bumpversion in a script

If you need to use the version generated by bumpversion in a script, you can make use of the `show` subcommand.

Say, for example, that you are using git-flow to manage your project and want to automatically create a release. When you issue `git flow release start` you need to know the new version before applying the change.

The standard way to get it in a bash script is

    bump-my-version show new_version --increment <part>

where `part` is the part of the version number you are updating.

For example, if you are updating the minor number and looking for the new version number, this becomes:

```console
$ bump-my-version show new_version --increment minor
1.1.0
```

## Development & Contributing

Thank you, contributors! You can find a full list here: https://github.com/callowayproject/bump-my-version/graphs/contributors

See also our [CONTRIBUTING.md](CONTRIBUTING.md)

Development of this happens on GitHub, patches including tests, and documentation are very welcome, as well as bug reports! Please open an issue if this tool does not support every aspect of bumping versions in your development
workflow, as it is intended to be very versatile.

## License

bump-my-version is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
