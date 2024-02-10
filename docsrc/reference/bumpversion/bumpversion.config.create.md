# {py:mod}`bumpversion.config.create`

```{py:module} bumpversion.config.create
```

```{autodoc2-docstring} bumpversion.config.create
:parser: myst
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`create_configuration <bumpversion.config.create.create_configuration>`
  - ```{autodoc2-docstring} bumpversion.config.create.create_configuration
    :parser: myst
    :summary:
    ```
* - {py:obj}`get_defaults_from_dest <bumpversion.config.create.get_defaults_from_dest>`
  - ```{autodoc2-docstring} bumpversion.config.create.get_defaults_from_dest
    :parser: myst
    :summary:
    ```
````

### API

````{py:function} create_configuration(destination: str, prompt: bool) -> tomlkit.TOMLDocument
:canonical: bumpversion.config.create.create_configuration

```{autodoc2-docstring} bumpversion.config.create.create_configuration
:parser: myst
```
````

````{py:function} get_defaults_from_dest(destination: str) -> typing.Tuple[dict, tomlkit.TOMLDocument]
:canonical: bumpversion.config.create.get_defaults_from_dest

```{autodoc2-docstring} bumpversion.config.create.get_defaults_from_dest
:parser: myst
```
````