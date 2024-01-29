# {py:mod}`bumpversion.versioning.functions`

```{py:module} bumpversion.versioning.functions
```

```{autodoc2-docstring} bumpversion.versioning.functions
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`PartFunction <bumpversion.versioning.functions.PartFunction>`
  - ```{autodoc2-docstring} bumpversion.versioning.functions.PartFunction
    :parser: myst
    :summary:
    ```
* - {py:obj}`IndependentFunction <bumpversion.versioning.functions.IndependentFunction>`
  - ```{autodoc2-docstring} bumpversion.versioning.functions.IndependentFunction
    :parser: myst
    :summary:
    ```
* - {py:obj}`NumericFunction <bumpversion.versioning.functions.NumericFunction>`
  - ```{autodoc2-docstring} bumpversion.versioning.functions.NumericFunction
    :parser: myst
    :summary:
    ```
* - {py:obj}`ValuesFunction <bumpversion.versioning.functions.ValuesFunction>`
  - ```{autodoc2-docstring} bumpversion.versioning.functions.ValuesFunction
    :parser: myst
    :summary:
    ```
````

### API

`````{py:class} PartFunction
:canonical: bumpversion.versioning.functions.PartFunction

```{autodoc2-docstring} bumpversion.versioning.functions.PartFunction
:parser: myst
```

````{py:attribute} first_value
:canonical: bumpversion.versioning.functions.PartFunction.first_value
:type: str
:value: >
   None

```{autodoc2-docstring} bumpversion.versioning.functions.PartFunction.first_value
:parser: myst
```

````

````{py:attribute} optional_value
:canonical: bumpversion.versioning.functions.PartFunction.optional_value
:type: str
:value: >
   None

```{autodoc2-docstring} bumpversion.versioning.functions.PartFunction.optional_value
:parser: myst
```

````

````{py:attribute} independent
:canonical: bumpversion.versioning.functions.PartFunction.independent
:type: bool
:value: >
   None

```{autodoc2-docstring} bumpversion.versioning.functions.PartFunction.independent
:parser: myst
```

````

````{py:method} bump(value: str) -> str
:canonical: bumpversion.versioning.functions.PartFunction.bump
:abstractmethod:

```{autodoc2-docstring} bumpversion.versioning.functions.PartFunction.bump
:parser: myst
```

````

`````

`````{py:class} IndependentFunction(value: typing.Union[str, int, None] = None)
:canonical: bumpversion.versioning.functions.IndependentFunction

Bases: {py:obj}`bumpversion.versioning.functions.PartFunction`

```{autodoc2-docstring} bumpversion.versioning.functions.IndependentFunction
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.versioning.functions.IndependentFunction.__init__
:parser: myst
```

````{py:method} bump(value: typing.Optional[str] = None) -> str
:canonical: bumpversion.versioning.functions.IndependentFunction.bump

```{autodoc2-docstring} bumpversion.versioning.functions.IndependentFunction.bump
:parser: myst
```

````

`````

`````{py:class} NumericFunction(optional_value: typing.Union[str, int, None] = None, first_value: typing.Union[str, int, None] = None)
:canonical: bumpversion.versioning.functions.NumericFunction

Bases: {py:obj}`bumpversion.versioning.functions.PartFunction`

```{autodoc2-docstring} bumpversion.versioning.functions.NumericFunction
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.versioning.functions.NumericFunction.__init__
:parser: myst
```

````{py:attribute} FIRST_NUMERIC
:canonical: bumpversion.versioning.functions.NumericFunction.FIRST_NUMERIC
:value: >
   'compile(...)'

```{autodoc2-docstring} bumpversion.versioning.functions.NumericFunction.FIRST_NUMERIC
:parser: myst
```

````

````{py:method} bump(value: typing.Union[str, int]) -> str
:canonical: bumpversion.versioning.functions.NumericFunction.bump

```{autodoc2-docstring} bumpversion.versioning.functions.NumericFunction.bump
:parser: myst
```

````

`````

`````{py:class} ValuesFunction(values: typing.List[str], optional_value: typing.Optional[str] = None, first_value: typing.Optional[str] = None)
:canonical: bumpversion.versioning.functions.ValuesFunction

Bases: {py:obj}`bumpversion.versioning.functions.PartFunction`

```{autodoc2-docstring} bumpversion.versioning.functions.ValuesFunction
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.versioning.functions.ValuesFunction.__init__
:parser: myst
```

````{py:method} bump(value: str) -> str
:canonical: bumpversion.versioning.functions.ValuesFunction.bump

```{autodoc2-docstring} bumpversion.versioning.functions.ValuesFunction.bump
:parser: myst
```

````

`````
