# {py:mod}`bumpversion.config`

```{py:module} bumpversion.config
```

```{autodoc2-docstring} bumpversion.config
:allowtitles:
```

## Submodules

```{toctree}
:titlesonly:
:maxdepth: 1

bumpversion.config.files
bumpversion.config.models
bumpversion.config.create
bumpversion.config.files_legacy
bumpversion.config.utils
```

## Package Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`get_configuration <bumpversion.config.get_configuration>`
  - ```{autodoc2-docstring} bumpversion.config.get_configuration
    :summary:
    ```
* - {py:obj}`check_current_version <bumpversion.config.check_current_version>`
  - ```{autodoc2-docstring} bumpversion.config.check_current_version
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
````

### API

````{py:data} logger
:canonical: bumpversion.config.logger
:value: >
   'get_indented_logger(...)'

```{autodoc2-docstring} bumpversion.config.logger
```

````

````{py:data} DEFAULTS
:canonical: bumpversion.config.DEFAULTS
:value: >
   None

```{autodoc2-docstring} bumpversion.config.DEFAULTS
```

````

````{py:function} get_configuration(config_file: typing.Union[str, pathlib.Path, None] = None, **overrides) -> bumpversion.config.models.Config
:canonical: bumpversion.config.get_configuration

```{autodoc2-docstring} bumpversion.config.get_configuration
```
````

````{py:function} check_current_version(config: bumpversion.config.models.Config) -> str
:canonical: bumpversion.config.check_current_version

```{autodoc2-docstring} bumpversion.config.check_current_version
```
````
