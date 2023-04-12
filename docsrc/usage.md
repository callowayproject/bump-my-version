# Usage

```{admonition} NOTE

Throughout this document, you can use `bumpversion` or `bump-my-version` interchangeably.
```

There are two modes of operation: On the command line for single-file operation
and using a configuration file (`pyproject.toml`) for more complex multi-file operations.

```console
bump-my-version [OPTIONS] VERSION_PART [FILES]...
```

## `VERSION_PART`

_**required**_

The part of the version to increase, e.g. `minor`.

Valid values include those given in the `--serialize` / `--parse` option.

Example bumping 0.5.1 to 0.6.0:

```console
bump-my-version --current-version 0.5.1 minor src/VERSION
```


## `FILES`

_**[optional]**_<br />
**default**: `None`

The additional file(s) to modify.

This file is added to the list of files specified in the configuration file. If you want to rewrite only files
specified on the command line, use `--no-configured-files`.

Example bumping version 1.1.9 to 2.0.0 in the `setup.py` file:

```console
bump-my-version --current-version 1.1.9 major setup.py
```

Example bumping version 1.1.9 to 2.0.0 in _only_ the `setup.py` file:

```console
bump-my-version --current-version 1.1.9 --no-configured-files major setup.py
```
