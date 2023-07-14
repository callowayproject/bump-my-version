# {py:mod}`bumpversion.files`

```{py:module} bumpversion.files
```

```{autodoc2-docstring} bumpversion.files
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`ConfiguredFile <bumpversion.files.ConfiguredFile>`
  - ```{autodoc2-docstring} bumpversion.files.ConfiguredFile
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`resolve_file_config <bumpversion.files.resolve_file_config>`
  - ```{autodoc2-docstring} bumpversion.files.resolve_file_config
    :summary:
    ```
* - {py:obj}`modify_files <bumpversion.files.modify_files>`
  - ```{autodoc2-docstring} bumpversion.files.modify_files
    :summary:
    ```
* - {py:obj}`get_glob_files <bumpversion.files.get_glob_files>`
  - ```{autodoc2-docstring} bumpversion.files.get_glob_files
    :summary:
    ```
* - {py:obj}`_check_files_contain_version <bumpversion.files._check_files_contain_version>`
  - ```{autodoc2-docstring} bumpversion.files._check_files_contain_version
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`logger <bumpversion.files.logger>`
  - ```{autodoc2-docstring} bumpversion.files.logger
    :summary:
    ```
````

### API

````{py:data} logger
:canonical: bumpversion.files.logger
:value: >
   None

```{autodoc2-docstring} bumpversion.files.logger
```

````

`````{py:class} ConfiguredFile(file_cfg: bumpversion.config.FileConfig, version_config: bumpversion.version_part.VersionConfig, search: typing.Optional[str] = None, replace: typing.Optional[str] = None)
:canonical: bumpversion.files.ConfiguredFile

```{autodoc2-docstring} bumpversion.files.ConfiguredFile
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.files.ConfiguredFile.__init__
```

````{py:method} contains_version(version: bumpversion.version_part.Version, context: typing.MutableMapping) -> bool
:canonical: bumpversion.files.ConfiguredFile.contains_version

```{autodoc2-docstring} bumpversion.files.ConfiguredFile.contains_version
```

````

````{py:method} contains(search: str) -> bool
:canonical: bumpversion.files.ConfiguredFile.contains

```{autodoc2-docstring} bumpversion.files.ConfiguredFile.contains
```

````

````{py:method} replace_version(current_version: bumpversion.version_part.Version, new_version: bumpversion.version_part.Version, context: typing.MutableMapping, dry_run: bool = False) -> None
:canonical: bumpversion.files.ConfiguredFile.replace_version

```{autodoc2-docstring} bumpversion.files.ConfiguredFile.replace_version
```

````

````{py:method} __str__() -> str
:canonical: bumpversion.files.ConfiguredFile.__str__

````

````{py:method} __repr__() -> str
:canonical: bumpversion.files.ConfiguredFile.__repr__

````

`````

````{py:function} resolve_file_config(files: typing.List[bumpversion.config.FileConfig], version_config: bumpversion.version_part.VersionConfig, search: typing.Optional[str] = None, replace: typing.Optional[str] = None) -> typing.List[bumpversion.files.ConfiguredFile]
:canonical: bumpversion.files.resolve_file_config

```{autodoc2-docstring} bumpversion.files.resolve_file_config
```
````

````{py:function} modify_files(files: typing.List[bumpversion.files.ConfiguredFile], current_version: bumpversion.version_part.Version, new_version: bumpversion.version_part.Version, context: typing.MutableMapping, dry_run: bool = False) -> None
:canonical: bumpversion.files.modify_files

```{autodoc2-docstring} bumpversion.files.modify_files
```
````

````{py:function} get_glob_files(file_cfg: bumpversion.config.FileConfig, version_config: bumpversion.version_part.VersionConfig, search: typing.Optional[str] = None, replace: typing.Optional[str] = None) -> typing.List[bumpversion.files.ConfiguredFile]
:canonical: bumpversion.files.get_glob_files

```{autodoc2-docstring} bumpversion.files.get_glob_files
```
````

````{py:function} _check_files_contain_version(files: typing.List[bumpversion.files.ConfiguredFile], current_version: bumpversion.version_part.Version, context: typing.MutableMapping) -> None
:canonical: bumpversion.files._check_files_contain_version

```{autodoc2-docstring} bumpversion.files._check_files_contain_version
```
````
