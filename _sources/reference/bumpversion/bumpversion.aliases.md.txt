# {py:mod}`bumpversion.aliases`

```{py:module} bumpversion.aliases
```

```{autodoc2-docstring} bumpversion.aliases
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`AliasedGroup <bumpversion.aliases.AliasedGroup>`
  - ```{autodoc2-docstring} bumpversion.aliases.AliasedGroup
    :summary:
    ```
````

### API

`````{py:class} AliasedGroup(name: typing.Optional[str] = None, commands: typing.Optional[typing.Union[typing.Dict[str, click.core.Command], typing.Sequence[click.core.Command]]] = None, **attrs: typing.Any)
:canonical: bumpversion.aliases.AliasedGroup

Bases: {py:obj}`rich_click.rich_group.RichGroup`

```{autodoc2-docstring} bumpversion.aliases.AliasedGroup
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.aliases.AliasedGroup.__init__
```

````{py:method} get_command(ctx: click.Context, cmd_name: str) -> typing.Optional[rich_click.Command]
:canonical: bumpversion.aliases.AliasedGroup.get_command

```{autodoc2-docstring} bumpversion.aliases.AliasedGroup.get_command
```

````

````{py:method} resolve_command(ctx: click.Context, args: typing.List[str]) -> tuple
:canonical: bumpversion.aliases.AliasedGroup.resolve_command

```{autodoc2-docstring} bumpversion.aliases.AliasedGroup.resolve_command
```

````

`````
