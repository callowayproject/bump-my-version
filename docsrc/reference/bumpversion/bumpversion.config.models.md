# {py:mod}`bumpversion.config.models`

```{py:module} bumpversion.config.models
```

```{autodoc2-docstring} bumpversion.config.models
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`FileChange <bumpversion.config.models.FileChange>`
  - ```{autodoc2-docstring} bumpversion.config.models.FileChange
    :parser: myst
    :summary:
    ```
* - {py:obj}`Config <bumpversion.config.models.Config>`
  - ```{autodoc2-docstring} bumpversion.config.models.Config
    :parser: myst
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`logger <bumpversion.config.models.logger>`
  - ```{autodoc2-docstring} bumpversion.config.models.logger
    :parser: myst
    :summary:
    ```
````

### API

````{py:data} logger
:canonical: bumpversion.config.models.logger
:value: >
   'get_indented_logger(...)'

```{autodoc2-docstring} bumpversion.config.models.logger
:parser: myst
```

````

`````{py:class} FileChange(**data: typing.Any)
:canonical: bumpversion.config.models.FileChange

Bases: {py:obj}`pydantic.BaseModel`

```{autodoc2-docstring} bumpversion.config.models.FileChange
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.config.models.FileChange.__init__
:parser: myst
```

````{py:attribute} parse
:canonical: bumpversion.config.models.FileChange.parse
:type: str
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.FileChange.parse
:parser: myst
```

````

````{py:attribute} serialize
:canonical: bumpversion.config.models.FileChange.serialize
:type: tuple
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.FileChange.serialize
:parser: myst
```

````

````{py:attribute} search
:canonical: bumpversion.config.models.FileChange.search
:type: str
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.FileChange.search
:parser: myst
```

````

````{py:attribute} replace
:canonical: bumpversion.config.models.FileChange.replace
:type: str
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.FileChange.replace
:parser: myst
```

````

````{py:attribute} regex
:canonical: bumpversion.config.models.FileChange.regex
:type: bool
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.FileChange.regex
:parser: myst
```

````

````{py:attribute} ignore_missing_version
:canonical: bumpversion.config.models.FileChange.ignore_missing_version
:type: bool
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.FileChange.ignore_missing_version
:parser: myst
```

````

````{py:attribute} filename
:canonical: bumpversion.config.models.FileChange.filename
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.FileChange.filename
:parser: myst
```

````

````{py:attribute} glob
:canonical: bumpversion.config.models.FileChange.glob
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.FileChange.glob
:parser: myst
```

````

````{py:attribute} key_path
:canonical: bumpversion.config.models.FileChange.key_path
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.FileChange.key_path
:parser: myst
```

````

````{py:method} __hash__()
:canonical: bumpversion.config.models.FileChange.__hash__

```{autodoc2-docstring} bumpversion.config.models.FileChange.__hash__
:parser: myst
```

````

````{py:method} get_search_pattern(context: typing.MutableMapping) -> typing.Tuple[re.Pattern, str]
:canonical: bumpversion.config.models.FileChange.get_search_pattern

```{autodoc2-docstring} bumpversion.config.models.FileChange.get_search_pattern
:parser: myst
```

````

`````

`````{py:class} Config(_case_sensitive: bool | None = None, _env_prefix: str | None = None, _env_file: pydantic_settings.sources.DotenvType | None = ENV_FILE_SENTINEL, _env_file_encoding: str | None = None, _env_nested_delimiter: str | None = None, _secrets_dir: str | pathlib.Path | None = None, **values: typing.Any)
:canonical: bumpversion.config.models.Config

Bases: {py:obj}`pydantic_settings.BaseSettings`

```{autodoc2-docstring} bumpversion.config.models.Config
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} bumpversion.config.models.Config.__init__
:parser: myst
```

````{py:attribute} current_version
:canonical: bumpversion.config.models.Config.current_version
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.Config.current_version
:parser: myst
```

````

````{py:attribute} parse
:canonical: bumpversion.config.models.Config.parse
:type: str
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.Config.parse
:parser: myst
```

````

````{py:attribute} serialize
:canonical: bumpversion.config.models.Config.serialize
:type: tuple
:value: >
   'Field(...)'

```{autodoc2-docstring} bumpversion.config.models.Config.serialize
:parser: myst
```

````

````{py:attribute} search
:canonical: bumpversion.config.models.Config.search
:type: str
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.Config.search
:parser: myst
```

````

````{py:attribute} replace
:canonical: bumpversion.config.models.Config.replace
:type: str
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.Config.replace
:parser: myst
```

````

````{py:attribute} regex
:canonical: bumpversion.config.models.Config.regex
:type: bool
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.Config.regex
:parser: myst
```

````

````{py:attribute} ignore_missing_version
:canonical: bumpversion.config.models.Config.ignore_missing_version
:type: bool
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.Config.ignore_missing_version
:parser: myst
```

````

````{py:attribute} tag
:canonical: bumpversion.config.models.Config.tag
:type: bool
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.Config.tag
:parser: myst
```

````

````{py:attribute} sign_tags
:canonical: bumpversion.config.models.Config.sign_tags
:type: bool
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.Config.sign_tags
:parser: myst
```

````

````{py:attribute} tag_name
:canonical: bumpversion.config.models.Config.tag_name
:type: str
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.Config.tag_name
:parser: myst
```

````

````{py:attribute} tag_message
:canonical: bumpversion.config.models.Config.tag_message
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.Config.tag_message
:parser: myst
```

````

````{py:attribute} allow_dirty
:canonical: bumpversion.config.models.Config.allow_dirty
:type: bool
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.Config.allow_dirty
:parser: myst
```

````

````{py:attribute} commit
:canonical: bumpversion.config.models.Config.commit
:type: bool
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.Config.commit
:parser: myst
```

````

````{py:attribute} message
:canonical: bumpversion.config.models.Config.message
:type: str
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.Config.message
:parser: myst
```

````

````{py:attribute} commit_args
:canonical: bumpversion.config.models.Config.commit_args
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.Config.commit_args
:parser: myst
```

````

````{py:attribute} scm_info
:canonical: bumpversion.config.models.Config.scm_info
:type: typing.Optional[bumpversion.scm.SCMInfo]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.Config.scm_info
:parser: myst
```

````

````{py:attribute} parts
:canonical: bumpversion.config.models.Config.parts
:type: typing.Dict[str, bumpversion.versioning.models.VersionComponentSpec]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.Config.parts
:parser: myst
```

````

````{py:attribute} files
:canonical: bumpversion.config.models.Config.files
:type: typing.List[bumpversion.config.models.FileChange]
:value: >
   'Field(...)'

```{autodoc2-docstring} bumpversion.config.models.Config.files
:parser: myst
```

````

````{py:attribute} included_paths
:canonical: bumpversion.config.models.Config.included_paths
:type: typing.List[str]
:value: >
   'Field(...)'

```{autodoc2-docstring} bumpversion.config.models.Config.included_paths
:parser: myst
```

````

````{py:attribute} excluded_paths
:canonical: bumpversion.config.models.Config.excluded_paths
:type: typing.List[str]
:value: >
   'Field(...)'

```{autodoc2-docstring} bumpversion.config.models.Config.excluded_paths
:parser: myst
```

````

````{py:attribute} model_config
:canonical: bumpversion.config.models.Config.model_config
:value: >
   'SettingsConfigDict(...)'

```{autodoc2-docstring} bumpversion.config.models.Config.model_config
:parser: myst
```

````

````{py:attribute} _resolved_filemap
:canonical: bumpversion.config.models.Config._resolved_filemap
:type: typing.Optional[typing.Dict[str, typing.List[bumpversion.config.models.FileChange]]]
:value: >
   None

```{autodoc2-docstring} bumpversion.config.models.Config._resolved_filemap
:parser: myst
```

````

````{py:method} add_files(filename: typing.Union[str, typing.List[str]]) -> None
:canonical: bumpversion.config.models.Config.add_files

```{autodoc2-docstring} bumpversion.config.models.Config.add_files
:parser: myst
```

````

````{py:property} resolved_filemap
:canonical: bumpversion.config.models.Config.resolved_filemap
:type: typing.Dict[str, typing.List[bumpversion.config.models.FileChange]]

```{autodoc2-docstring} bumpversion.config.models.Config.resolved_filemap
:parser: myst
```

````

````{py:method} _resolve_filemap() -> typing.Dict[str, typing.List[bumpversion.config.models.FileChange]]
:canonical: bumpversion.config.models.Config._resolve_filemap

```{autodoc2-docstring} bumpversion.config.models.Config._resolve_filemap
:parser: myst
```

````

````{py:property} files_to_modify
:canonical: bumpversion.config.models.Config.files_to_modify
:type: typing.List[bumpversion.config.models.FileChange]

```{autodoc2-docstring} bumpversion.config.models.Config.files_to_modify
:parser: myst
```

````

````{py:property} version_config
:canonical: bumpversion.config.models.Config.version_config
:type: bumpversion.version_part.VersionConfig

```{autodoc2-docstring} bumpversion.config.models.Config.version_config
:parser: myst
```

````

````{py:method} version_spec(version: typing.Optional[str] = None) -> bumpversion.versioning.models.VersionSpec
:canonical: bumpversion.config.models.Config.version_spec

```{autodoc2-docstring} bumpversion.config.models.Config.version_spec
:parser: myst
```

````

`````
