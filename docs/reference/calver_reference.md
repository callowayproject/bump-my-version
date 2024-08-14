# Calendar versioning reference

## Calendar versioning codes

The following table lists the available format codes for calendar versioning (CalVer) schemes. The codes can be used to
define the version format in the `calver_format` configuration options. Formatting codes, surrounded by `{ }` can be
combined to create a custom version format. For example, the format `YYYY.MM.DD` can be defined as `"{YYYY}.{MM}.{DD}"`.

| Code   | Example(s)          | Comment                                       |
|--------|---------------------|-----------------------------------------------|
| `YYYY` | 2000, 2001, …, 2099 | Full year                                     |
| `YY`   | 0, 1, 2, …, 99      | Short year as integer                         |
| `0Y`   | 00, 01, 02, …, 99   | Short Year, zero-padded                       |
| `MMM`  | Jan, Feb, jan, fév  | Month abbreviation, locale-based              |
| `MM`   | 1, 2, …, 12         | Month as integer                              |
| `0M`   | 01, 02, …, 12       | Month, zero-padded                            |
| `DD`   | 1, 2, …, 31         | Day of month as integer                       |
| `0D`   | 01, 02, …, 31       | Day of month, zero-padded                     |
| `JJJ`  | 1, 2, 3, …, 366     | Day of year as integer                        |
| `00J`  | 001, 002, …, 366    | Day of year, zero-padded                      |
| `Q`    | 1, 2, 3, 4          | Quarter                                       |
| `WW`   | 0, 1, 2, …, 53      | Week number, Monday is first day              |
| `0W`   | 00, 01, 02, …, 53   | Week number, Monday is first day, zero-padded |
| `UU`   | 0, 1, 2, …, 53      | Week number, Sunday is first day              |
| `0U`   | 00, 01, 02, …, 53   | Week number, Sunday is first day, zero-padded |
| `VV`   | 1, 2, …, 53         | ISO 8601 week number as integer               |
| `0V`   | 01, 02, …, 53       | ISO 8601 week number, zero-padded             |
| `GGGG` | 2000, 2001, …, 2099 | ISO 8601 week-based year                      |
| `GG`   | 0, 1, 2, …, 99      | ISO 8601 short week-based year as integer     |
| `0G`   | 01, 02, …, 99       | ISO 8601 short week-based year, zero-padded   |

```toml title="Example configuration"
[tool.bumpversion.parts.release]
calver_format = "{YYYY}.{MM}.{DD}"
```

## Parsing CalVer versions

Using the following chart, we can set up the version parsing:

| Code   | Regex                                                             |
|--------|-------------------------------------------------------------------|
| `YYYY` | `(?:[1-9][0-9]{3})`                                               |
| `YY`   | `(?:[1-9][0-9]?)`                                                 |
| `0Y`   | `(?:[0-9]{2})`                                                    |
| `MMM`  | See below                                                         |
| `MM`   | `(?:1[0-2]\|[1-9])`                                               |
| `0M`   | `(?:1[0-2]\|0[1-9])`                                              |
| `DD`   | `(?:3[0-1]\|[1-2][0-9]\|[1-9])`                                   |
| `0D`   | `(?:3[0-1]\|[1-2][0-9]\|0[1-9])`                                  |
| `JJJ`  | `(?:36[0-6]\|3[0-5][0-9]\|[1-2][0-9][0-9]\|[1-9][0-9]\|[1-9])`    |
| `00J`  | `(?:36[0-6]\|3[0-5][0-9]\|[1-2][0-9][0-9]\|0[1-9][0-9]\|00[1-9])` |
| `Q`    | `(?:[1-4])`                                                       |
| `WW`   | `(?:5[0-3]\|[1-4][0-9]\|[0-9])`                                   |
| `0W`   | `(?:5[0-3]\|[0-4][0-9])`                                          |
| `UU`   | `(?:5[0-3]\|[1-4][0-9]\|[0-9])`                                   |
| `0U`   | `(?:5[0-3]\|[0-4][0-9])`                                          |
| `VV`   | `(?:5[0-3]\|[1-4][0-9]\|[1-9])`                                   |
| `0V`   | `(?:5[0-3]\|[1-4][0-9]\|0[1-9])`                                  |
| `GGGG` | `(?:[1-9][0-9]{3})`                                               |
| `GG`   | `(?:[0-9][0-9]?)`                                                 |
| `0G`   | `(?:[0-9]{2})`                                                    |

!!! Note "Month abbreviations"

    The month abbreviation is locale-based. Here are some examples:

    `(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)` for English

    `(?:jan|fév|mar|avr|mai|jui|jui|aoû|sep|oct|nov|déc)` for French

You can use these regular expressions to parse CalVer versions in your project. For example, the following `parse`
configuration can be used to parse a version string in the format `YYYY.MM.DD` as the `release` part of the version
string:

```toml
[tool.bumpversion]
parse = """(?x)                      # Verbose mode
    (?P<release>
        (?:[1-9][0-9]{3})\\.         # YYYY.
        (?:1[0-2]|[1-9])\\.          # MM.
        (?:3[0-1]|[1-2][0-9]|[1-9])  # DD
    )
"""
```
