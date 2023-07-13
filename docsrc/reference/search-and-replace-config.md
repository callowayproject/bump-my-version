# Searching and replace configuration

Bump-my-version uses [template strings](https://docs.python.org/3/library/string.html#format-string-syntax) to search the configured files for the old or current version and replace the text with the new version.

You can configure the search or replace templates globally and within each `tool.bumpversion.files` entry in your configuration.

The default search template is `{current_version}` to find the version string within the file and replace it with `{new_version}`.

The search and replace templates can be multiple lines, like so:

```toml
[tool.bumpversion]
current_version = "1.2.3"

[[tool.bumpversion.files]]
filename = "config.ini"
search = "[myproject]\nversion={current_version}"
replace = "[myproject]\nversion={new_version}"
```

Alternatively, using [TOML's multiline strings](https://toml.io/en/v1.0.0#string):

```toml
[tool.bumpversion]
current_version = "1.2.3"

[[tool.bumpversion.files]]
filename = "config.ini"
search = """
[myproject]
version={current_version}"""

replace = """
[myproject]
version={new_version}"""
```
