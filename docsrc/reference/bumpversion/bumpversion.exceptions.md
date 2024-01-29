# {py:mod}`bumpversion.exceptions`

```{py:module} bumpversion.exceptions
```

```{autodoc2-docstring} bumpversion.exceptions
:parser: myst
:allowtitles:
```

## Module Contents

### API

````{py:exception} BumpVersionError(message: str, ctx: typing.Optional[click.Context] = None)
:canonical: bumpversion.exceptions.BumpVersionError

Bases: {py:obj}`click.UsageError`

```{autodoc2-docstring} bumpversion.exceptions.BumpVersionError
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.exceptions.BumpVersionError.__init__
:parser: myst
```

````

````{py:exception} FormattingError(message: str, ctx: typing.Optional[click.Context] = None)
:canonical: bumpversion.exceptions.FormattingError

Bases: {py:obj}`bumpversion.exceptions.BumpVersionError`

```{autodoc2-docstring} bumpversion.exceptions.FormattingError
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.exceptions.FormattingError.__init__
:parser: myst
```

````

````{py:exception} MissingValueError(message: str, ctx: typing.Optional[click.Context] = None)
:canonical: bumpversion.exceptions.MissingValueError

Bases: {py:obj}`bumpversion.exceptions.BumpVersionError`

```{autodoc2-docstring} bumpversion.exceptions.MissingValueError
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.exceptions.MissingValueError.__init__
:parser: myst
```

````

````{py:exception} DirtyWorkingDirectoryError(message: str, ctx: typing.Optional[click.Context] = None)
:canonical: bumpversion.exceptions.DirtyWorkingDirectoryError

Bases: {py:obj}`bumpversion.exceptions.BumpVersionError`

```{autodoc2-docstring} bumpversion.exceptions.DirtyWorkingDirectoryError
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.exceptions.DirtyWorkingDirectoryError.__init__
:parser: myst
```

````

````{py:exception} SignedTagsError(message: str, ctx: typing.Optional[click.Context] = None)
:canonical: bumpversion.exceptions.SignedTagsError

Bases: {py:obj}`bumpversion.exceptions.BumpVersionError`

```{autodoc2-docstring} bumpversion.exceptions.SignedTagsError
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.exceptions.SignedTagsError.__init__
:parser: myst
```

````

````{py:exception} VersionNotFoundError(message: str, ctx: typing.Optional[click.Context] = None)
:canonical: bumpversion.exceptions.VersionNotFoundError

Bases: {py:obj}`bumpversion.exceptions.BumpVersionError`

```{autodoc2-docstring} bumpversion.exceptions.VersionNotFoundError
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.exceptions.VersionNotFoundError.__init__
:parser: myst
```

````

````{py:exception} InvalidVersionPartError(message: str, ctx: typing.Optional[click.Context] = None)
:canonical: bumpversion.exceptions.InvalidVersionPartError

Bases: {py:obj}`bumpversion.exceptions.BumpVersionError`

```{autodoc2-docstring} bumpversion.exceptions.InvalidVersionPartError
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.exceptions.InvalidVersionPartError.__init__
:parser: myst
```

````

````{py:exception} ConfigurationError(message: str, ctx: typing.Optional[click.Context] = None)
:canonical: bumpversion.exceptions.ConfigurationError

Bases: {py:obj}`bumpversion.exceptions.BumpVersionError`

```{autodoc2-docstring} bumpversion.exceptions.ConfigurationError
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.exceptions.ConfigurationError.__init__
:parser: myst
```

````

````{py:exception} BadInputError(message: str, ctx: typing.Optional[click.Context] = None)
:canonical: bumpversion.exceptions.BadInputError

Bases: {py:obj}`bumpversion.exceptions.BumpVersionError`

```{autodoc2-docstring} bumpversion.exceptions.BadInputError
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.exceptions.BadInputError.__init__
:parser: myst
```

````
