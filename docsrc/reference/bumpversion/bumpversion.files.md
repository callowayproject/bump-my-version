# {py:mod}`bumpversion.files`

```{py:module} bumpversion.files
```

```{autodoc2-docstring} bumpversion.files
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`ConfiguredFile <bumpversion.files.ConfiguredFile>`
  - ```{autodoc2-docstring} bumpversion.files.ConfiguredFile
    :parser: myst
    :summary:
    ```
* - {py:obj}`FileUpdater <bumpversion.files.FileUpdater>`
  - ```{autodoc2-docstring} bumpversion.files.FileUpdater
    :parser: myst
    :summary:
    ```
* - {py:obj}`DataFileUpdater <bumpversion.files.DataFileUpdater>`
  - ```{autodoc2-docstring} bumpversion.files.DataFileUpdater
    :parser: myst
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`contains_pattern <bumpversion.files.contains_pattern>`
  - ```{autodoc2-docstring} bumpversion.files.contains_pattern
    :parser: myst
    :summary:
    ```
* - {py:obj}`log_changes <bumpversion.files.log_changes>`
  - ```{autodoc2-docstring} bumpversion.files.log_changes
    :parser: myst
    :summary:
    ```
* - {py:obj}`resolve_file_config <bumpversion.files.resolve_file_config>`
  - ```{autodoc2-docstring} bumpversion.files.resolve_file_config
    :parser: myst
    :summary:
    ```
* - {py:obj}`modify_files <bumpversion.files.modify_files>`
  - ```{autodoc2-docstring} bumpversion.files.modify_files
    :parser: myst
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`logger <bumpversion.files.logger>`
  - ```{autodoc2-docstring} bumpversion.files.logger
    :parser: myst
    :summary:
    ```
````

### API

````{py:data} logger
:canonical: bumpversion.files.logger
:value: >
   'get_indented_logger(...)'

```{autodoc2-docstring} bumpversion.files.logger
:parser: myst
```

````

````{py:function} contains_pattern(search: re.Pattern, contents: str) -> bool
:canonical: bumpversion.files.contains_pattern

```{autodoc2-docstring} bumpversion.files.contains_pattern
:parser: myst
```
````

````{py:function} log_changes(file_path: str, file_content_before: str, file_content_after: str, dry_run: bool = False) -> None
:canonical: bumpversion.files.log_changes

```{autodoc2-docstring} bumpversion.files.log_changes
:parser: myst
```
````

`````{py:class} ConfiguredFile(file_change: bumpversion.config.models.FileChange, version_config: bumpversion.version_part.VersionConfig, search: typing.Optional[str] = None, replace: typing.Optional[str] = None)
:canonical: bumpversion.files.ConfiguredFile

```{autodoc2-docstring} bumpversion.files.ConfiguredFile
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.files.ConfiguredFile.__init__
:parser: myst
```

````{py:method} get_file_contents() -> str
:canonical: bumpversion.files.ConfiguredFile.get_file_contents

```{autodoc2-docstring} bumpversion.files.ConfiguredFile.get_file_contents
:parser: myst
```

````

````{py:method} write_file_contents(contents: str) -> None
:canonical: bumpversion.files.ConfiguredFile.write_file_contents

```{autodoc2-docstring} bumpversion.files.ConfiguredFile.write_file_contents
:parser: myst
```

````

````{py:method} _contains_change_pattern(search_expression: re.Pattern, raw_search_expression: str, version: bumpversion.versioning.models.Version, context: typing.MutableMapping) -> bool
:canonical: bumpversion.files.ConfiguredFile._contains_change_pattern

```{autodoc2-docstring} bumpversion.files.ConfiguredFile._contains_change_pattern
:parser: myst
```

````

````{py:method} make_file_change(current_version: bumpversion.versioning.models.Version, new_version: bumpversion.versioning.models.Version, context: typing.MutableMapping, dry_run: bool = False) -> None
:canonical: bumpversion.files.ConfiguredFile.make_file_change

```{autodoc2-docstring} bumpversion.files.ConfiguredFile.make_file_change
:parser: myst
```

````

````{py:method} __str__() -> str
:canonical: bumpversion.files.ConfiguredFile.__str__

````

````{py:method} __repr__() -> str
:canonical: bumpversion.files.ConfiguredFile.__repr__

````

`````

````{py:function} resolve_file_config(files: typing.List[bumpversion.config.models.FileChange], version_config: bumpversion.version_part.VersionConfig, search: typing.Optional[str] = None, replace: typing.Optional[str] = None) -> typing.List[bumpversion.files.ConfiguredFile]
:canonical: bumpversion.files.resolve_file_config

```{autodoc2-docstring} bumpversion.files.resolve_file_config
:parser: myst
```
````

````{py:function} modify_files(files: typing.List[bumpversion.files.ConfiguredFile], current_version: bumpversion.versioning.models.Version, new_version: bumpversion.versioning.models.Version, context: typing.MutableMapping, dry_run: bool = False) -> None
:canonical: bumpversion.files.modify_files

```{autodoc2-docstring} bumpversion.files.modify_files
:parser: myst
```
````

`````{py:class} FileUpdater(file_change: bumpversion.config.models.FileChange, version_config: bumpversion.version_part.VersionConfig, search: typing.Optional[str] = None, replace: typing.Optional[str] = None)
:canonical: bumpversion.files.FileUpdater

```{autodoc2-docstring} bumpversion.files.FileUpdater
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.files.FileUpdater.__init__
:parser: myst
```

````{py:method} update_file(current_version: bumpversion.versioning.models.Version, new_version: bumpversion.versioning.models.Version, context: typing.MutableMapping, dry_run: bool = False) -> None
:canonical: bumpversion.files.FileUpdater.update_file

```{autodoc2-docstring} bumpversion.files.FileUpdater.update_file
:parser: myst
```

````

`````

`````{py:class} DataFileUpdater(file_change: bumpversion.config.models.FileChange, version_part_configs: typing.Dict[str, bumpversion.versioning.models.VersionComponentSpec])
:canonical: bumpversion.files.DataFileUpdater

```{autodoc2-docstring} bumpversion.files.DataFileUpdater
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.files.DataFileUpdater.__init__
:parser: myst
```

````{py:method} update_file(current_version: bumpversion.versioning.models.Version, new_version: bumpversion.versioning.models.Version, context: typing.MutableMapping, dry_run: bool = False) -> None
:canonical: bumpversion.files.DataFileUpdater.update_file

```{autodoc2-docstring} bumpversion.files.DataFileUpdater.update_file
:parser: myst
```

````

````{py:method} _update_toml_file(search_for: re.Pattern, raw_search_pattern: str, replace_with: str, dry_run: bool = False) -> None
:canonical: bumpversion.files.DataFileUpdater._update_toml_file

```{autodoc2-docstring} bumpversion.files.DataFileUpdater._update_toml_file
:parser: myst
```

````

`````
