# Search and replace configuration

Bump-my-version uses a combination of [template strings](https://docs.python.org/3/library/string.html#format-string-syntax) using a [formatting context](formatting-context.md) and regular expressions to search the configured files for the old or current version and replace the text with the new version.

Bump My Version defaults to using a simple string search. If the search template is not a valid regular expression or if the `no-regex` flag is `True`. The search template is always rendered using the formatting context. The basic logic is:

1. Escape the formatting context for use in a regular expression.
2. Render the search string using the escaped formatting context.
3. Attempt to compile the rendered search string as a regular expression.
4. If the rendered search string is a valid regular expression, use it.
5. If the rendered search string is _not_ a valid regular expression or the `no-regex` flag is `True`, use the search string rendered with the unescaped context.

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

Curly braces (`{}`) must be doubled in the regular expression to escape them from the string-formatting process.

If you are using a TOML-formatted configuration file, you must also escape backslashes (`\`) in the regular expression. The TOML parser will treat a single backslash as an escape character. 

The following template:

=== "TOML"

    ```toml
    search = "{current_version} date-released: \\d{{4}}-\\d{{2}}-\\d{{2}}"
    ```

=== "CFG"

    ```ini
    search = "{current_version} date-released: \d{{4}}-\d{{2}}-\d{{2}}"
    ```

Gets rendered to:

```text
1\.2\.3 date-released: \d{4}-\d{2}-\d{2}
```

This string is used as a regular expression pattern to search.

## Regular expression special characters

The `.`, `^`, `$`, `*`, `+`, `?`, `()`, `[]`, `{}`, `\`, `|` characters are special characters in regular expressions. If your search string contains these characters, you must escape them with a backslash (`\`) to treat them as literal characters or set the `no-regex` flag to `True`.

For example, if you are looking for this string in a file:

```text
[Unreleased] 2023-07-17
```

and you use this search pattern:

```text
[Unreleased] \\d{{4}}-\\d{{2}}-\\d{{2}}
```

Bump My Version will not find the string. While the rendered regular expression `[Unreleased] \d{4}-\d{2}-\d{2}` is valid, it is not searching for the literal `[Unreleased]`. Instead, it matches a single character in the list `U`, `n`, `r`, `e`, `l`, `a`, `s`, `d`.

You must escape the `[` and `]` to treat them as literal characters:

```text
\[Unreleased\] \\d{{4}}-\\d{{2}}-\\d{{2}}
```
