# Custom version formats in different files

You can use file configurations to replace the version in multiple files, even if each file has the version formatted differently.

In a module-aware Go project, when you create a major version of your module beyond `v1`, your module name must include the major version number (e.g., `github.com/myorg/myproject/v2`). However, you also have the full version in a YAML file named `release-channels.yaml`.

`go.mod` file:

```go
module github.com/myorg/myproject/v2

go 1.12

require (
    ...
)
```

`release-channels.yaml` file:

```yaml
stable: "v2.21.4"
```

You can use Bump My Version to maintain the major version number within the `go.mod` file by using the `parse` and `serialize` options, as in this example:

 `.bumpversion.toml` file:

```toml
[tool.bumpversion]
current_version = "2.21.4"

[[tool.bumpversion.files]]
filename = "go.mod"
parse = "(?P<major>\\d+)"
serialize = "{major}"
search = "module github.com/myorg/myproject/v{current_version}"
replace = "module github.com/myorg/myproject/v{new_version}"

[[tool.bumpversion.files]]
filename = "release-channels.yaml"
```

While all the version bumps are `minor` or `patch`, the `go.mod` file doesn't change, while the `release-channels.yaml` file will. As soon as you do a `major` version bump, the `go.mod` file now contains this module directive:

```go
module github.com/myorg/myproject/v3
```
