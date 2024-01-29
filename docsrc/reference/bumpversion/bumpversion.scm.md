# {py:mod}`bumpversion.scm`

```{py:module} bumpversion.scm
```

```{autodoc2-docstring} bumpversion.scm
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`SCMInfo <bumpversion.scm.SCMInfo>`
  - ```{autodoc2-docstring} bumpversion.scm.SCMInfo
    :parser: myst
    :summary:
    ```
* - {py:obj}`SourceCodeManager <bumpversion.scm.SourceCodeManager>`
  - ```{autodoc2-docstring} bumpversion.scm.SourceCodeManager
    :parser: myst
    :summary:
    ```
* - {py:obj}`Git <bumpversion.scm.Git>`
  - ```{autodoc2-docstring} bumpversion.scm.Git
    :parser: myst
    :summary:
    ```
* - {py:obj}`Mercurial <bumpversion.scm.Mercurial>`
  - ```{autodoc2-docstring} bumpversion.scm.Mercurial
    :parser: myst
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`get_scm_info <bumpversion.scm.get_scm_info>`
  - ```{autodoc2-docstring} bumpversion.scm.get_scm_info
    :parser: myst
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`logger <bumpversion.scm.logger>`
  - ```{autodoc2-docstring} bumpversion.scm.logger
    :parser: myst
    :summary:
    ```
````

### API

````{py:data} logger
:canonical: bumpversion.scm.logger
:value: >
   'get_indented_logger(...)'

```{autodoc2-docstring} bumpversion.scm.logger
:parser: myst
```

````

`````{py:class} SCMInfo
:canonical: bumpversion.scm.SCMInfo

```{autodoc2-docstring} bumpversion.scm.SCMInfo
:parser: myst
```

````{py:attribute} tool
:canonical: bumpversion.scm.SCMInfo.tool
:type: typing.Optional[typing.Type[SourceCodeManager]]
:value: >
   None

```{autodoc2-docstring} bumpversion.scm.SCMInfo.tool
:parser: myst
```

````

````{py:attribute} commit_sha
:canonical: bumpversion.scm.SCMInfo.commit_sha
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} bumpversion.scm.SCMInfo.commit_sha
:parser: myst
```

````

````{py:attribute} distance_to_latest_tag
:canonical: bumpversion.scm.SCMInfo.distance_to_latest_tag
:type: int
:value: >
   0

```{autodoc2-docstring} bumpversion.scm.SCMInfo.distance_to_latest_tag
:parser: myst
```

````

````{py:attribute} current_version
:canonical: bumpversion.scm.SCMInfo.current_version
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} bumpversion.scm.SCMInfo.current_version
:parser: myst
```

````

````{py:attribute} branch_name
:canonical: bumpversion.scm.SCMInfo.branch_name
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} bumpversion.scm.SCMInfo.branch_name
:parser: myst
```

````

````{py:attribute} short_branch_name
:canonical: bumpversion.scm.SCMInfo.short_branch_name
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} bumpversion.scm.SCMInfo.short_branch_name
:parser: myst
```

````

````{py:attribute} dirty
:canonical: bumpversion.scm.SCMInfo.dirty
:type: typing.Optional[bool]
:value: >
   None

```{autodoc2-docstring} bumpversion.scm.SCMInfo.dirty
:parser: myst
```

````

````{py:method} __str__()
:canonical: bumpversion.scm.SCMInfo.__str__

````

````{py:method} __repr__()
:canonical: bumpversion.scm.SCMInfo.__repr__

````

`````

`````{py:class} SourceCodeManager
:canonical: bumpversion.scm.SourceCodeManager

```{autodoc2-docstring} bumpversion.scm.SourceCodeManager
:parser: myst
```

````{py:attribute} _TEST_USABLE_COMMAND
:canonical: bumpversion.scm.SourceCodeManager._TEST_USABLE_COMMAND
:type: typing.ClassVar[typing.List[str]]
:value: >
   []

```{autodoc2-docstring} bumpversion.scm.SourceCodeManager._TEST_USABLE_COMMAND
:parser: myst
```

````

````{py:attribute} _COMMIT_COMMAND
:canonical: bumpversion.scm.SourceCodeManager._COMMIT_COMMAND
:type: typing.ClassVar[typing.List[str]]
:value: >
   []

```{autodoc2-docstring} bumpversion.scm.SourceCodeManager._COMMIT_COMMAND
:parser: myst
```

````

````{py:attribute} _ALL_TAGS_COMMAND
:canonical: bumpversion.scm.SourceCodeManager._ALL_TAGS_COMMAND
:type: typing.ClassVar[typing.List[str]]
:value: >
   []

```{autodoc2-docstring} bumpversion.scm.SourceCodeManager._ALL_TAGS_COMMAND
:parser: myst
```

````

````{py:method} commit(message: str, current_version: str, new_version: str, extra_args: typing.Optional[list] = None) -> None
:canonical: bumpversion.scm.SourceCodeManager.commit
:classmethod:

```{autodoc2-docstring} bumpversion.scm.SourceCodeManager.commit
:parser: myst
```

````

````{py:method} is_usable() -> bool
:canonical: bumpversion.scm.SourceCodeManager.is_usable
:classmethod:

```{autodoc2-docstring} bumpversion.scm.SourceCodeManager.is_usable
:parser: myst
```

````

````{py:method} assert_nondirty() -> None
:canonical: bumpversion.scm.SourceCodeManager.assert_nondirty
:abstractmethod:
:classmethod:

```{autodoc2-docstring} bumpversion.scm.SourceCodeManager.assert_nondirty
:parser: myst
```

````

````{py:method} latest_tag_info(tag_name: str, parse_pattern: str) -> bumpversion.scm.SCMInfo
:canonical: bumpversion.scm.SourceCodeManager.latest_tag_info
:abstractmethod:
:classmethod:

```{autodoc2-docstring} bumpversion.scm.SourceCodeManager.latest_tag_info
:parser: myst
```

````

````{py:method} add_path(path: typing.Union[str, pathlib.Path]) -> None
:canonical: bumpversion.scm.SourceCodeManager.add_path
:abstractmethod:
:classmethod:

```{autodoc2-docstring} bumpversion.scm.SourceCodeManager.add_path
:parser: myst
```

````

````{py:method} tag(name: str, sign: bool = False, message: typing.Optional[str] = None) -> None
:canonical: bumpversion.scm.SourceCodeManager.tag
:abstractmethod:
:classmethod:

```{autodoc2-docstring} bumpversion.scm.SourceCodeManager.tag
:parser: myst
```

````

````{py:method} get_all_tags() -> typing.List[str]
:canonical: bumpversion.scm.SourceCodeManager.get_all_tags
:classmethod:

```{autodoc2-docstring} bumpversion.scm.SourceCodeManager.get_all_tags
:parser: myst
```

````

````{py:method} get_version_from_tag(tag: str, tag_name: str, parse_pattern: str) -> typing.Optional[str]
:canonical: bumpversion.scm.SourceCodeManager.get_version_from_tag
:classmethod:

```{autodoc2-docstring} bumpversion.scm.SourceCodeManager.get_version_from_tag
:parser: myst
```

````

````{py:method} commit_to_scm(files: typing.List[typing.Union[str, pathlib.Path]], config: bumpversion.config.Config, context: typing.MutableMapping, extra_args: typing.Optional[typing.List[str]] = None, dry_run: bool = False) -> None
:canonical: bumpversion.scm.SourceCodeManager.commit_to_scm
:classmethod:

```{autodoc2-docstring} bumpversion.scm.SourceCodeManager.commit_to_scm
:parser: myst
```

````

````{py:method} tag_in_scm(config: bumpversion.config.Config, context: typing.MutableMapping, dry_run: bool = False) -> None
:canonical: bumpversion.scm.SourceCodeManager.tag_in_scm
:classmethod:

```{autodoc2-docstring} bumpversion.scm.SourceCodeManager.tag_in_scm
:parser: myst
```

````

````{py:method} __str__()
:canonical: bumpversion.scm.SourceCodeManager.__str__

````

````{py:method} __repr__()
:canonical: bumpversion.scm.SourceCodeManager.__repr__

````

`````

`````{py:class} Git
:canonical: bumpversion.scm.Git

Bases: {py:obj}`bumpversion.scm.SourceCodeManager`

```{autodoc2-docstring} bumpversion.scm.Git
:parser: myst
```

````{py:attribute} _TEST_USABLE_COMMAND
:canonical: bumpversion.scm.Git._TEST_USABLE_COMMAND
:type: typing.ClassVar[typing.List[str]]
:value: >
   ['git', 'rev-parse', '--git-dir']

```{autodoc2-docstring} bumpversion.scm.Git._TEST_USABLE_COMMAND
:parser: myst
```

````

````{py:attribute} _COMMIT_COMMAND
:canonical: bumpversion.scm.Git._COMMIT_COMMAND
:type: typing.ClassVar[typing.List[str]]
:value: >
   ['git', 'commit', '-F']

```{autodoc2-docstring} bumpversion.scm.Git._COMMIT_COMMAND
:parser: myst
```

````

````{py:attribute} _ALL_TAGS_COMMAND
:canonical: bumpversion.scm.Git._ALL_TAGS_COMMAND
:type: typing.ClassVar[typing.List[str]]
:value: >
   ['git', 'tag', '--list']

```{autodoc2-docstring} bumpversion.scm.Git._ALL_TAGS_COMMAND
:parser: myst
```

````

````{py:method} assert_nondirty() -> None
:canonical: bumpversion.scm.Git.assert_nondirty
:classmethod:

```{autodoc2-docstring} bumpversion.scm.Git.assert_nondirty
:parser: myst
```

````

````{py:method} latest_tag_info(tag_name: str, parse_pattern: str) -> bumpversion.scm.SCMInfo
:canonical: bumpversion.scm.Git.latest_tag_info
:classmethod:

```{autodoc2-docstring} bumpversion.scm.Git.latest_tag_info
:parser: myst
```

````

````{py:method} add_path(path: typing.Union[str, pathlib.Path]) -> None
:canonical: bumpversion.scm.Git.add_path
:classmethod:

```{autodoc2-docstring} bumpversion.scm.Git.add_path
:parser: myst
```

````

````{py:method} tag(name: str, sign: bool = False, message: typing.Optional[str] = None) -> None
:canonical: bumpversion.scm.Git.tag
:classmethod:

```{autodoc2-docstring} bumpversion.scm.Git.tag
:parser: myst
```

````

`````

`````{py:class} Mercurial
:canonical: bumpversion.scm.Mercurial

Bases: {py:obj}`bumpversion.scm.SourceCodeManager`

```{autodoc2-docstring} bumpversion.scm.Mercurial
:parser: myst
```

````{py:attribute} _TEST_USABLE_COMMAND
:canonical: bumpversion.scm.Mercurial._TEST_USABLE_COMMAND
:type: typing.ClassVar[typing.List[str]]
:value: >
   ['hg', 'root']

```{autodoc2-docstring} bumpversion.scm.Mercurial._TEST_USABLE_COMMAND
:parser: myst
```

````

````{py:attribute} _COMMIT_COMMAND
:canonical: bumpversion.scm.Mercurial._COMMIT_COMMAND
:type: typing.ClassVar[typing.List[str]]
:value: >
   ['hg', 'commit', '--logfile']

```{autodoc2-docstring} bumpversion.scm.Mercurial._COMMIT_COMMAND
:parser: myst
```

````

````{py:attribute} _ALL_TAGS_COMMAND
:canonical: bumpversion.scm.Mercurial._ALL_TAGS_COMMAND
:type: typing.ClassVar[typing.List[str]]
:value: >
   ['hg', 'log', '--rev="tag()"', '--template="{tags}\n"']

```{autodoc2-docstring} bumpversion.scm.Mercurial._ALL_TAGS_COMMAND
:parser: myst
```

````

````{py:method} latest_tag_info(tag_name: str, parse_pattern: str) -> bumpversion.scm.SCMInfo
:canonical: bumpversion.scm.Mercurial.latest_tag_info
:classmethod:

```{autodoc2-docstring} bumpversion.scm.Mercurial.latest_tag_info
:parser: myst
```

````

````{py:method} assert_nondirty() -> None
:canonical: bumpversion.scm.Mercurial.assert_nondirty
:classmethod:

```{autodoc2-docstring} bumpversion.scm.Mercurial.assert_nondirty
:parser: myst
```

````

````{py:method} add_path(path: typing.Union[str, pathlib.Path]) -> None
:canonical: bumpversion.scm.Mercurial.add_path
:classmethod:

```{autodoc2-docstring} bumpversion.scm.Mercurial.add_path
:parser: myst
```

````

````{py:method} tag(name: str, sign: bool = False, message: typing.Optional[str] = None) -> None
:canonical: bumpversion.scm.Mercurial.tag
:classmethod:

```{autodoc2-docstring} bumpversion.scm.Mercurial.tag
:parser: myst
```

````

`````

````{py:function} get_scm_info(tag_name: str, parse_pattern: str) -> bumpversion.scm.SCMInfo
:canonical: bumpversion.scm.get_scm_info

```{autodoc2-docstring} bumpversion.scm.get_scm_info
:parser: myst
```
````
