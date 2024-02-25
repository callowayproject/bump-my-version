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

<!--start-->

## Overview

Bump My Version's purpose is to:

- Work as a part of an automated build system
- Manage project versioning through the project's development life cycle
    - Incrementing version numbers
    - serializing version numbers
    - parsing version numbers
- Modify project files as part of the project's development life cycle
- Work with the project's source control system
    - Committing changes
    - Tagging releases
    - Reading version numbers from tags

## Installation

You can download and install the latest version of this software from the Python package index (PyPI) as follows:

```console
pip install --upgrade bump-my-version
```

## Changelog

Please find the changelog here: [CHANGELOG.md](CHANGELOG.md)

## Semantic versioning example
<!--tutorial start-->

### Create a default configuration

The default configuration uses a simplified version of [semantic versioning](https://semver.org/).

```console title="Generating a default configuration"
$ bump-my-version sample-config --no-prompt --destination .bumpversion.toml
$ cat .bumpversion.toml
[tool.bumpversion]
current_version = "0.1.0"
parse = "(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+)"
serialize = ["{major}.{minor}.{patch}"]
search = "{current_version}"
replace = "{new_version}"
regex = false
ignore_missing_version = false
tag = false
sign_tags = false
tag_name = "v{new_version}"
tag_message = "Bump version: {current_version} → {new_version}"
allow_dirty = false
commit = false
message = "Bump version: {current_version} → {new_version}"
commit_args = ""
```

### Visualize the versioning path

You can see the potential versioning paths with the `show-bump` subcommand.

```console title="Showing the potential versioning path"
$ bump-my-version show-bump
0.1.0 ── bump ─┬─ major ─ 1.0.0
               ├─ minor ─ 0.2.0
               ╰─ patch ─ 0.1.1
$ bump-my-version show-bump 1.2.3
1.2.3 ── bump ─┬─ major ─ 2.0.0
               ├─ minor ─ 1.3.0
               ╰─ patch ─ 1.2.4
```

The default configuration only allows bumping the major, minor, or patch version. What if you wanted to support pre-release versions?

### Add support for pre-release versions

Alter the `parse` configuration to support pre-release versions. This `parse` option uses an extended (or verbose) regular expression to extract the version parts from the current version. 

```toml title="New parse configuration"
parse = """(?x)
    (?P<major>0|[1-9]\\d*)\\.
    (?P<minor>0|[1-9]\\d*)\\.
    (?P<patch>0|[1-9]\\d*)
    (?:
        -                             # dash seperator for pre-release section
        (?P<pre_l>[a-zA-Z-]+)         # pre-release label
        (?P<pre_n>0|[1-9]\\d*)        # pre-release version number
    )?                                # pre-release section is optional
"""
```

Alter the `serialize` configuration to support pre-release versions.

```toml title="New serialize configuration"
serialize = [
    "{major}.{minor}.{patch}-{pre_l}{pre_n}",
    "{major}.{minor}.{patch}",
]
```

Add a new configuration section for the `pre_l` part.

```toml title="New pre_l configuration"

[tool.bumpversion.parts.pre_l]
values = ["dev", "rc", "final"]
optional_value = "final"
```

### Visualize the new versioning path

Now when you run `bump-my-version show-bump`, you can see the new pre-release versioning path.

```console title="Showing the new versioning path"
$ bump-my-version show-bump
0.1.0 ── bump ─┬─ major ─ 1.0.0-dev0
               ├─ minor ─ 0.2.0-dev0
               ├─ patch ─ 0.1.1-dev0
               ├─ pre_l ─ invalid: The part has already the maximum value among ['dev', 'rc', 'final'] and cannot be bumped.
               ╰─ pre_n ─ 0.1.0-final1
```

The `pre_l` is not bump-able because it is already at the maximum value. The `pre_n` is bump-able because it is not at the maximum value.

If we run `bump-my-version show-bump 1.0.0-dev0`, we can see the new versioning path for a `dev` starting version.

```console title="Showing the new versioning path for a dev version"
$ bump-my-version show-bump 1.0.0-dev0
1.0.0-dev0 ── bump ─┬─ major ─ 2.0.0-dev0
                    ├─ minor ─ 1.1.0-dev0
                    ├─ patch ─ 1.0.1-dev0
                    ├─ pre_l ─ 1.0.0-rc0
                    ╰─ pre_n ─ 1.0.0-dev1
```

Finally, we can see the new versioning path for a `rc` starting version.

```console title="Showing the new versioning path for an rc version"
$ bump-my-version show-bump 1.0.0-rc0 
1.0.0-rc0 ── bump ─┬─ major ─ 2.0.0-dev0
                   ├─ minor ─ 1.1.0-dev0
                   ├─ patch ─ 1.0.1-dev0
                   ├─ pre_l ─ 1.0.0
                   ╰─ pre_n ─ 1.0.0-rc1
```

The full development and release path is:

- `1.0.0`
- `bump patch` → `1.0.1-dev0`
- `bump pre_n` → `1.0.1-dev1`
- `bump pre_l` → `1.0.1-rc0`
- `bump pre_n` → `1.0.1-rc1`
- `bump pre_l` → `1.0.1`

1. You must decide on the next version before you start developing.
2. Development versions increase using `bump-my-version bump pre_n`.
3. Switch from development to release candidate using `bump-my-version bump pre_l`.
4. Release candidates increase using `bump-my-version bump pre_n`.
5. Switch from the release candidate to the final release using `bump-my-version bump pre_l`.

### Automate the pre-release numbering

The `pre_n` or pre-release number is a number that increases with each pre-release. You can automate this my changing the serialization configuration.

```toml title="Serialize configuration with pre_n automation"
serialize = [
    "{major}.{minor}.{patch}-{pre_l}{distance_to_latest_tag}",
    "{major}.{minor}.{patch}",
]
```

The `distance_to_latest_tag` is a special value that is replaced with the number of commits since the last tag. This is a good value to use for the `pre_n` because it will always increase with each commit.

### Visualize the pre_n versioning path

Now when you run `bump-my-version show-bump`, you can see the new pre-release versioning path.

```console title="Showing the new versioning path with pre_n automation"

$ bump-my-version show-bump
0.1.0 ── bump ─┬─ major ─ 1.0.0-dev0
               ├─ minor ─ 0.2.0-dev0
               ├─ patch ─ 0.1.1-dev0
               ╰─ pre_l ─ invalid: The part has already the maximum value among ['dev', 'rc', 'final'] and cannot be bumped.
$ bump-my-version show-bump 1.0.0-dev0
1.0.0-dev0 ── bump ─┬─ major ─ 2.0.0-dev0
                    ├─ minor ─ 1.1.0-dev0
                    ├─ patch ─ 1.0.1-dev0
                    ╰─ pre_l ─ 1.0.0-rc0
$ bump-my-version show-bump 1.0.0-rc0 
1.0.0-rc0 ── bump ─┬─ major ─ 2.0.0-dev0
                   ├─ minor ─ 1.1.0-dev0
                   ├─ patch ─ 1.0.1-dev0
                   ╰─ pre_l ─ 1.0.0
 ```

The `pre_n` path is now missing because it is automated.

The full development and release path now is:

- `1.0.0`
- `bump patch` → `1.0.1-dev0`
- each commit will increase → `1.0.1-dev1`
- `bump pre_l` → `1.0.1-rc0`
- each commit will increase → `1.0.1-rc1`
- `bump pre_l` → `1.0.1`

1. You must decide on the next version before you start developing.
2. Development versions increase automatically with each commit.
3. Switch from development to release candidate using `bump-my-version bump pre_l`.
4. Release candidate versions increase automatically with each commit.
5. Switch from the release candidate to the final release using `bump-my-version bump pre_l`.

<!--tutorial end-->

## Development & Contributing

Thank you, contributors! You can find a full list here: https://github.com/callowayproject/bump-my-version/graphs/contributors

See also our [CONTRIBUTING.md](CONTRIBUTING.md)

Development of this happens on GitHub, patches including tests, and documentation are very welcome, as well as bug reports! Please open an issue if this tool does not support every aspect of bumping versions in your development
workflow, as it is intended to be very versatile.

## License

Bump My Version is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

<!--end-->
