# {py:mod}`bumpversion.yaml_dump`

```{py:module} bumpversion.yaml_dump
```

```{autodoc2-docstring} bumpversion.yaml_dump
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`YAMLDumpers <bumpversion.yaml_dump.YAMLDumpers>`
  - ```{autodoc2-docstring} bumpversion.yaml_dump.YAMLDumpers
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`dump <bumpversion.yaml_dump.dump>`
  - ```{autodoc2-docstring} bumpversion.yaml_dump.dump
    :summary:
    ```
* - {py:obj}`format_str <bumpversion.yaml_dump.format_str>`
  - ```{autodoc2-docstring} bumpversion.yaml_dump.format_str
    :summary:
    ```
* - {py:obj}`format_int <bumpversion.yaml_dump.format_int>`
  - ```{autodoc2-docstring} bumpversion.yaml_dump.format_int
    :summary:
    ```
* - {py:obj}`format_float <bumpversion.yaml_dump.format_float>`
  - ```{autodoc2-docstring} bumpversion.yaml_dump.format_float
    :summary:
    ```
* - {py:obj}`format_bool <bumpversion.yaml_dump.format_bool>`
  - ```{autodoc2-docstring} bumpversion.yaml_dump.format_bool
    :summary:
    ```
* - {py:obj}`format_dict <bumpversion.yaml_dump.format_dict>`
  - ```{autodoc2-docstring} bumpversion.yaml_dump.format_dict
    :summary:
    ```
* - {py:obj}`format_list <bumpversion.yaml_dump.format_list>`
  - ```{autodoc2-docstring} bumpversion.yaml_dump.format_list
    :summary:
    ```
* - {py:obj}`format_none <bumpversion.yaml_dump.format_none>`
  - ```{autodoc2-docstring} bumpversion.yaml_dump.format_none
    :summary:
    ```
* - {py:obj}`format_date <bumpversion.yaml_dump.format_date>`
  - ```{autodoc2-docstring} bumpversion.yaml_dump.format_date
    :summary:
    ```
* - {py:obj}`format_datetime <bumpversion.yaml_dump.format_datetime>`
  - ```{autodoc2-docstring} bumpversion.yaml_dump.format_datetime
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`DumperFunc <bumpversion.yaml_dump.DumperFunc>`
  - ```{autodoc2-docstring} bumpversion.yaml_dump.DumperFunc
    :summary:
    ```
* - {py:obj}`YAML_DUMPERS <bumpversion.yaml_dump.YAML_DUMPERS>`
  - ```{autodoc2-docstring} bumpversion.yaml_dump.YAML_DUMPERS
    :summary:
    ```
* - {py:obj}`INDENT <bumpversion.yaml_dump.INDENT>`
  - ```{autodoc2-docstring} bumpversion.yaml_dump.INDENT
    :summary:
    ```
````

### API

````{py:data} DumperFunc
:canonical: bumpversion.yaml_dump.DumperFunc
:value: >
   None

```{autodoc2-docstring} bumpversion.yaml_dump.DumperFunc
```

````

`````{py:class} YAMLDumpers(dict=None, /, **kwargs)
:canonical: bumpversion.yaml_dump.YAMLDumpers

Bases: {py:obj}`collections.UserDict`

```{autodoc2-docstring} bumpversion.yaml_dump.YAMLDumpers
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.yaml_dump.YAMLDumpers.__init__
```

````{py:method} add_dumper(data_type: type, dumper: bumpversion.yaml_dump.DumperFunc) -> None
:canonical: bumpversion.yaml_dump.YAMLDumpers.add_dumper

```{autodoc2-docstring} bumpversion.yaml_dump.YAMLDumpers.add_dumper
```

````

`````

````{py:data} YAML_DUMPERS
:canonical: bumpversion.yaml_dump.YAML_DUMPERS
:value: >
   None

```{autodoc2-docstring} bumpversion.yaml_dump.YAML_DUMPERS
```

````

````{py:data} INDENT
:canonical: bumpversion.yaml_dump.INDENT
:value: >
   '  '

```{autodoc2-docstring} bumpversion.yaml_dump.INDENT
```

````

````{py:function} dump(data: typing.Any) -> str
:canonical: bumpversion.yaml_dump.dump

```{autodoc2-docstring} bumpversion.yaml_dump.dump
```
````

````{py:function} format_str(val: str) -> str
:canonical: bumpversion.yaml_dump.format_str

```{autodoc2-docstring} bumpversion.yaml_dump.format_str
```
````

````{py:function} format_int(val: int) -> str
:canonical: bumpversion.yaml_dump.format_int

```{autodoc2-docstring} bumpversion.yaml_dump.format_int
```
````

````{py:function} format_float(data: float) -> str
:canonical: bumpversion.yaml_dump.format_float

```{autodoc2-docstring} bumpversion.yaml_dump.format_float
```
````

````{py:function} format_bool(val: bool) -> str
:canonical: bumpversion.yaml_dump.format_bool

```{autodoc2-docstring} bumpversion.yaml_dump.format_bool
```
````

````{py:function} format_dict(val: dict) -> str
:canonical: bumpversion.yaml_dump.format_dict

```{autodoc2-docstring} bumpversion.yaml_dump.format_dict
```
````

````{py:function} format_list(val: list) -> str
:canonical: bumpversion.yaml_dump.format_list

```{autodoc2-docstring} bumpversion.yaml_dump.format_list
```
````

````{py:function} format_none(_: None) -> str
:canonical: bumpversion.yaml_dump.format_none

```{autodoc2-docstring} bumpversion.yaml_dump.format_none
```
````

````{py:function} format_date(val: datetime.date) -> str
:canonical: bumpversion.yaml_dump.format_date

```{autodoc2-docstring} bumpversion.yaml_dump.format_date
```
````

````{py:function} format_datetime(val: datetime.datetime) -> str
:canonical: bumpversion.yaml_dump.format_datetime

```{autodoc2-docstring} bumpversion.yaml_dump.format_datetime
```
````
