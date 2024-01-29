# {py:mod}`bumpversion.config.files`

```{py:module} bumpversion.config.files
```

```{autodoc2-docstring} bumpversion.config.files
:parser: myst
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`find_config_file <bumpversion.config.files.find_config_file>`
  - ```{autodoc2-docstring} bumpversion.config.files.find_config_file
    :parser: myst
    :summary:
    ```
* - {py:obj}`read_config_file <bumpversion.config.files.read_config_file>`
  - ```{autodoc2-docstring} bumpversion.config.files.read_config_file
    :parser: myst
    :summary:
    ```
* - {py:obj}`read_toml_file <bumpversion.config.files.read_toml_file>`
  - ```{autodoc2-docstring} bumpversion.config.files.read_toml_file
    :parser: myst
    :summary:
    ```
* - {py:obj}`update_config_file <bumpversion.config.files.update_config_file>`
  - ```{autodoc2-docstring} bumpversion.config.files.update_config_file
    :parser: myst
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`logger <bumpversion.config.files.logger>`
  - ```{autodoc2-docstring} bumpversion.config.files.logger
    :parser: myst
    :summary:
    ```
* - {py:obj}`CONFIG_FILE_SEARCH_ORDER <bumpversion.config.files.CONFIG_FILE_SEARCH_ORDER>`
  - ```{autodoc2-docstring} bumpversion.config.files.CONFIG_FILE_SEARCH_ORDER
    :parser: myst
    :summary:
    ```
````

### API

````{py:data} logger
:canonical: bumpversion.config.files.logger
:value: >
   'get_indented_logger(...)'

```{autodoc2-docstring} bumpversion.config.files.logger
:parser: myst
```

````

````{py:data} CONFIG_FILE_SEARCH_ORDER
:canonical: bumpversion.config.files.CONFIG_FILE_SEARCH_ORDER
:value: >
   ('.bumpversion.cfg', '.bumpversion.toml', 'setup.cfg', 'pyproject.toml')

```{autodoc2-docstring} bumpversion.config.files.CONFIG_FILE_SEARCH_ORDER
:parser: myst
```

````

````{py:function} find_config_file(explicit_file: typing.Union[str, pathlib.Path, None] = None) -> typing.Union[pathlib.Path, None]
:canonical: bumpversion.config.files.find_config_file

```{autodoc2-docstring} bumpversion.config.files.find_config_file
:parser: myst
```
````

````{py:function} read_config_file(config_file: typing.Union[str, pathlib.Path, None] = None) -> typing.Dict[str, typing.Any]
:canonical: bumpversion.config.files.read_config_file

```{autodoc2-docstring} bumpversion.config.files.read_config_file
:parser: myst
```
````

````{py:function} read_toml_file(file_path: pathlib.Path) -> typing.Dict[str, typing.Any]
:canonical: bumpversion.config.files.read_toml_file

```{autodoc2-docstring} bumpversion.config.files.read_toml_file
:parser: myst
```
````

````{py:function} update_config_file(config_file: typing.Union[str, pathlib.Path], config: bumpversion.config.models.Config, current_version: bumpversion.versioning.models.Version, new_version: bumpversion.versioning.models.Version, context: typing.MutableMapping, dry_run: bool = False) -> None
:canonical: bumpversion.config.files.update_config_file

```{autodoc2-docstring} bumpversion.config.files.update_config_file
:parser: myst
```
````
