# {py:mod}`bumpversion.yaml_dump`

```{py:module} bumpversion.yaml_dump
```

```{autodoc2-docstring} bumpversion.yaml_dump
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`YAMLDumpers <bumpversion.yaml_dump.YAMLDumpers>`
  - ```{autodoc2-docstring} bumpversion.yaml_dump.YAMLDumpers
    :parser: myst
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`dump <bumpversion.yaml_dump.dump>`
  - ```{autodoc2-docstring} bumpversion.yaml_dump.dump
    :parser: myst
    :summary:
    ```
* - {py:obj}`format_str <bumpversion.yaml_dump.format_str>`
  - ```{autodoc2-docstring} bumpversion.yaml_dump.format_str
    :parser: myst
    :summary:
    ```
* - {py:obj}`format_int <bumpversion.yaml_dump.format_int>`
  - ```{autodoc2-docstring} bumpversion.yaml_dump.format_int
    :parser: myst
    :summary:
    ```
* - {py:obj}`format_float <bumpversion.yaml_dump.format_float>`
  - ```{autodoc2-docstring} bumpversion.yaml_dump.format_float
    :parser: myst
    :summary:
    ```
* - {py:obj}`format_bool <bumpversion.yaml_dump.format_bool>`
  - ```{autodoc2-docstring} bumpversion.yaml_dump.format_bool
    :parser: myst
    :summary:
    ```
* - {py:obj}`format_dict <bumpversion.yaml_dump.format_dict>`
  - ```{autodoc2-docstring} bumpversion.yaml_dump.format_dict
    :parser: myst
    :summary:
    ```
* - {py:obj}`format_sequence <bumpversion.yaml_dump.format_sequence>`
  - ```{autodoc2-docstring} bumpversion.yaml_dump.format_sequence
    :parser: myst
    :summary:
    ```
* - {py:obj}`format_none <bumpversion.yaml_dump.format_none>`
  - ```{autodoc2-docstring} bumpversion.yaml_dump.format_none
    :parser: myst
    :summary:
    ```
* - {py:obj}`format_date <bumpversion.yaml_dump.format_date>`
  - ```{autodoc2-docstring} bumpversion.yaml_dump.format_date
    :parser: myst
    :summary:
    ```
* - {py:obj}`format_datetime <bumpversion.yaml_dump.format_datetime>`
  - ```{autodoc2-docstring} bumpversion.yaml_dump.format_datetime
    :parser: myst
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`DumperFunc <bumpversion.yaml_dump.DumperFunc>`
  - ```{autodoc2-docstring} bumpversion.yaml_dump.DumperFunc
    :parser: myst
    :summary:
    ```
* - {py:obj}`YAML_DUMPERS <bumpversion.yaml_dump.YAML_DUMPERS>`
  - ```{autodoc2-docstring} bumpversion.yaml_dump.YAML_DUMPERS
    :parser: myst
    :summary:
    ```
* - {py:obj}`INDENT <bumpversion.yaml_dump.INDENT>`
  - ```{autodoc2-docstring} bumpversion.yaml_dump.INDENT
    :parser: myst
    :summary:
    ```
````

### API

````{py:data} DumperFunc
:canonical: bumpversion.yaml_dump.DumperFunc
:value: >
   None

```{autodoc2-docstring} bumpversion.yaml_dump.DumperFunc
:parser: myst
```

````

`````{py:class} YAMLDumpers(dict=None, /, **kwargs)
:canonical: bumpversion.yaml_dump.YAMLDumpers

Bases: {py:obj}`collections.UserDict`

```{autodoc2-docstring} bumpversion.yaml_dump.YAMLDumpers
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.yaml_dump.YAMLDumpers.__init__
:parser: myst
```

````{py:method} add_dumper(data_type: type, dumper: bumpversion.yaml_dump.DumperFunc) -> None
:canonical: bumpversion.yaml_dump.YAMLDumpers.add_dumper

```{autodoc2-docstring} bumpversion.yaml_dump.YAMLDumpers.add_dumper
:parser: myst
```

````

`````

````{py:data} YAML_DUMPERS
:canonical: bumpversion.yaml_dump.YAML_DUMPERS
:value: >
   'YAMLDumpers(...)'

```{autodoc2-docstring} bumpversion.yaml_dump.YAML_DUMPERS
:parser: myst
```

````

````{py:data} INDENT
:canonical: bumpversion.yaml_dump.INDENT
:value: >
   '  '

```{autodoc2-docstring} bumpversion.yaml_dump.INDENT
:parser: myst
```

````

````{py:function} dump(data: typing.Any) -> str
:canonical: bumpversion.yaml_dump.dump

```{autodoc2-docstring} bumpversion.yaml_dump.dump
:parser: myst
```
````

````{py:function} format_str(val: str) -> str
:canonical: bumpversion.yaml_dump.format_str

```{autodoc2-docstring} bumpversion.yaml_dump.format_str
:parser: myst
```
````

````{py:function} format_int(val: int) -> str
:canonical: bumpversion.yaml_dump.format_int

```{autodoc2-docstring} bumpversion.yaml_dump.format_int
:parser: myst
```
````

````{py:function} format_float(data: float) -> str
:canonical: bumpversion.yaml_dump.format_float

```{autodoc2-docstring} bumpversion.yaml_dump.format_float
:parser: myst
```
````

````{py:function} format_bool(val: bool) -> str
:canonical: bumpversion.yaml_dump.format_bool

```{autodoc2-docstring} bumpversion.yaml_dump.format_bool
:parser: myst
```
````

````{py:function} format_dict(val: dict) -> str
:canonical: bumpversion.yaml_dump.format_dict

```{autodoc2-docstring} bumpversion.yaml_dump.format_dict
:parser: myst
```
````

````{py:function} format_sequence(val: typing.Union[list, tuple]) -> str
:canonical: bumpversion.yaml_dump.format_sequence

```{autodoc2-docstring} bumpversion.yaml_dump.format_sequence
:parser: myst
```
````

````{py:function} format_none(_: None) -> str
:canonical: bumpversion.yaml_dump.format_none

```{autodoc2-docstring} bumpversion.yaml_dump.format_none
:parser: myst
```
````

````{py:function} format_date(val: datetime.date) -> str
:canonical: bumpversion.yaml_dump.format_date

```{autodoc2-docstring} bumpversion.yaml_dump.format_date
:parser: myst
```
````

````{py:function} format_datetime(val: datetime.datetime) -> str
:canonical: bumpversion.yaml_dump.format_datetime

```{autodoc2-docstring} bumpversion.yaml_dump.format_datetime
:parser: myst
```
````
