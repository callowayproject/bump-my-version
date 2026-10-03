# How to set a version part to a specific value

Normally `bump` increments a part by one step. Sometimes you want to jump a part straight to a value instead, such as moving from a pre-release to the final release, or forcing a `1.0.0` release. Use `--to` with the part you want to change:

```console
bump-my-version bump major --to 1
```

With a current version of `0.9.3`, the new version is `1.0.0`. Like a normal bump, the parts that depend on the changed part (`minor` and `patch` here) are reset to their first value.

## Jumping to the last value in a list

Given this configuration:

```toml title=".bumpversion.toml or other config file"
[tool.bumpversion.parts.release]
optional_value = "final"
values = ["beta", "rc", "final"]
```

You can skip straight to the final release from any pre-release:

```console
bump-my-version bump release --to final
```

## Things to know

- `--to` takes one part per run. To set several parts at once, use `--new-version` with the whole version.
- `--to` and `--new-version` cannot be used together, and `--to` requires a version part.
- The value must be valid for the part. For a part with `values`, it must be one of them. For a numeric part, it must contain a number that is not lower than the `first_value`. It _can_ be lower than the current value.
- CalVer parts are based on the date and cannot be set with `--to`.
- Parts that always increment (`always_increment`) still increment, as they do in a normal bump.
- `include_bumps` and `exclude_bumps` file filters apply to the part named on the command line.
