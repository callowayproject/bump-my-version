# {py:mod}`bumpversion.indented_logger`

```{py:module} bumpversion.indented_logger
```

```{autodoc2-docstring} bumpversion.indented_logger
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`IndentedLoggerAdapter <bumpversion.indented_logger.IndentedLoggerAdapter>`
  - ```{autodoc2-docstring} bumpversion.indented_logger.IndentedLoggerAdapter
    :parser: myst
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`CURRENT_INDENT <bumpversion.indented_logger.CURRENT_INDENT>`
  - ```{autodoc2-docstring} bumpversion.indented_logger.CURRENT_INDENT
    :parser: myst
    :summary:
    ```
````

### API

````{py:data} CURRENT_INDENT
:canonical: bumpversion.indented_logger.CURRENT_INDENT
:value: >
   'ContextVar(...)'

```{autodoc2-docstring} bumpversion.indented_logger.CURRENT_INDENT
:parser: myst
```

````

`````{py:class} IndentedLoggerAdapter(logger: logging.Logger, extra: typing.Optional[dict] = None, depth: int = 2, indent_char: str = ' ', reset: bool = False)
:canonical: bumpversion.indented_logger.IndentedLoggerAdapter

Bases: {py:obj}`logging.LoggerAdapter`

```{autodoc2-docstring} bumpversion.indented_logger.IndentedLoggerAdapter
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.indented_logger.IndentedLoggerAdapter.__init__
:parser: myst
```

````{py:property} current_indent
:canonical: bumpversion.indented_logger.IndentedLoggerAdapter.current_indent
:type: int

```{autodoc2-docstring} bumpversion.indented_logger.IndentedLoggerAdapter.current_indent
:parser: myst
```

````

````{py:method} indent(amount: int = 1) -> None
:canonical: bumpversion.indented_logger.IndentedLoggerAdapter.indent

```{autodoc2-docstring} bumpversion.indented_logger.IndentedLoggerAdapter.indent
:parser: myst
```

````

````{py:method} dedent(amount: int = 1) -> None
:canonical: bumpversion.indented_logger.IndentedLoggerAdapter.dedent

```{autodoc2-docstring} bumpversion.indented_logger.IndentedLoggerAdapter.dedent
:parser: myst
```

````

````{py:method} reset() -> None
:canonical: bumpversion.indented_logger.IndentedLoggerAdapter.reset

```{autodoc2-docstring} bumpversion.indented_logger.IndentedLoggerAdapter.reset
:parser: myst
```

````

````{py:property} indent_str
:canonical: bumpversion.indented_logger.IndentedLoggerAdapter.indent_str
:type: str

```{autodoc2-docstring} bumpversion.indented_logger.IndentedLoggerAdapter.indent_str
:parser: myst
```

````

````{py:method} process(msg: str, kwargs: typing.Optional[typing.MutableMapping[str, typing.Any]]) -> typing.Tuple[str, typing.MutableMapping[str, typing.Any]]
:canonical: bumpversion.indented_logger.IndentedLoggerAdapter.process

```{autodoc2-docstring} bumpversion.indented_logger.IndentedLoggerAdapter.process
:parser: myst
```

````

`````
