# {py:mod}`bumpversion.config.utils`

```{py:module} bumpversion.config.utils
```

```{autodoc2-docstring} bumpversion.config.utils
:parser: myst
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`get_all_file_configs <bumpversion.config.utils.get_all_file_configs>`
  - ```{autodoc2-docstring} bumpversion.config.utils.get_all_file_configs
    :parser: myst
    :summary:
    ```
* - {py:obj}`get_all_part_configs <bumpversion.config.utils.get_all_part_configs>`
  - ```{autodoc2-docstring} bumpversion.config.utils.get_all_part_configs
    :parser: myst
    :summary:
    ```
* - {py:obj}`resolve_glob_files <bumpversion.config.utils.resolve_glob_files>`
  - ```{autodoc2-docstring} bumpversion.config.utils.resolve_glob_files
    :parser: myst
    :summary:
    ```
````

### API

````{py:function} get_all_file_configs(config_dict: dict) -> typing.List[bumpversion.config.models.FileChange]
:canonical: bumpversion.config.utils.get_all_file_configs

```{autodoc2-docstring} bumpversion.config.utils.get_all_file_configs
:parser: myst
```
````

````{py:function} get_all_part_configs(config_dict: dict) -> typing.Dict[str, bumpversion.versioning.models.VersionComponentSpec]
:canonical: bumpversion.config.utils.get_all_part_configs

```{autodoc2-docstring} bumpversion.config.utils.get_all_part_configs
:parser: myst
```
````

````{py:function} resolve_glob_files(file_cfg: bumpversion.config.models.FileChange) -> typing.List[bumpversion.config.models.FileChange]
:canonical: bumpversion.config.utils.resolve_glob_files

```{autodoc2-docstring} bumpversion.config.utils.resolve_glob_files
:parser: myst
```
````
