# How to check the version before a release

`bump-my-version check` verifies, without changing anything, that every configured file contains the current version. Each file is searched exactly as the next `bump` would search it, so a file that somebody forgot to bump, or bumped by hand to a different version, makes the check fail with a non-zero exit status.

```console
$ bump-my-version check
Version 1.2.3 is consistent across the configured files.
```

```console
$ bump-my-version check
Did not find '1.2.3' in file: 'CITATION.cff'
```

A file configuration whose `search` does not contain the version at all (like an `**unreleased**` changelog heading, which a bump may replace) is skipped, as it says nothing about the version.

The PEP 621 `project.version` in `pyproject.toml`, which `bump` keeps in sync with `current_version`, is checked too.

## Block a release in CI/CD

When the release is triggered by pushing a tag, pass the tag with `--release-tag`. The check then also fails unless the tag matches [`tag_name`](../reference/configuration/global.md#tag_name) rendered with the current version:

```yaml title=".github/workflows/release.yml"
on:
  push:
    tags: ["v*"]

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pipx run bump-my-version check --release-tag "$GITHUB_REF_NAME"
      # build and publish
```

## Tag a release whose files were bumped by hand

If you bump the files yourself, or with `bump-my-version bump --no-commit --no-tag` and then commit them together with other changes, run the check before tagging:

```bash
bump-my-version check && git tag "v$(bump-my-version show current_version)"
```

## Require more than the version

The check uses each file's own [`search`](../reference/configuration/file.md#search). A file configuration whose `replace` puts back what it found (`\g<0>`) is never changed by `bump`, but its pattern must still be present. For example, to require a dated changelog heading for the current version:

```toml title=".bumpversion.toml or other config file"
[[tool.bumpversion.files]]
filename = "CHANGELOG.md"
search = "^## {current_version} \\(\\d{{4}}-\\d{{2}}-\\d{{2}}\\)"
replace = "\\g<0>"
regex = true
```
