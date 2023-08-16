# {py:mod}`bumpversion.config`

```{py:module} bumpversion.config
```

```{autodoc2-docstring} bumpversion.config
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`VersionPartConfig <bumpversion.config.VersionPartConfig>`
  - ```{autodoc2-docstring} bumpversion.config.VersionPartConfig
    :summary:
    ```
* - {py:obj}`FileConfig <bumpversion.config.FileConfig>`
  - ```{autodoc2-docstring} bumpversion.config.FileConfig
    :summary:
    ```
* - {py:obj}`Config <bumpversion.config.Config>`
  - ```{autodoc2-docstring} bumpversion.config.Config
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`get_all_file_configs <bumpversion.config.get_all_file_configs>`
  - ```{autodoc2-docstring} bumpversion.config.get_all_file_configs
    :summary:
    ```
* - {py:obj}`get_configuration <bumpversion.config.get_configuration>`
  - ```{autodoc2-docstring} bumpversion.config.get_configuration
    :summary:
    ```
* - {py:obj}`get_all_part_configs <bumpversion.config.get_all_part_configs>`
  - ```{autodoc2-docstring} bumpversion.config.get_all_part_configs
    :summary:
    ```
* - {py:obj}`check_current_version <bumpversion.config.check_current_version>`
  - ```{autodoc2-docstring} bumpversion.config.check_current_version
    :summary:
    ```
* - {py:obj}`find_config_file <bumpversion.config.find_config_file>`
  - ```{autodoc2-docstring} bumpversion.config.find_config_file
    :summary:
    ```
* - {py:obj}`read_config_file <bumpversion.config.read_config_file>`
  - ```{autodoc2-docstring} bumpversion.config.read_config_file
    :summary:
    ```
* - {py:obj}`read_ini_file <bumpversion.config.read_ini_file>`
  - ```{autodoc2-docstring} bumpversion.config.read_ini_file
    :summary:
    ```
* - {py:obj}`read_toml_file <bumpversion.config.read_toml_file>`
  - ```{autodoc2-docstring} bumpversion.config.read_toml_file
    :summary:
    ```
* - {py:obj}`update_config_file <bumpversion.config.update_config_file>`
  - ```{autodoc2-docstring} bumpversion.config.update_config_file
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`logger <bumpversion.config.logger>`
  - ```{autodoc2-docstring} bumpversion.config.logger
    :summary:
    ```
* - {py:obj}`DEFAULTS <bumpversion.config.DEFAULTS>`
  - ```{autodoc2-docstring} bumpversion.config.DEFAULTS
    :summary:
    ```
* - {py:obj}`CONFIG_FILE_SEARCH_ORDER <bumpversion.config.CONFIG_FILE_SEARCH_ORDER>`
  - ```{autodoc2-docstring} bumpversion.config.CONFIG_FILE_SEARCH_ORDER
    :summary:
    ```
````

### API

````{py:data} logger
:canonical: bumpversion.config.logger
:value: >
   None

```{autodoc2-docstring} bumpversion.config.logger
```

````

`````{py:class} VersionPartConfig
:canonical: bumpversion.config.VersionPartConfig

Bases: {py:obj}`pydantic.BaseModel`

```{autodoc2-docstring} bumpversion.config.VersionPartConfig
```

````{py:attribute} values
:canonical: bumpversion.config.VersionPartConfig.values
:type: typing.Optional[list]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.VersionPartConfig.values
```

````

````{py:attribute} optional_value
:canonical: bumpversion.config.VersionPartConfig.optional_value
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.VersionPartConfig.optional_value
```

````

````{py:attribute} first_value
:canonical: bumpversion.config.VersionPartConfig.first_value
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.VersionPartConfig.first_value
```

````

````{py:attribute} independent
:canonical: bumpversion.config.VersionPartConfig.independent
:type: bool
:value: >
   False

```{autodoc2-docstring} bumpversion.config.VersionPartConfig.independent
```

````

`````

`````{py:class} FileConfig
:canonical: bumpversion.config.FileConfig

Bases: {py:obj}`pydantic.BaseModel`

```{autodoc2-docstring} bumpversion.config.FileConfig
```

````{py:attribute} filename
:canonical: bumpversion.config.FileConfig.filename
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.FileConfig.filename
```

````

````{py:attribute} glob
:canonical: bumpversion.config.FileConfig.glob
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.FileConfig.glob
```

````

````{py:attribute} parse
:canonical: bumpversion.config.FileConfig.parse
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.FileConfig.parse
```

````

````{py:attribute} serialize
:canonical: bumpversion.config.FileConfig.serialize
:type: typing.Optional[typing.List[str]]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.FileConfig.serialize
```

````

````{py:attribute} search
:canonical: bumpversion.config.FileConfig.search
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.FileConfig.search
```

````

````{py:attribute} replace
:canonical: bumpversion.config.FileConfig.replace
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.FileConfig.replace
```

````

````{py:attribute} no_regex
:canonical: bumpversion.config.FileConfig.no_regex
:type: typing.Optional[bool]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.FileConfig.no_regex
```

````

````{py:attribute} ignore_missing_version
:canonical: bumpversion.config.FileConfig.ignore_missing_version
:type: typing.Optional[bool]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.FileConfig.ignore_missing_version
```

````

`````

``````{py:class} Config
:canonical: bumpversion.config.Config

Bases: {py:obj}`pydantic.BaseSettings`

```{autodoc2-docstring} bumpversion.config.Config
```

````{py:attribute} current_version
:canonical: bumpversion.config.Config.current_version
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.Config.current_version
```

````

````{py:attribute} parse
:canonical: bumpversion.config.Config.parse
:type: str
:value: >
   None

```{autodoc2-docstring} bumpversion.config.Config.parse
```

````

````{py:attribute} serialize
:canonical: bumpversion.config.Config.serialize
:type: typing.List[str]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.Config.serialize
```

````

````{py:attribute} search
:canonical: bumpversion.config.Config.search
:type: str
:value: >
   None

```{autodoc2-docstring} bumpversion.config.Config.search
```

````

````{py:attribute} replace
:canonical: bumpversion.config.Config.replace
:type: str
:value: >
   None

```{autodoc2-docstring} bumpversion.config.Config.replace
```

````

````{py:attribute} no_regex
:canonical: bumpversion.config.Config.no_regex
:type: bool
:value: >
   None

```{autodoc2-docstring} bumpversion.config.Config.no_regex
```

````

````{py:attribute} ignore_missing_version
:canonical: bumpversion.config.Config.ignore_missing_version
:type: bool
:value: >
   None

```{autodoc2-docstring} bumpversion.config.Config.ignore_missing_version
```

````

````{py:attribute} tag
:canonical: bumpversion.config.Config.tag
:type: bool
:value: >
   None

```{autodoc2-docstring} bumpversion.config.Config.tag
```

````

````{py:attribute} sign_tags
:canonical: bumpversion.config.Config.sign_tags
:type: bool
:value: >
   None

```{autodoc2-docstring} bumpversion.config.Config.sign_tags
```

````

````{py:attribute} tag_name
:canonical: bumpversion.config.Config.tag_name
:type: str
:value: >
   None

```{autodoc2-docstring} bumpversion.config.Config.tag_name
```

````

````{py:attribute} tag_message
:canonical: bumpversion.config.Config.tag_message
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.Config.tag_message
```

````

````{py:attribute} allow_dirty
:canonical: bumpversion.config.Config.allow_dirty
:type: bool
:value: >
   None

```{autodoc2-docstring} bumpversion.config.Config.allow_dirty
```

````

````{py:attribute} commit
:canonical: bumpversion.config.Config.commit
:type: bool
:value: >
   None

```{autodoc2-docstring} bumpversion.config.Config.commit
```

````

````{py:attribute} message
:canonical: bumpversion.config.Config.message
:type: str
:value: >
   None

```{autodoc2-docstring} bumpversion.config.Config.message
```

````

````{py:attribute} commit_args
:canonical: bumpversion.config.Config.commit_args
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.Config.commit_args
```

````

````{py:attribute} scm_info
:canonical: bumpversion.config.Config.scm_info
:type: typing.Optional[bumpversion.scm.SCMInfo]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.Config.scm_info
```

````

````{py:attribute} parts
:canonical: bumpversion.config.Config.parts
:type: typing.Dict[str, bumpversion.config.VersionPartConfig]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.Config.parts
```

````

````{py:attribute} files
:canonical: bumpversion.config.Config.files
:type: typing.List[bumpversion.config.FileConfig]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.Config.files
```

````

`````{py:class} Config
:canonical: bumpversion.config.Config.Config

```{autodoc2-docstring} bumpversion.config.Config.Config
```

````{py:attribute} env_prefix
:canonical: bumpversion.config.Config.Config.env_prefix
:value: >
   'bumpversion_'

```{autodoc2-docstring} bumpversion.config.Config.Config.env_prefix
```

````

`````

````{py:method} add_files(filename: typing.Union[str, typing.List[str]]) -> None
:canonical: bumpversion.config.Config.add_files

```{autodoc2-docstring} bumpversion.config.Config.add_files
```

````

````{py:property} version_config
:canonical: bumpversion.config.Config.version_config
:type: bumpversion.version_part.VersionConfig

```{autodoc2-docstring} bumpversion.config.Config.version_config
```

````

``````

````{py:data} DEFAULTS
:canonical: bumpversion.config.DEFAULTS
:value: >
   None

```{autodoc2-docstring} bumpversion.config.DEFAULTS
```

````

````{py:data} CONFIG_FILE_SEARCH_ORDER
:canonical: bumpversion.config.CONFIG_FILE_SEARCH_ORDER
:value: >
   ()

```{autodoc2-docstring} bumpversion.config.CONFIG_FILE_SEARCH_ORDER
```

````

````{py:function} get_all_file_configs(config_dict: dict) -> typing.List[bumpversion.config.FileConfig]
:canonical: bumpversion.config.get_all_file_configs

```{autodoc2-docstring} bumpversion.config.get_all_file_configs
```
````

````{py:function} get_configuration(config_file: typing.Union[str, pathlib.Path, None] = None, **overrides) -> bumpversion.config.Config
:canonical: bumpversion.config.get_configuration

```{autodoc2-docstring} bumpversion.config.get_configuration
```
````

````{py:function} get_all_part_configs(config_dict: dict) -> typing.Dict[str, bumpversion.config.VersionPartConfig]
:canonical: bumpversion.config.get_all_part_configs

```{autodoc2-docstring} bumpversion.config.get_all_part_configs
```
````

````{py:function} check_current_version(config: bumpversion.config.Config) -> str
:canonical: bumpversion.config.check_current_version

```{autodoc2-docstring} bumpversion.config.check_current_version
```
````

````{py:function} find_config_file(explicit_file: typing.Union[str, pathlib.Path, None] = None) -> typing.Union[pathlib.Path, None]
:canonical: bumpversion.config.find_config_file

```{autodoc2-docstring} bumpversion.config.find_config_file
```
````

````{py:function} read_config_file(config_file: typing.Union[str, pathlib.Path, None] = None) -> typing.Dict[str, typing.Any]
:canonical: bumpversion.config.read_config_file

```{autodoc2-docstring} bumpversion.config.read_config_file
```
````

````{py:function} read_ini_file(file_path: pathlib.Path) -> typing.Dict[str, typing.Any]
:canonical: bumpversion.config.read_ini_file

```{autodoc2-docstring} bumpversion.config.read_ini_file
```
````

````{py:function} read_toml_file(file_path: pathlib.Path) -> typing.Dict[str, typing.Any]
:canonical: bumpversion.config.read_toml_file

```{autodoc2-docstring} bumpversion.config.read_toml_file
```
````

````{py:function} update_config_file(config_file: typing.Union[str, pathlib.Path, None], current_version: str, new_version: str, dry_run: bool = False) -> None
:canonical: bumpversion.config.update_config_file

```{autodoc2-docstring} bumpversion.config.update_config_file
```
````
