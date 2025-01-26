# Moveable version tags

While controversial, [several platforms](https://github.com/actions/toolkit/blob/master/docs/action-versioning.md) recommend providing moving "release bindings."
These release bindings are tags that represent the latest revision of a version component.
For example, a tag of `v1` is similar to specifying a dependency of `>=1.0.0 <2.0.0`.
A tag of `v1.1` is similar to specifying a dependency of `>=1.1.0 <1.2.0`.

Bump My Version's stance is to provide unique, immutable release tags when tagging is enabled as its default behavior.
"Moving" tags are an optional choice and will work in addition to the default behavior.

## How they work

- The `moving_tags` configuration is a list of serialization strings.
- All strings are serialized
- Each string is forcibly tagged (as a lightweight, non-annotated tag) and forcibly pushed to origin. 


## Configuration

```toml
moving_tags = [
    "latest",
    "v{major}.{minor}.{patch}",
    "v{major}.{minor}",
    "v{major}"
]
```

## Example

![](../assets/moving-tags.svg)
