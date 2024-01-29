# {py:mod}`bumpversion.config.files_legacy`

```{py:module} bumpversion.config.files_legacy
```

```{autodoc2-docstring} bumpversion.config.files_legacy
:parser: myst
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`read_ini_file <bumpversion.config.files_legacy.read_ini_file>`
  - ```{autodoc2-docstring} bumpversion.config.files_legacy.read_ini_file
    :parser: myst
    :summary:
    ```
* - {py:obj}`update_ini_config_file <bumpversion.config.files_legacy.update_ini_config_file>`
  - ```{autodoc2-docstring} bumpversion.config.files_legacy.update_ini_config_file
    :parser: myst
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`logger <bumpversion.config.files_legacy.logger>`
  - ```{autodoc2-docstring} bumpversion.config.files_legacy.logger
    :parser: myst
    :summary:
    ```
````

### API

````{py:data} logger
:canonical: bumpversion.config.files_legacy.logger
:value: >
   'get_indented_logger(...)'

```{autodoc2-docstring} bumpversion.config.files_legacy.logger
:parser: myst
```

````

````{py:function} read_ini_file(file_path: pathlib.Path) -> typing.Dict[str, typing.Any]
:canonical: bumpversion.config.files_legacy.read_ini_file

```{autodoc2-docstring} bumpversion.config.files_legacy.read_ini_file
:parser: myst
```
````

````{py:function} update_ini_config_file(config_file: typing.Union[str, pathlib.Path], current_version: str, new_version: str, dry_run: bool = False) -> None
:canonical: bumpversion.config.files_legacy.update_ini_config_file

```{autodoc2-docstring} bumpversion.config.files_legacy.update_ini_config_file
:parser: myst
```
````
