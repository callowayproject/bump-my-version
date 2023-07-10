# {py:mod}`bumpversion.bump`

```{py:module} bumpversion.bump
```

```{autodoc2-docstring} bumpversion.bump
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`get_next_version <bumpversion.bump.get_next_version>`
  - ```{autodoc2-docstring} bumpversion.bump.get_next_version
    :summary:
    ```
* - {py:obj}`do_bump <bumpversion.bump.do_bump>`
  - ```{autodoc2-docstring} bumpversion.bump.do_bump
    :summary:
    ```
* - {py:obj}`commit_and_tag <bumpversion.bump.commit_and_tag>`
  - ```{autodoc2-docstring} bumpversion.bump.commit_and_tag
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`logger <bumpversion.bump.logger>`
  - ```{autodoc2-docstring} bumpversion.bump.logger
    :summary:
    ```
````

### API

````{py:data} logger
:canonical: bumpversion.bump.logger
:value: >
   None

```{autodoc2-docstring} bumpversion.bump.logger
```

````

````{py:function} get_next_version(current_version: bumpversion.version_part.Version, config: bumpversion.config.Config, version_part: typing.Optional[str], new_version: typing.Optional[str]) -> bumpversion.version_part.Version
:canonical: bumpversion.bump.get_next_version

```{autodoc2-docstring} bumpversion.bump.get_next_version
```
````

````{py:function} do_bump(version_part: typing.Optional[str], new_version: typing.Optional[str], config: bumpversion.config.Config, config_file: typing.Optional[pathlib.Path] = None, dry_run: bool = False) -> None
:canonical: bumpversion.bump.do_bump

```{autodoc2-docstring} bumpversion.bump.do_bump
```
````

````{py:function} commit_and_tag(config: bumpversion.config.Config, config_file: typing.Optional[pathlib.Path], configured_files: typing.List[bumpversion.files.ConfiguredFile], ctx: typing.ChainMap, dry_run: bool = False) -> None
:canonical: bumpversion.bump.commit_and_tag

```{autodoc2-docstring} bumpversion.bump.commit_and_tag
```
````
