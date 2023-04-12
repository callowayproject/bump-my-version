# Version parts

A version string consists of one or more parts, e.g. the version `1.0.2` has three parts, separated by a dot (`.`) character. The names of these parts are defined in the named groups within the `parse` regular expression. The default configuration ( `(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)`) names them *major, minor,* and *patch.*

By default all parts are considered numeric, that is their initial value is `0` and they are increased as integers. Also, the value `0` is considered to be
optional if it's not needed for serialization, i.e. the version `1.4.0` is
equal to `1.4` if `{major}.{minor}` is given as a `serialize` value.

For advanced versioning schemes, non-numeric parts may be desirable (e.g. to
identify [alpha or beta versions](http://en.wikipedia.org/wiki/Software_release_life_cycle#Stages_of_development)
to indicate the stage of development, the flavor of the software package or
a release name). To do so, you can use a `[bumpversion:part:…]` section
containing the part's name (e.g. a part named `release_name` is configured in
a section called `[bumpversion:part:release_name]`.

The following options are valid inside a part configuration:





Example:

```ini
[bumpversion:part:release_name]
values =
witty-warthog
ridiculous-rat
marvelous-mantis
```

---

Example:

```ini
[bumpversion]
current_version = 1.alpha
parse = (?P<num>\d+)(\.(?P<release>.*))?
serialize =
{num}.{release}
{num}

[bumpversion:part:release]
optional_value = gamma
values =
alpha
beta
gamma
```

Here, `bump-my-version release` would bump `1.alpha` to `1.beta`. Executing
`bump-my-version release` again would bump `1.beta` to `1`, because
`release` being `gamma` is configured optional.

You should consider the version of `1` to technically be `1.gamma`
with the `.gamma` part not being serialized since it is optional.
The `{num}` entry in the `serialize` list allows the release part to be
hidden. If you only had `{num}.{release}`, an optional release will always
be serialized.

Attempting to bump the release when it is the value of
`gamma` will cause a `ValueError` as it will think you are trying to
exceed the `values` list of the release part.

---

Example:

```ini
[bumpversion]
current_version = 1.alpha1
parse = (?P<num>\d+)(\.(?P<release>.*)(?P<build>\d+))?
serialize =
{num}.{release}{build}

[bumpversion:part:release]
values =
alpha
beta
gamma

[bumpversion:part:build]
first_value = 1
```

Here, `bump-my-version release` would bump `1.alpha1` to `1.beta1`.

Without the `first_value = 1` of the build part configured,
`bump-my-version release` would bump `1.alpha1` to `1.beta0`, starting
the build at `0`.



---

Example:

```ini
[bumpversion]
current_version: 2.1.6-5123
parse = (?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)\-(?P<build>\d+)
serialize = {major}.{minor}.{patch}-{build}

[bumpversion:file:VERSION.txt]

[bumpversion:part:build]
independent = True
```

Here, `bump-my-version build` would bump `2.1.6-5123` to `2.1.6-5124`. Executing`bump-my-version major`
would bump `2.1.6-5124` to `3.0.0-5124` without resetting the build number.
