# Search and replace configuration

Bump-my-version uses a combination of [template strings](https://docs.python.org/3/library/string.html#format-string-syntax) using a [formatting context](formatting-context.md) and regular expressions to search the configured files for the old or current version and replace the text with the new version.

## Using template strings

Both the search and replace templates are rendered using the [formatting context](formatting-context.md). However, only the search template is also treated as a regular expression. The replacement fields available in the formatting context are enclosed in curly braces `{}`. 

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

## Using regular expressions

Only the search template will use [Python's regular expression syntax](https://docs.python.org/3/library/re.html#regular-expression-syntax) with minor changes. The template string is rendered using the formatting context. The resulting string is treated as a regular expression for searching unless configured otherwise.

Curly braces (`{}`) and backslashes (`\`) must be doubled in the regular expression to escape them from the string formatting process.

The following template:

```text
{current_version} date-released: \\d{{4}}-\\d{{2}}-\\d{{2}}
```

Gets rendered to:

```text
1\.2\.3 date-released: \d{4}-\d{2}-\d{2}
```

This string is used as a regular expression pattern to search.
