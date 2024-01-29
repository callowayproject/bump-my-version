# {py:mod}`bumpversion.utils`

```{py:module} bumpversion.utils
```

```{autodoc2-docstring} bumpversion.utils
:parser: myst
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`extract_regex_flags <bumpversion.utils.extract_regex_flags>`
  - ```{autodoc2-docstring} bumpversion.utils.extract_regex_flags
    :parser: myst
    :summary:
    ```
* - {py:obj}`recursive_sort_dict <bumpversion.utils.recursive_sort_dict>`
  - ```{autodoc2-docstring} bumpversion.utils.recursive_sort_dict
    :parser: myst
    :summary:
    ```
* - {py:obj}`key_val_string <bumpversion.utils.key_val_string>`
  - ```{autodoc2-docstring} bumpversion.utils.key_val_string
    :parser: myst
    :summary:
    ```
* - {py:obj}`prefixed_environ <bumpversion.utils.prefixed_environ>`
  - ```{autodoc2-docstring} bumpversion.utils.prefixed_environ
    :parser: myst
    :summary:
    ```
* - {py:obj}`labels_for_format <bumpversion.utils.labels_for_format>`
  - ```{autodoc2-docstring} bumpversion.utils.labels_for_format
    :parser: myst
    :summary:
    ```
* - {py:obj}`base_context <bumpversion.utils.base_context>`
  - ```{autodoc2-docstring} bumpversion.utils.base_context
    :parser: myst
    :summary:
    ```
* - {py:obj}`get_context <bumpversion.utils.get_context>`
  - ```{autodoc2-docstring} bumpversion.utils.get_context
    :parser: myst
    :summary:
    ```
* - {py:obj}`get_overrides <bumpversion.utils.get_overrides>`
  - ```{autodoc2-docstring} bumpversion.utils.get_overrides
    :parser: myst
    :summary:
    ```
* - {py:obj}`get_nested_value <bumpversion.utils.get_nested_value>`
  - ```{autodoc2-docstring} bumpversion.utils.get_nested_value
    :parser: myst
    :summary:
    ```
* - {py:obj}`set_nested_value <bumpversion.utils.set_nested_value>`
  - ```{autodoc2-docstring} bumpversion.utils.set_nested_value
    :parser: myst
    :summary:
    ```
````

### API

````{py:function} extract_regex_flags(regex_pattern: str) -> typing.Tuple[str, str]
:canonical: bumpversion.utils.extract_regex_flags

```{autodoc2-docstring} bumpversion.utils.extract_regex_flags
:parser: myst
```
````

````{py:function} recursive_sort_dict(input_value: typing.Any) -> typing.Any
:canonical: bumpversion.utils.recursive_sort_dict

```{autodoc2-docstring} bumpversion.utils.recursive_sort_dict
:parser: myst
```
````

````{py:function} key_val_string(d: dict) -> str
:canonical: bumpversion.utils.key_val_string

```{autodoc2-docstring} bumpversion.utils.key_val_string
:parser: myst
```
````

````{py:function} prefixed_environ() -> dict
:canonical: bumpversion.utils.prefixed_environ

```{autodoc2-docstring} bumpversion.utils.prefixed_environ
:parser: myst
```
````

````{py:function} labels_for_format(serialize_format: str) -> typing.List[str]
:canonical: bumpversion.utils.labels_for_format

```{autodoc2-docstring} bumpversion.utils.labels_for_format
:parser: myst
```
````

````{py:function} base_context(scm_info: typing.Optional[bumpversion.scm.SCMInfo] = None) -> collections.ChainMap
:canonical: bumpversion.utils.base_context

```{autodoc2-docstring} bumpversion.utils.base_context
:parser: myst
```
````

````{py:function} get_context(config: bumpversion.config.Config, current_version: typing.Optional[bumpversion.versioning.models.Version] = None, new_version: typing.Optional[bumpversion.versioning.models.Version] = None) -> collections.ChainMap
:canonical: bumpversion.utils.get_context

```{autodoc2-docstring} bumpversion.utils.get_context
:parser: myst
```
````

````{py:function} get_overrides(**kwargs) -> dict
:canonical: bumpversion.utils.get_overrides

```{autodoc2-docstring} bumpversion.utils.get_overrides
:parser: myst
```
````

````{py:function} get_nested_value(d: dict, path: str) -> typing.Any
:canonical: bumpversion.utils.get_nested_value

```{autodoc2-docstring} bumpversion.utils.get_nested_value
:parser: myst
```
````

````{py:function} set_nested_value(d: dict, value: typing.Any, path: str) -> None
:canonical: bumpversion.utils.set_nested_value

```{autodoc2-docstring} bumpversion.utils.set_nested_value
:parser: myst
```
````
