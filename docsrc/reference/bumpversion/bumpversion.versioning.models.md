# {py:mod}`bumpversion.versioning.models`

```{py:module} bumpversion.versioning.models
```

```{autodoc2-docstring} bumpversion.versioning.models
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`VersionComponent <bumpversion.versioning.models.VersionComponent>`
  - ```{autodoc2-docstring} bumpversion.versioning.models.VersionComponent
    :parser: myst
    :summary:
    ```
* - {py:obj}`VersionComponentSpec <bumpversion.versioning.models.VersionComponentSpec>`
  - ```{autodoc2-docstring} bumpversion.versioning.models.VersionComponentSpec
    :parser: myst
    :summary:
    ```
* - {py:obj}`VersionSpec <bumpversion.versioning.models.VersionSpec>`
  - ```{autodoc2-docstring} bumpversion.versioning.models.VersionSpec
    :parser: myst
    :summary:
    ```
* - {py:obj}`Version <bumpversion.versioning.models.Version>`
  - ```{autodoc2-docstring} bumpversion.versioning.models.Version
    :parser: myst
    :summary:
    ```
````

### API

`````{py:class} VersionComponent(values: typing.Optional[list] = None, optional_value: typing.Optional[str] = None, first_value: typing.Union[str, int, None] = None, independent: bool = False, source: typing.Optional[str] = None, value: typing.Union[str, int, None] = None)
:canonical: bumpversion.versioning.models.VersionComponent

```{autodoc2-docstring} bumpversion.versioning.models.VersionComponent
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.versioning.models.VersionComponent.__init__
:parser: myst
```

````{py:property} value
:canonical: bumpversion.versioning.models.VersionComponent.value
:type: str

```{autodoc2-docstring} bumpversion.versioning.models.VersionComponent.value
:parser: myst
```

````

````{py:method} copy() -> bumpversion.versioning.models.VersionComponent
:canonical: bumpversion.versioning.models.VersionComponent.copy

```{autodoc2-docstring} bumpversion.versioning.models.VersionComponent.copy
:parser: myst
```

````

````{py:method} bump() -> bumpversion.versioning.models.VersionComponent
:canonical: bumpversion.versioning.models.VersionComponent.bump

```{autodoc2-docstring} bumpversion.versioning.models.VersionComponent.bump
:parser: myst
```

````

````{py:method} null() -> bumpversion.versioning.models.VersionComponent
:canonical: bumpversion.versioning.models.VersionComponent.null

```{autodoc2-docstring} bumpversion.versioning.models.VersionComponent.null
:parser: myst
```

````

````{py:property} is_optional
:canonical: bumpversion.versioning.models.VersionComponent.is_optional
:type: bool

```{autodoc2-docstring} bumpversion.versioning.models.VersionComponent.is_optional
:parser: myst
```

````

````{py:property} is_independent
:canonical: bumpversion.versioning.models.VersionComponent.is_independent
:type: bool

```{autodoc2-docstring} bumpversion.versioning.models.VersionComponent.is_independent
:parser: myst
```

````

````{py:method} __format__(format_spec: str) -> str
:canonical: bumpversion.versioning.models.VersionComponent.__format__

````

````{py:method} __repr__() -> str
:canonical: bumpversion.versioning.models.VersionComponent.__repr__

````

````{py:method} __eq__(other: typing.Any) -> bool
:canonical: bumpversion.versioning.models.VersionComponent.__eq__

````

`````

`````{py:class} VersionComponentSpec(**data: typing.Any)
:canonical: bumpversion.versioning.models.VersionComponentSpec

Bases: {py:obj}`pydantic.BaseModel`

```{autodoc2-docstring} bumpversion.versioning.models.VersionComponentSpec
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.versioning.models.VersionComponentSpec.__init__
:parser: myst
```

````{py:attribute} values
:canonical: bumpversion.versioning.models.VersionComponentSpec.values
:type: typing.Optional[list]
:value: >
   None

```{autodoc2-docstring} bumpversion.versioning.models.VersionComponentSpec.values
:parser: myst
```

````

````{py:attribute} optional_value
:canonical: bumpversion.versioning.models.VersionComponentSpec.optional_value
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} bumpversion.versioning.models.VersionComponentSpec.optional_value
:parser: myst
```

````

````{py:attribute} first_value
:canonical: bumpversion.versioning.models.VersionComponentSpec.first_value
:type: typing.Union[str, int, None]
:value: >
   None

```{autodoc2-docstring} bumpversion.versioning.models.VersionComponentSpec.first_value
:parser: myst
```

````

````{py:attribute} independent
:canonical: bumpversion.versioning.models.VersionComponentSpec.independent
:type: bool
:value: >
   False

```{autodoc2-docstring} bumpversion.versioning.models.VersionComponentSpec.independent
:parser: myst
```

````

````{py:attribute} depends_on
:canonical: bumpversion.versioning.models.VersionComponentSpec.depends_on
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} bumpversion.versioning.models.VersionComponentSpec.depends_on
:parser: myst
```

````

````{py:method} create_component(value: typing.Union[str, int, None] = None) -> bumpversion.versioning.models.VersionComponent
:canonical: bumpversion.versioning.models.VersionComponentSpec.create_component

```{autodoc2-docstring} bumpversion.versioning.models.VersionComponentSpec.create_component
:parser: myst
```

````

`````

`````{py:class} VersionSpec(components: typing.Dict[str, bumpversion.versioning.models.VersionComponentSpec], order: typing.Optional[typing.List[str]] = None)
:canonical: bumpversion.versioning.models.VersionSpec

```{autodoc2-docstring} bumpversion.versioning.models.VersionSpec
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.versioning.models.VersionSpec.__init__
:parser: myst
```

````{py:method} create_version(values: typing.Dict[str, str]) -> bumpversion.versioning.models.Version
:canonical: bumpversion.versioning.models.VersionSpec.create_version

```{autodoc2-docstring} bumpversion.versioning.models.VersionSpec.create_version
:parser: myst
```

````

````{py:method} get_dependents(component_name: str) -> typing.List[str]
:canonical: bumpversion.versioning.models.VersionSpec.get_dependents

```{autodoc2-docstring} bumpversion.versioning.models.VersionSpec.get_dependents
:parser: myst
```

````

`````

`````{py:class} Version(version_spec: bumpversion.versioning.models.VersionSpec, components: typing.Dict[str, bumpversion.versioning.models.VersionComponent], original: typing.Optional[str] = None)
:canonical: bumpversion.versioning.models.Version

```{autodoc2-docstring} bumpversion.versioning.models.Version
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.versioning.models.Version.__init__
:parser: myst
```

````{py:method} values() -> typing.Dict[str, str]
:canonical: bumpversion.versioning.models.Version.values

```{autodoc2-docstring} bumpversion.versioning.models.Version.values
:parser: myst
```

````

````{py:method} __getitem__(key: str) -> bumpversion.versioning.models.VersionComponent
:canonical: bumpversion.versioning.models.Version.__getitem__

```{autodoc2-docstring} bumpversion.versioning.models.Version.__getitem__
:parser: myst
```

````

````{py:method} __len__() -> int
:canonical: bumpversion.versioning.models.Version.__len__

```{autodoc2-docstring} bumpversion.versioning.models.Version.__len__
:parser: myst
```

````

````{py:method} __iter__()
:canonical: bumpversion.versioning.models.Version.__iter__

```{autodoc2-docstring} bumpversion.versioning.models.Version.__iter__
:parser: myst
```

````

````{py:method} __repr__()
:canonical: bumpversion.versioning.models.Version.__repr__

````

````{py:method} __eq__(other: typing.Any) -> bool
:canonical: bumpversion.versioning.models.Version.__eq__

````

````{py:method} required_components() -> typing.List[str]
:canonical: bumpversion.versioning.models.Version.required_components

```{autodoc2-docstring} bumpversion.versioning.models.Version.required_components
:parser: myst
```

````

````{py:method} bump(component_name: str) -> bumpversion.versioning.models.Version
:canonical: bumpversion.versioning.models.Version.bump

```{autodoc2-docstring} bumpversion.versioning.models.Version.bump
:parser: myst
```

````

`````
