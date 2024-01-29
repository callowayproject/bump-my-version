# {py:mod}`bumpversion.show`

```{py:module} bumpversion.show
```

```{autodoc2-docstring} bumpversion.show
:parser: myst
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`output_default <bumpversion.show.output_default>`
  - ```{autodoc2-docstring} bumpversion.show.output_default
    :parser: myst
    :summary:
    ```
* - {py:obj}`output_yaml <bumpversion.show.output_yaml>`
  - ```{autodoc2-docstring} bumpversion.show.output_yaml
    :parser: myst
    :summary:
    ```
* - {py:obj}`output_json <bumpversion.show.output_json>`
  - ```{autodoc2-docstring} bumpversion.show.output_json
    :parser: myst
    :summary:
    ```
* - {py:obj}`resolve_name <bumpversion.show.resolve_name>`
  - ```{autodoc2-docstring} bumpversion.show.resolve_name
    :parser: myst
    :summary:
    ```
* - {py:obj}`log_list <bumpversion.show.log_list>`
  - ```{autodoc2-docstring} bumpversion.show.log_list
    :parser: myst
    :summary:
    ```
* - {py:obj}`do_show <bumpversion.show.do_show>`
  - ```{autodoc2-docstring} bumpversion.show.do_show
    :parser: myst
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`OUTPUTTERS <bumpversion.show.OUTPUTTERS>`
  - ```{autodoc2-docstring} bumpversion.show.OUTPUTTERS
    :parser: myst
    :summary:
    ```
````

### API

````{py:function} output_default(value: dict) -> None
:canonical: bumpversion.show.output_default

```{autodoc2-docstring} bumpversion.show.output_default
:parser: myst
```
````

````{py:function} output_yaml(value: dict) -> None
:canonical: bumpversion.show.output_yaml

```{autodoc2-docstring} bumpversion.show.output_yaml
:parser: myst
```
````

````{py:function} output_json(value: dict) -> None
:canonical: bumpversion.show.output_json

```{autodoc2-docstring} bumpversion.show.output_json
:parser: myst
```
````

````{py:data} OUTPUTTERS
:canonical: bumpversion.show.OUTPUTTERS
:value: >
   None

```{autodoc2-docstring} bumpversion.show.OUTPUTTERS
:parser: myst
```

````

````{py:function} resolve_name(obj: typing.Any, name: str, default: typing.Any = None, err_on_missing: bool = False) -> typing.Any
:canonical: bumpversion.show.resolve_name

```{autodoc2-docstring} bumpversion.show.resolve_name
:parser: myst
```
````

````{py:function} log_list(config: bumpversion.config.Config, version_part: typing.Optional[str], new_version: typing.Optional[str]) -> None
:canonical: bumpversion.show.log_list

```{autodoc2-docstring} bumpversion.show.log_list
:parser: myst
```
````

````{py:function} do_show(*args, config: bumpversion.config.Config, format_: str = 'default', increment: typing.Optional[str] = None) -> None
:canonical: bumpversion.show.do_show

```{autodoc2-docstring} bumpversion.show.do_show
:parser: myst
```
````
