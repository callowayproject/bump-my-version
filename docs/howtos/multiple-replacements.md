# Multiple replacements within the same file

To make several replacements in the same file, you must configure multiple `[[tool.bumpversion.files]]` sections for the same file with different configuration options.

In this example, the changelog is generated before the version bump. It uses `Unreleased` as the heading and includes a link to GitHub to compare this version (`HEAD`) with the previous version.

To change `Unreleased ` to the current version, we have an entry with `search` set to `Unreleased`.  The default `replace` value is `{new_version}`, so changing it is unnecessary.

To change the link, another entry has its `search` set to `{current_version}...HEAD` and the `replace` set to `{current_version}...{new_version}`.

```toml
[[tool.bumpversion.files]]
filename = "CHANGELOG.md"
search = "Unreleased"

[[tool.bumpversion.files]]
filename = "CHANGELOG.md"
search = "{current_version}...HEAD"
replace = "{current_version}...{new_version}"
```
