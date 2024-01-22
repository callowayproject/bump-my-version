# Usage

```{admonition} NOTE

You can use `bumpversion` or `bump-my-version` throughout this document  interchangeably.
```
There are two modes of operation: On the command line for single-file operation and using a configuration file (`pyproject.toml` or `.bumpversion.toml`) for more complex multi-file processes. We recommend using a configuration file for all but the simplest of projects.

```{admonition} WARNING

The invocation of `bump-my-version` changed in version 0.6.0. It splits functionality into sub-commands. It remains backward-compatible with previous versions. Previous usage is discouraged and may be removed in a 1.0 release.
```
## Incrementing a version

```console
bump-my-version bump [OPTIONS] [ARGS]...
```

The `bump` sub-command triggers a version increment. The [complete list of options](reference/cli.rst#bumpversion-bump) is available. The `ARGS` may contain a `VERSION_PART` or `FILES`


### `VERSION_PART`

_**[optional]**_

The part of the version to increase, e.g., `minor`.

Valid values include those given in the [`--serialize`](reference/configuration.md#serialize) / [`--parse`](reference/configuration.md#parse) option.

For example, if the current version is `0.5.1` and you want to bump it to `0.6.0`:

```console
bump-my-version bump minor
```


### `FILES`

_**[optional]**_<br />
**default**: `None`

The additional file(s) to modify.

This file is added to the list of files specified in the configuration file. If you want to rewrite only files specified on the command line, use `--no-configured-files`.

For example, if the current version is `1.1.9` and you want to bump the version to `2.0.0` and also change the version in the `_version.txt` file:

```console
bump-my-version bump major _version.txt
```

If you want to bump the current version of `1.1.9` to `2.0.0` and _only_ change the `_version.txt` file:

```console
bump-my-version bump --no-configured-files major _version.txt
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

## Searching and replacing without bumping

More complex workflows may require you to change one or more files without changing the `current_version` in the configuration file.

The `replace` sub-command works identically to the `bump` sub-command except for the following:

- It will not commit or tag any changes
- It will not increment the version
- It will not change the configuration file

```{admonition} NOTE

If you do not include the `--new-version` option, the `new_version` context variable will be `None`.
```

One way of providing the `--new-version` option is to use the `bump-my-version show` subcommand with an environment variable:

```console
$ export BUMPVERSION_NEW_VERSION=$(bump-my-version show new_version --increment <versionpart>)
$ bump-my-version replace
```
