# Searching and replacing versions

Given this `requirements.txt`:

  Django>=1.5.6,<1.6
  MyProject==1.5.6

using this `.bumpversion.cfg` will ensure only the line containing
`MyProject` will be changed:

```ini
[bumpversion]
current_version = 1.5.6

[bumpversion:file:requirements.txt]
search = MyProject=={current_version}
replace = MyProject=={new_version}
```

Can be multiple lines, templated using [Python Format String Syntax](https://docs.python.org/3/library/string.html#format-string-syntax).

**NOTE**: (*Updated in v1.0.1*) It is important to point out that if a
custom search pattern is configured, then `bump-my-version` will only perform
a change if it finds an exact match and will not fallback to the default
pattern. This is to prevent accidentally changing strings that match the
default pattern when there is a typo in the custom search pattern.

For example, if the string to be replaced includes literal quotes,
the search and replace patterns must include them too to match. Given the
file `version.sh`:

    MY_VERSION="1.2.3"

Then the following search and replace patterns (including quotes) would be
required:

```ini
[bumpversion:file:version.sh]
search = MY_VERSION="{current_version}"
replace = MY_VERSION="{new_version}"
```

---

## Using bumpversion to maintain a go.mod file within a Go project

In a module-aware Go project, when you create a major version of your module beyond v1, your module name will need to include the major version number (e.g. `github.com/myorg/myproject/v2`).

You can use bump-my-version to maintain the major version number within the `go.mod` file by using the `parse` and `serialize` options, as in this example:

- Example `.bumpversion.toml` file:

```toml
[tool.bumpversion]
current_version = 2.0.0
commit = True

[[tool.bumpversion.files]]
filename: go.mod
parse = (?P<major>\d+)
serialize = {major}
search = module github.com/myorg/myproject/v{current_version}
replace = module github.com/myorg/myproject/v{new_version}
```

- Example `go.mod` file:

```go
module github.com/myorg/myproject/v2

go 1.12

require (
    ...
)
```

Then run this command to create version 3.0.0 of your project:

```console
bump-my-version --new-version 3.0.0 major
```

Your `go.mod` file now contains this module directive:

```go
module github.com/myorg/myproject/v3
```

## 
