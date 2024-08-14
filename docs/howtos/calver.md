# Using Calendar Versioning (CalVer)

Calendar Versioning (CalVer) is a versioning scheme that uses a date-based version number. 

For this example, we will use the following format: `YYYY.MM.DD.patch`. It will yield numbers like:

- `2022.2.1` for the first patch of February 1, 2022
- `2022.2.1.1` for the second patch of February 1, 2022

## Initial configuration

```toml title=".bumpversion.toml"
[tool.bumpversion]
current_version = "2024.3.1.4"
parse = """(?x)                     # Verbose mode
    (?P<release>                    # The release part
        (?:[1-9][0-9]{3})\\.        # YYYY.
        (?:1[0-2]|[1-9])\\.         # MM.
        (?:3[0-1]|[1-2][0-9]|[1-9]) # DD
    )
    (?:\\.(?P<patch>\\d+))?         # .patch, optional
"""
serialize = ["{release}.{patch}", "{release}"]

[tool.bumpversion.parts.release]
calver_format = "{YYYY}.{MM}.{DD}"
```

You can look up the regular expressions for the CalVer format in the [CalVer reference](../reference/calver_reference.md).

## Expected behavior

- CalVer version components are marked as `always_increment` by default.
- When bumping a version, you specify which component to increment. It is called the target component.
- When bumping a version, the components marked as `always_increment` are incremented first.
- If an `always_increment` component's value changed, its dependent components are marked for reset to their default values.
- If the target component is in the set of components marked for reset, the target component is reset to its default value.
- If the target component is not in the set of components marked for reset, the target component is incremented and its dependent components are reset to their default values.

### Bumping the release resets the patch part

When you bump the calendar version, the patch is reset to 0 _even if the release did not change._

```console title="Bumping the release resets patch"
$ date -I      
2024-03-1
$ bump-my-version show-bump
2024.3.1.4 ── bump ─┬─ release ─ 2024.3.1
                    ╰─ patch ─── 2024.3.1.5
```

The next day:

```console title="Bumping the release resets patch, the next day"
$ date -I      
2024-03-2
$ bump-my-version show-bump
2024.3.1.4 ── bump ─┬─ release ─ 2024.3.2
                    ╰─ patch ─── 2024.3.2
```

### The result of a bump to patch depends on the date

Calendar Versioned parts are updated with every bump, regardless of the part being bumped. If you are bumping the version within the same time period (in this example, the same day), the `release` part will not change. So bumping the `patch` part will increment the `patch` part only.


```console title="Bumping patch on the same day"
$ date -I      
2024-03-1
$ bump-my-version show-bump
2024.3.1.4 ── bump ─┬─ release ─ 2024.3.1
                    ╰─ patch ─── 2024.3.1.5
```

However, if you bump the version on the next day, the `release` part will also be updated.

```console title="Bumping patch on the next day"
$ date -I      
2024-03-2
$ bump-my-version show-bump
2024.3.1.4 ── bump ─┬─ release ─ 2024.3.2
                    ╰─ patch ─── 2024.3.2
```
