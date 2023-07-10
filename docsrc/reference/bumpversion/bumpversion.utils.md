# {py:mod}`bumpversion.utils`

```{py:module} bumpversion.utils
```

```{autodoc2-docstring} bumpversion.utils
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`key_val_string <bumpversion.utils.key_val_string>`
  - ```{autodoc2-docstring} bumpversion.utils.key_val_string
    :summary:
    ```
* - {py:obj}`prefixed_environ <bumpversion.utils.prefixed_environ>`
  - ```{autodoc2-docstring} bumpversion.utils.prefixed_environ
    :summary:
    ```
* - {py:obj}`labels_for_format <bumpversion.utils.labels_for_format>`
  - ```{autodoc2-docstring} bumpversion.utils.labels_for_format
    :summary:
    ```
* - {py:obj}`get_context <bumpversion.utils.get_context>`
  - ```{autodoc2-docstring} bumpversion.utils.get_context
    :summary:
    ```
* - {py:obj}`get_overrides <bumpversion.utils.get_overrides>`
  - ```{autodoc2-docstring} bumpversion.utils.get_overrides
    :summary:
    ```
````

### API

````{py:function} key_val_string(d: dict) -> str
:canonical: bumpversion.utils.key_val_string

```{autodoc2-docstring} bumpversion.utils.key_val_string
```
````

````{py:function} prefixed_environ() -> dict
:canonical: bumpversion.utils.prefixed_environ

```{autodoc2-docstring} bumpversion.utils.prefixed_environ
```
````

````{py:function} labels_for_format(serialize_format: str) -> typing.List[str]
:canonical: bumpversion.utils.labels_for_format

```{autodoc2-docstring} bumpversion.utils.labels_for_format
```
````

````{py:function} get_context(config: bumpversion.config.Config, current_version: typing.Optional[bumpversion.version_part.Version] = None, new_version: typing.Optional[bumpversion.version_part.Version] = None) -> collections.ChainMap
:canonical: bumpversion.utils.get_context

```{autodoc2-docstring} bumpversion.utils.get_context
```
````

````{py:function} get_overrides(**kwargs) -> dict
:canonical: bumpversion.utils.get_overrides

```{autodoc2-docstring} bumpversion.utils.get_overrides
```
````
