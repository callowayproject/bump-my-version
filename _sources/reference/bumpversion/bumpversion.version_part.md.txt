# {py:mod}`bumpversion.version_part`

```{py:module} bumpversion.version_part
```

```{autodoc2-docstring} bumpversion.version_part
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`VersionConfig <bumpversion.version_part.VersionConfig>`
  - ```{autodoc2-docstring} bumpversion.version_part.VersionConfig
    :parser: myst
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`logger <bumpversion.version_part.logger>`
  - ```{autodoc2-docstring} bumpversion.version_part.logger
    :parser: myst
    :summary:
    ```
````

### API

````{py:data} logger
:canonical: bumpversion.version_part.logger
:value: >
   'get_indented_logger(...)'

```{autodoc2-docstring} bumpversion.version_part.logger
:parser: myst
```

````

`````{py:class} VersionConfig(parse: str, serialize: typing.Tuple[str], search: str, replace: str, part_configs: typing.Optional[typing.Dict[str, bumpversion.versioning.models.VersionComponentSpec]] = None)
:canonical: bumpversion.version_part.VersionConfig

```{autodoc2-docstring} bumpversion.version_part.VersionConfig
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.version_part.VersionConfig.__init__
:parser: myst
```

````{py:method} __repr__() -> str
:canonical: bumpversion.version_part.VersionConfig.__repr__

````

````{py:method} __eq__(other: typing.Any) -> bool
:canonical: bumpversion.version_part.VersionConfig.__eq__

````

````{py:property} order
:canonical: bumpversion.version_part.VersionConfig.order
:type: typing.List[str]

```{autodoc2-docstring} bumpversion.version_part.VersionConfig.order
:parser: myst
```

````

````{py:method} parse(version_string: typing.Optional[str] = None) -> typing.Optional[bumpversion.versioning.models.Version]
:canonical: bumpversion.version_part.VersionConfig.parse

```{autodoc2-docstring} bumpversion.version_part.VersionConfig.parse
:parser: myst
```

````

````{py:method} serialize(version: bumpversion.versioning.models.Version, context: typing.MutableMapping) -> str
:canonical: bumpversion.version_part.VersionConfig.serialize

```{autodoc2-docstring} bumpversion.version_part.VersionConfig.serialize
:parser: myst
```

````

`````
