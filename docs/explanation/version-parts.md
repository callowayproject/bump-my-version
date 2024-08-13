# Version components

- The version string is the rendering of some or all version parts.
- While the version string may be rendered differently in various places, the value for all parts is maintained in Bump My Version's configuration.
- The version parts are typically dependent on each other. Incrementing one part might change other elements.
- You can compare two version strings (of the same project) and know which is more recent.

## Version configuration

A version configuration consists of the following:

- A regular expression that will parse all the possible parts and name them
- A list of one or more serialization formats

A version string consists of one or more parts; e.g., version `1.0.2` has three parts, separated by a dot (`.`) character.

The names of these parts are defined in the named groups within the `parse` regular expression. The default configuration calls them *major, minor,* and *patch.*

The `serialize` configuration value is a list of default formats. You have the option for multiple serialization formats to omit *optional* values. For example, the following configuration:

```toml
serialize = [
    "{major}.{minor}.{patch}",
    "{major}.{minor}",
]
```

Bump-my-version will serialize using the first format if the `patch` value is not `0`. If the `patch` value *is* `0`, Bump My Version will use the second format.

## Version part configuration

A version part configuration consists of the following:

- An incrementing function
- An optional value
- A first value
- A flag indicating its dependence or independence of changes to other version parts

### Incrementing functions

There are two incrementing functions: numeric and value. The numeric function uses integer values and returns the next integer value. The values function uses a sequence of values and returns the next value until finished.

By default, parts use the numeric function starting at 0.

You can configure a part using the values function by providing a list of values in the version part's configuration. For example, for the `release_name` part:

```toml
[tool.bumpversion.parts.release_name]
values = [
    "witty-warthog", 
    "ridiculous-rat", 
    "marvelous-mantis",
]
```

### Optional values

By default, the *first* value of a version part is considered *optional.* An optional value may be omitted from the version serialization. Using the example from above:

```toml
serialize = [
    "{major}.{minor}.{patch}",
    "{major}.{minor}",
]
```

Version `1.4.0` is rendered as `1.4` since the `patch` is `0`; as the first value, it is optional.

Optional values are helpful for non-numeric version parts that indicate development stages, such as [alpha or beta](http://en.wikipedia.org/wiki/Software_release_life_cycle#Stages_of_development).

Example:

```toml
[tool.bumpversion]
current_version = "1.0.0"
parse = """(?x)
    (?P<major>[0-9]+)
    \\.(?P<minor>[0-9]+)
    \\.(?P<patch>[0-9]+)
    (?:
        -(?P<pre_label>alpha|beta|stable)
        (?:-(?P<pre_n>[0-9]+))?
    )?
"""
serialize = [
	"{major}.{minor}.{patch}-{pre_label}-{pre_n}",
	"{major}.{minor}.{patch}",
]

[tool.bumpversion.parts.pre_label]
optional_value = "stable"
values =[
	"alpha",
	"beta",
	"stable",
]
```

Bumping the `patch` part of version `1.0.0` would change the version to `1.0.1-alpha-0`. Bumping the `pre_label` part would change the version to `1.0.1-beta-0`. Bumping the `pre_label` part again would change the version to `1.0.1`. The `stable-0` is not serialized because both `stable` and `0` are *optional*.

### First Values

You can specify the starting number with the first_value configuration for numeric version parts.

For example, if we added the following to the above configuration:

```toml
[tool.bumpversion.parts.pre_n]
first_value = "1"
```

Bumping the `patch` value of version `1.0.0` would change the version to `1.0.1-alpha-1` instead of `1.0.1-alpha-0`.

### Independent Values

In the pattern `{major}.{minor}.{patch}-{pre_label}-{pre_n}`, each version part resets to its first value when the element preceding it changes. All these version parts are *dependent.*

You can include a value that incremented *independently* from the other parts, such as a `build` part: `{major}.{minor}.{patch}-{pre_label}-{pre_n}+{build}`—in the configuration for that part, set `independent=true`.

```toml
[tool.bumpversion.parts.build]
independent = true
```

## Reference

- https://devopedia.org/semantic-versioning
- https://semver.org
- https://calver.org
