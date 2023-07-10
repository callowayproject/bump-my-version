# {py:mod}`bumpversion.exceptions`

```{py:module} bumpversion.exceptions
```

```{autodoc2-docstring} bumpversion.exceptions
:allowtitles:
```

## Module Contents

### API

````{py:exception} BumpVersionError(message: str, ctx: typing.Optional[click.Context] = None)
:canonical: bumpversion.exceptions.BumpVersionError

Bases: {py:obj}`click.UsageError`

```{autodoc2-docstring} bumpversion.exceptions.BumpVersionError
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.exceptions.BumpVersionError.__init__
```

````

````{py:exception} FormattingError(message: str, ctx: typing.Optional[click.Context] = None)
:canonical: bumpversion.exceptions.FormattingError

Bases: {py:obj}`bumpversion.exceptions.BumpVersionError`

```{autodoc2-docstring} bumpversion.exceptions.FormattingError
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.exceptions.FormattingError.__init__
```

````

````{py:exception} MissingValueError(message: str, ctx: typing.Optional[click.Context] = None)
:canonical: bumpversion.exceptions.MissingValueError

Bases: {py:obj}`bumpversion.exceptions.BumpVersionError`

```{autodoc2-docstring} bumpversion.exceptions.MissingValueError
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.exceptions.MissingValueError.__init__
```

````

````{py:exception} DirtyWorkingDirectoryError(message: str, ctx: typing.Optional[click.Context] = None)
:canonical: bumpversion.exceptions.DirtyWorkingDirectoryError

Bases: {py:obj}`bumpversion.exceptions.BumpVersionError`

```{autodoc2-docstring} bumpversion.exceptions.DirtyWorkingDirectoryError
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.exceptions.DirtyWorkingDirectoryError.__init__
```

````

````{py:exception} SignedTagsError(message: str, ctx: typing.Optional[click.Context] = None)
:canonical: bumpversion.exceptions.SignedTagsError

Bases: {py:obj}`bumpversion.exceptions.BumpVersionError`

```{autodoc2-docstring} bumpversion.exceptions.SignedTagsError
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.exceptions.SignedTagsError.__init__
```

````

````{py:exception} VersionNotFoundError(message: str, ctx: typing.Optional[click.Context] = None)
:canonical: bumpversion.exceptions.VersionNotFoundError

Bases: {py:obj}`bumpversion.exceptions.BumpVersionError`

```{autodoc2-docstring} bumpversion.exceptions.VersionNotFoundError
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.exceptions.VersionNotFoundError.__init__
```

````

````{py:exception} InvalidVersionPartError(message: str, ctx: typing.Optional[click.Context] = None)
:canonical: bumpversion.exceptions.InvalidVersionPartError

Bases: {py:obj}`bumpversion.exceptions.BumpVersionError`

```{autodoc2-docstring} bumpversion.exceptions.InvalidVersionPartError
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.exceptions.InvalidVersionPartError.__init__
```

````

````{py:exception} ConfigurationError(message: str, ctx: typing.Optional[click.Context] = None)
:canonical: bumpversion.exceptions.ConfigurationError

Bases: {py:obj}`bumpversion.exceptions.BumpVersionError`

```{autodoc2-docstring} bumpversion.exceptions.ConfigurationError
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.exceptions.ConfigurationError.__init__
```

````

````{py:exception} BadInputError(message: str, ctx: typing.Optional[click.Context] = None)
:canonical: bumpversion.exceptions.BadInputError

Bases: {py:obj}`bumpversion.exceptions.BumpVersionError`

```{autodoc2-docstring} bumpversion.exceptions.BadInputError
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.exceptions.BadInputError.__init__
```

````
