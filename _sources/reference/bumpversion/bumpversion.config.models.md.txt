# {py:mod}`bumpversion.config.models`

```{py:module} bumpversion.config.models
```

```{autodoc2-docstring} bumpversion.config.models
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`VersionPartConfig <bumpversion.config.models.VersionPartConfig>`
  - ```{autodoc2-docstring} bumpversion.config.models.VersionPartConfig
    :summary:
    ```
* - {py:obj}`FileChange <bumpversion.config.models.FileChange>`
  - ```{autodoc2-docstring} bumpversion.config.models.FileChange
    :summary:
    ```
* - {py:obj}`Config <bumpversion.config.models.Config>`
  - ```{autodoc2-docstring} bumpversion.config.models.Config
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`logger <bumpversion.config.models.logger>`
  - ```{autodoc2-docstring} bumpversion.config.models.logger
    :summary:
    ```
````

### API

````{py:data} logger
:canonical: bumpversion.config.models.logger
:value: >
   'get_indented_logger(...)'

```{autodoc2-docstring} bumpversion.config.models.logger
```

````

`````{py:class} VersionPartConfig(**data: typing.Any)
:canonical: bumpversion.config.models.VersionPartConfig

Bases: {py:obj}`pydantic.BaseModel`

```{autodoc2-docstring} bumpversion.config.models.VersionPartConfig
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.config.models.VersionPartConfig.__init__
```

````{py:attribute} values
:canonical: bumpversion.config.models.VersionPartConfig.values
:type: typing.Optional[list]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.VersionPartConfig.values
```

````

````{py:attribute} optional_value
:canonical: bumpversion.config.models.VersionPartConfig.optional_value
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.VersionPartConfig.optional_value
```

````

````{py:attribute} first_value
:canonical: bumpversion.config.models.VersionPartConfig.first_value
:type: typing.Union[str, int, None]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.VersionPartConfig.first_value
```

````

````{py:attribute} independent
:canonical: bumpversion.config.models.VersionPartConfig.independent
:type: bool
:value: >
   False

```{autodoc2-docstring} bumpversion.config.models.VersionPartConfig.independent
```

````

`````

`````{py:class} FileChange(**data: typing.Any)
:canonical: bumpversion.config.models.FileChange

Bases: {py:obj}`pydantic.BaseModel`

```{autodoc2-docstring} bumpversion.config.models.FileChange
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.config.models.FileChange.__init__
```

````{py:attribute} parse
:canonical: bumpversion.config.models.FileChange.parse
:type: str
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.FileChange.parse
```

````

````{py:attribute} serialize
:canonical: bumpversion.config.models.FileChange.serialize
:type: tuple
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.FileChange.serialize
```

````

````{py:attribute} search
:canonical: bumpversion.config.models.FileChange.search
:type: str
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.FileChange.search
```

````

````{py:attribute} replace
:canonical: bumpversion.config.models.FileChange.replace
:type: str
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.FileChange.replace
```

````

````{py:attribute} regex
:canonical: bumpversion.config.models.FileChange.regex
:type: bool
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.FileChange.regex
```

````

````{py:attribute} ignore_missing_version
:canonical: bumpversion.config.models.FileChange.ignore_missing_version
:type: bool
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.FileChange.ignore_missing_version
```

````

````{py:attribute} filename
:canonical: bumpversion.config.models.FileChange.filename
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.FileChange.filename
```

````

````{py:attribute} glob
:canonical: bumpversion.config.models.FileChange.glob
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.FileChange.glob
```

````

````{py:attribute} key_path
:canonical: bumpversion.config.models.FileChange.key_path
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.FileChange.key_path
```

````

````{py:method} __hash__()
:canonical: bumpversion.config.models.FileChange.__hash__

```{autodoc2-docstring} bumpversion.config.models.FileChange.__hash__
```

````

````{py:method} get_search_pattern(context: typing.MutableMapping) -> typing.Tuple[re.Pattern, str]
:canonical: bumpversion.config.models.FileChange.get_search_pattern

```{autodoc2-docstring} bumpversion.config.models.FileChange.get_search_pattern
```

````

`````

`````{py:class} Config(_case_sensitive: bool | None = None, _env_prefix: str | None = None, _env_file: pydantic_settings.sources.DotenvType | None = ENV_FILE_SENTINEL, _env_file_encoding: str | None = None, _env_nested_delimiter: str | None = None, _secrets_dir: str | pathlib.Path | None = None, **values: typing.Any)
:canonical: bumpversion.config.models.Config

Bases: {py:obj}`pydantic_settings.BaseSettings`

```{autodoc2-docstring} bumpversion.config.models.Config
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.config.models.Config.__init__
```

````{py:attribute} current_version
:canonical: bumpversion.config.models.Config.current_version
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.Config.current_version
```

````

````{py:attribute} parse
:canonical: bumpversion.config.models.Config.parse
:type: str
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.Config.parse
```

````

````{py:attribute} serialize
:canonical: bumpversion.config.models.Config.serialize
:type: tuple
:value: >
   'Field(...)'

```{autodoc2-docstring} bumpversion.config.models.Config.serialize
```

````

````{py:attribute} search
:canonical: bumpversion.config.models.Config.search
:type: str
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.Config.search
```

````

````{py:attribute} replace
:canonical: bumpversion.config.models.Config.replace
:type: str
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.Config.replace
```

````

````{py:attribute} regex
:canonical: bumpversion.config.models.Config.regex
:type: bool
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.Config.regex
```

````

````{py:attribute} ignore_missing_version
:canonical: bumpversion.config.models.Config.ignore_missing_version
:type: bool
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.Config.ignore_missing_version
```

````

````{py:attribute} tag
:canonical: bumpversion.config.models.Config.tag
:type: bool
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.Config.tag
```

````

````{py:attribute} sign_tags
:canonical: bumpversion.config.models.Config.sign_tags
:type: bool
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.Config.sign_tags
```

````

````{py:attribute} tag_name
:canonical: bumpversion.config.models.Config.tag_name
:type: str
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.Config.tag_name
```

````

````{py:attribute} tag_message
:canonical: bumpversion.config.models.Config.tag_message
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.Config.tag_message
```

````

````{py:attribute} allow_dirty
:canonical: bumpversion.config.models.Config.allow_dirty
:type: bool
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.Config.allow_dirty
```

````

````{py:attribute} commit
:canonical: bumpversion.config.models.Config.commit
:type: bool
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.Config.commit
```

````

````{py:attribute} message
:canonical: bumpversion.config.models.Config.message
:type: str
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.Config.message
```

````

````{py:attribute} commit_args
:canonical: bumpversion.config.models.Config.commit_args
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.Config.commit_args
```

````

````{py:attribute} scm_info
:canonical: bumpversion.config.models.Config.scm_info
:type: typing.Optional[bumpversion.scm.SCMInfo]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.Config.scm_info
```

````

````{py:attribute} parts
:canonical: bumpversion.config.models.Config.parts
:type: typing.Dict[str, bumpversion.config.models.VersionPartConfig]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.Config.parts
```

````

````{py:attribute} files
:canonical: bumpversion.config.models.Config.files
:type: typing.List[bumpversion.config.models.FileChange]
:value: >
   'Field(...)'

```{autodoc2-docstring} bumpversion.config.models.Config.files
```

````

````{py:attribute} included_paths
:canonical: bumpversion.config.models.Config.included_paths
:type: typing.List[str]
:value: >
   'Field(...)'

```{autodoc2-docstring} bumpversion.config.models.Config.included_paths
```

````

````{py:attribute} excluded_paths
:canonical: bumpversion.config.models.Config.excluded_paths
:type: typing.List[str]
:value: >
   'Field(...)'

```{autodoc2-docstring} bumpversion.config.models.Config.excluded_paths
```

````

````{py:attribute} model_config
:canonical: bumpversion.config.models.Config.model_config
:value: >
   'SettingsConfigDict(...)'

```{autodoc2-docstring} bumpversion.config.models.Config.model_config
```

````

````{py:attribute} _resolved_filemap
:canonical: bumpversion.config.models.Config._resolved_filemap
:type: typing.Optional[typing.Dict[str, typing.List[bumpversion.config.models.FileChange]]]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.Config._resolved_filemap
```

````

````{py:method} add_files(filename: typing.Union[str, typing.List[str]]) -> None
:canonical: bumpversion.config.models.Config.add_files

```{autodoc2-docstring} bumpversion.config.models.Config.add_files
```

````

````{py:property} resolved_filemap
:canonical: bumpversion.config.models.Config.resolved_filemap
:type: typing.Dict[str, typing.List[bumpversion.config.models.FileChange]]

```{autodoc2-docstring} bumpversion.config.models.Config.resolved_filemap
```

````

````{py:method} _resolve_filemap() -> typing.Dict[str, typing.List[bumpversion.config.models.FileChange]]
:canonical: bumpversion.config.models.Config._resolve_filemap

```{autodoc2-docstring} bumpversion.config.models.Config._resolve_filemap
```

````

````{py:property} files_to_modify
:canonical: bumpversion.config.models.Config.files_to_modify
:type: typing.List[bumpversion.config.models.FileChange]

```{autodoc2-docstring} bumpversion.config.models.Config.files_to_modify
```

````

````{py:property} version_config
:canonical: bumpversion.config.models.Config.version_config
:type: bumpversion.version_part.VersionConfig

```{autodoc2-docstring} bumpversion.config.models.Config.version_config
```

````

`````
