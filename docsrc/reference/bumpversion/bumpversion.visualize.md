# {py:mod}`bumpversion.visualize`

```{py:module} bumpversion.visualize
```

```{autodoc2-docstring} bumpversion.visualize
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`Border <bumpversion.visualize.Border>`
  - ```{autodoc2-docstring} bumpversion.visualize.Border
    :parser: myst
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`lead_string <bumpversion.visualize.lead_string>`
  - ```{autodoc2-docstring} bumpversion.visualize.lead_string
    :parser: myst
    :summary:
    ```
* - {py:obj}`connection_str <bumpversion.visualize.connection_str>`
  - ```{autodoc2-docstring} bumpversion.visualize.connection_str
    :parser: myst
    :summary:
    ```
* - {py:obj}`labeled_line <bumpversion.visualize.labeled_line>`
  - ```{autodoc2-docstring} bumpversion.visualize.labeled_line
    :parser: myst
    :summary:
    ```
* - {py:obj}`filter_version_parts <bumpversion.visualize.filter_version_parts>`
  - ```{autodoc2-docstring} bumpversion.visualize.filter_version_parts
    :parser: myst
    :summary:
    ```
* - {py:obj}`visualize <bumpversion.visualize.visualize>`
  - ```{autodoc2-docstring} bumpversion.visualize.visualize
    :parser: myst
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`BOX_CHARS <bumpversion.visualize.BOX_CHARS>`
  - ```{autodoc2-docstring} bumpversion.visualize.BOX_CHARS
    :parser: myst
    :summary:
    ```
````

### API

````{py:data} BOX_CHARS
:canonical: bumpversion.visualize.BOX_CHARS
:value: >
   None

```{autodoc2-docstring} bumpversion.visualize.BOX_CHARS
:parser: myst
```

````

`````{py:class} Border
:canonical: bumpversion.visualize.Border

```{autodoc2-docstring} bumpversion.visualize.Border
:parser: myst
```

````{py:attribute} corner_bottom_right
:canonical: bumpversion.visualize.Border.corner_bottom_right
:type: str
:value: >
   None

```{autodoc2-docstring} bumpversion.visualize.Border.corner_bottom_right
:parser: myst
```

````

````{py:attribute} corner_top_right
:canonical: bumpversion.visualize.Border.corner_top_right
:type: str
:value: >
   None

```{autodoc2-docstring} bumpversion.visualize.Border.corner_top_right
:parser: myst
```

````

````{py:attribute} corner_top_left
:canonical: bumpversion.visualize.Border.corner_top_left
:type: str
:value: >
   None

```{autodoc2-docstring} bumpversion.visualize.Border.corner_top_left
:parser: myst
```

````

````{py:attribute} corner_bottom_left
:canonical: bumpversion.visualize.Border.corner_bottom_left
:type: str
:value: >
   None

```{autodoc2-docstring} bumpversion.visualize.Border.corner_bottom_left
:parser: myst
```

````

````{py:attribute} divider_left
:canonical: bumpversion.visualize.Border.divider_left
:type: str
:value: >
   None

```{autodoc2-docstring} bumpversion.visualize.Border.divider_left
:parser: myst
```

````

````{py:attribute} divider_up
:canonical: bumpversion.visualize.Border.divider_up
:type: str
:value: >
   None

```{autodoc2-docstring} bumpversion.visualize.Border.divider_up
:parser: myst
```

````

````{py:attribute} divider_down
:canonical: bumpversion.visualize.Border.divider_down
:type: str
:value: >
   None

```{autodoc2-docstring} bumpversion.visualize.Border.divider_down
:parser: myst
```

````

````{py:attribute} divider_right
:canonical: bumpversion.visualize.Border.divider_right
:type: str
:value: >
   None

```{autodoc2-docstring} bumpversion.visualize.Border.divider_right
:parser: myst
```

````

````{py:attribute} line
:canonical: bumpversion.visualize.Border.line
:type: str
:value: >
   None

```{autodoc2-docstring} bumpversion.visualize.Border.line
:parser: myst
```

````

````{py:attribute} pipe
:canonical: bumpversion.visualize.Border.pipe
:type: str
:value: >
   None

```{autodoc2-docstring} bumpversion.visualize.Border.pipe
:parser: myst
```

````

````{py:attribute} cross
:canonical: bumpversion.visualize.Border.cross
:type: str
:value: >
   None

```{autodoc2-docstring} bumpversion.visualize.Border.cross
:parser: myst
```

````

`````

````{py:function} lead_string(version_str: str, border: bumpversion.visualize.Border, blank: bool = False) -> str
:canonical: bumpversion.visualize.lead_string

```{autodoc2-docstring} bumpversion.visualize.lead_string
:parser: myst
```
````

````{py:function} connection_str(border: bumpversion.visualize.Border, has_next: bool = False, has_previous: bool = False) -> str
:canonical: bumpversion.visualize.connection_str

```{autodoc2-docstring} bumpversion.visualize.connection_str
:parser: myst
```
````

````{py:function} labeled_line(label: str, border: bumpversion.visualize.Border, fit_length: typing.Optional[int] = None) -> str
:canonical: bumpversion.visualize.labeled_line

```{autodoc2-docstring} bumpversion.visualize.labeled_line
:parser: myst
```
````

````{py:function} filter_version_parts(config: bumpversion.config.Config) -> typing.List[str]
:canonical: bumpversion.visualize.filter_version_parts

```{autodoc2-docstring} bumpversion.visualize.filter_version_parts
:parser: myst
```
````

````{py:function} visualize(config: bumpversion.config.Config, version_str: str, box_style: str = 'light') -> None
:canonical: bumpversion.visualize.visualize

```{autodoc2-docstring} bumpversion.visualize.visualize
:parser: myst
```
````
