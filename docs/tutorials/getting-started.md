# Getting Started

## Installation

To install Bump My Version as an independent tool, use [uv](https://docs.astral.sh/uv/getting-started/installation/) to install it on your system.

```console
uv tool install bump-my-version
```

## Create a default configuration

The default configuration uses a simplified version of [semantic versioning](https://semver.org/).

!!! Note

    Python projects can use `pyproject.toml` as the `--destination` of the sample config.

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
push_tag = false
sign_tags = false
tag_name = "v{new_version}"
tag_message = "Bump version: {current_version} → {new_version}"
allow_dirty = false
commit = false
message = "Bump version: {current_version} → {new_version}"
commit_args = ""
```

## Visualize the versioning path

You can see the potential versioning paths with the `show-bump` subcommand. This visualization will help debug any versioning logic you implement.

```console title="Showing the potential versioning path"
$ bump-my-version show-bump
0.1.0 ── bump ─┬─ major ─ 1.0.0
               ├─ minor ─ 0.2.0
               ╰─ patch ─ 0.1.1
```

You can also pass in a specific version to see how bumping that version would work.

```console title="Showing the potential versioning path from a specific version"
$ bump-my-version show-bump 1.2.3
1.2.3 ── bump ─┬─ major ─ 2.0.0
               ├─ minor ─ 1.3.0
               ╰─ patch ─ 1.2.4
```

## Get the new version in a script

If you want to get the new version within a script, you can use the [`show`](../../reference/cli/#bump-my-version-show) method.

```console title="Extract the new version"
$ bump-my-version show current_version
1.2.3
$ bump-my-version show --increment minor new_version
1.3.3
```

## Configure a file to modify when bumping

Let's say your version is stored in a file named `VERSION`. Every time you bump your version, that file needs to change.

Create the `VERSION` file with the current version `0.1.0`:

```console title="Create a VERSION file"
$ echo "0.1.0" >> VERSION
```

Add the following to the `.bumpversion.toml` file.

```toml title=".bumpversion.toml"
[[tool.bumpversion.files]]
filename = "VERSION"
```

Now bump-my-version will look in the `VERSION` file for the current version in that file and replace it with the new version on each `bump-my-version bump` command.

## Seeing what would happen with dry-run

You will increment the version using the `bump` subcommand. You "bump" a specific segment of the version. These segments are defined in the `parse` configuration. In this configuration (`(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+)`) the segments are `major`, `minor`, `patch`.

The `--dry-run` option will explain all the steps it performs without permanent changes. Use the `-vv` option to get the full description for debugging later.

!!! Note

    If you are in a Git or Mercurial repository, you may see additional messages.

```ansi-shell-session title="Incrementing the minor segment"
$ bump-my-version bump minor --dry-run -vv
{% include-markdown "../assets/getting-started-dry-run.ansi" comments=false %}
```
