# Usage

```{admonition} NOTE

Throughout this document, you can use `bumpversion` or `bump-my-version` interchangeably.
```

There are two modes of operation: On the command line for single-file operation and using a configuration file (`pyproject.toml` or `.bumpversion.toml`) for more complex multi-file processes.

```{admonition} WARNING

The invocation of `bump-my-version` changed in version 0.6.0. It split functionality into sub-commands. It remains backward-compatible with previous versions. Previous usage is discouraged and may be removed in a 1.0 release.
```
## Incrementing a version

```console
bump-my-version bump [OPTIONS] [ARGS]...
```

The `bump` sub-command triggers a version increment. The [complete list of options](cli.rst#bumpversion-bump) is available. The `ARGS` may contain a `VERSION_PART` or `FILES`


### `VERSION_PART`

_**[optional]**_

The part of the version to increase, e.g., `minor`.

Valid values include those given in the [`--serialize`](configuration.md#serialize) / [`--parse`](configuration.md#parse) option.

Example bumping 0.5.1 to 0.6.0:

```console
bump-my-version bump --current-version 0.5.1 minor src/VERSION
```


### `FILES`

_**[optional]**_<br />
**default**: `None`

The additional file(s) to modify.

This file is added to the list of files specified in the configuration file. If you want to rewrite only files specified on the command line, use `--no-configured-files`.

Example bumping version 1.1.9 to 2.0.0 in the `setup.py` file:

```console
bump-my-version bump --current-version 1.1.9 major setup.py
```

Example bumping version 1.1.9 to 2.0.0 in _only_ the `setup.py` file:

```console
bump-my-version bump --current-version 1.1.9 --no-configured-files major setup.py
```

## Showing configuration information

```console
bump-my-version show [OPTIONS] [ARGS]
```

The `show` subcommand allows you to output the entire or parts of the configuration to the console. The default invocation will output in the default format. The default format changes if one or more than one item is requested. If more than one item is asked for, it outputs the result of Python's `pprint` function. If only one thing is asked for, it outputs that value only.

```console
$ bump-my-version show current_version
1.0.0
$ bump-my-version show current_version commit
{'current_version': '1.0.0', 'commit': False}
```

You can use the `--increment` option to enable a `new_version` key.

```console
$ bump-my-version show --increment minor current_version new_version
{'current_version': '1.0.0', 'new_version': '1.1.0'}
```

You can also specify the output to be in JSON or YAML format:

```console
$ bump-my-version show --format yaml current_version
current_version: "1.0.0"
$ bump-my-version show --format yaml current_version commit
current_version: "1.0.0"
commit: false
$ bump-my-version show --format json current_version
{
  "current_version": "1.0.0"
}
$ bump-my-version show --format json current_version commit
{
  "current_version": "1.0.0",
  "commit": false,
}
```
