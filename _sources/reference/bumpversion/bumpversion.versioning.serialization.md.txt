# {py:mod}`bumpversion.versioning.serialization`

```{py:module} bumpversion.versioning.serialization
```

```{autodoc2-docstring} bumpversion.versioning.serialization
:parser: myst
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`parse_version <bumpversion.versioning.serialization.parse_version>`
  - ```{autodoc2-docstring} bumpversion.versioning.serialization.parse_version
    :parser: myst
    :summary:
    ```
* - {py:obj}`multisort <bumpversion.versioning.serialization.multisort>`
  - ```{autodoc2-docstring} bumpversion.versioning.serialization.multisort
    :parser: myst
    :summary:
    ```
* - {py:obj}`serialize <bumpversion.versioning.serialization.serialize>`
  - ```{autodoc2-docstring} bumpversion.versioning.serialization.serialize
    :parser: myst
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`logger <bumpversion.versioning.serialization.logger>`
  - ```{autodoc2-docstring} bumpversion.versioning.serialization.logger
    :parser: myst
    :summary:
    ```
````

### API

````{py:data} logger
:canonical: bumpversion.versioning.serialization.logger
:value: >
   'get_indented_logger(...)'

```{autodoc2-docstring} bumpversion.versioning.serialization.logger
:parser: myst
```

````

````{py:function} parse_version(version_string: str, parse_pattern: str) -> typing.Dict[str, str]
:canonical: bumpversion.versioning.serialization.parse_version

```{autodoc2-docstring} bumpversion.versioning.serialization.parse_version
:parser: myst
```
````

````{py:function} multisort(xs: list, specs: tuple) -> list
:canonical: bumpversion.versioning.serialization.multisort

```{autodoc2-docstring} bumpversion.versioning.serialization.multisort
:parser: myst
```
````

````{py:function} serialize(version: bumpversion.versioning.models.Version, serialize_patterns: typing.List[str], context: typing.MutableMapping) -> str
:canonical: bumpversion.versioning.serialization.serialize

```{autodoc2-docstring} bumpversion.versioning.serialization.serialize
:parser: myst
```
````
