# {py:mod}`bumpversion.scm`

```{py:module} bumpversion.scm
```

```{autodoc2-docstring} bumpversion.scm
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`SCMInfo <bumpversion.scm.SCMInfo>`
  - ```{autodoc2-docstring} bumpversion.scm.SCMInfo
    :summary:
    ```
* - {py:obj}`SourceCodeManager <bumpversion.scm.SourceCodeManager>`
  - ```{autodoc2-docstring} bumpversion.scm.SourceCodeManager
    :summary:
    ```
* - {py:obj}`Git <bumpversion.scm.Git>`
  - ```{autodoc2-docstring} bumpversion.scm.Git
    :summary:
    ```
* - {py:obj}`Mercurial <bumpversion.scm.Mercurial>`
  - ```{autodoc2-docstring} bumpversion.scm.Mercurial
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`get_scm_info <bumpversion.scm.get_scm_info>`
  - ```{autodoc2-docstring} bumpversion.scm.get_scm_info
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`logger <bumpversion.scm.logger>`
  - ```{autodoc2-docstring} bumpversion.scm.logger
    :summary:
    ```
````

### API

````{py:data} logger
:canonical: bumpversion.scm.logger
:value: >
   None

```{autodoc2-docstring} bumpversion.scm.logger
```

````

`````{py:class} SCMInfo
:canonical: bumpversion.scm.SCMInfo

```{autodoc2-docstring} bumpversion.scm.SCMInfo
```

````{py:attribute} tool
:canonical: bumpversion.scm.SCMInfo.tool
:type: typing.Optional[typing.Type[SourceCodeManager]]
:value: >
   None

```{autodoc2-docstring} bumpversion.scm.SCMInfo.tool
```

````

````{py:attribute} commit_sha
:canonical: bumpversion.scm.SCMInfo.commit_sha
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} bumpversion.scm.SCMInfo.commit_sha
```

````

````{py:attribute} distance_to_latest_tag
:canonical: bumpversion.scm.SCMInfo.distance_to_latest_tag
:type: typing.Optional[int]
:value: >
   None

```{autodoc2-docstring} bumpversion.scm.SCMInfo.distance_to_latest_tag
```

````

````{py:attribute} current_version
:canonical: bumpversion.scm.SCMInfo.current_version
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} bumpversion.scm.SCMInfo.current_version
```

````

````{py:attribute} branch_name
:canonical: bumpversion.scm.SCMInfo.branch_name
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} bumpversion.scm.SCMInfo.branch_name
```

````

````{py:attribute} short_branch_name
:canonical: bumpversion.scm.SCMInfo.short_branch_name
:type: typing.Optional[str]
:value: >
   None

```{autodoc2-docstring} bumpversion.scm.SCMInfo.short_branch_name
```

````

````{py:attribute} dirty
:canonical: bumpversion.scm.SCMInfo.dirty
:type: typing.Optional[bool]
:value: >
   None

```{autodoc2-docstring} bumpversion.scm.SCMInfo.dirty
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
```

````{py:attribute} _TEST_USABLE_COMMAND
:canonical: bumpversion.scm.SourceCodeManager._TEST_USABLE_COMMAND
:type: typing.ClassVar[typing.List[str]]
:value: >
   []

```{autodoc2-docstring} bumpversion.scm.SourceCodeManager._TEST_USABLE_COMMAND
```

````

````{py:attribute} _COMMIT_COMMAND
:canonical: bumpversion.scm.SourceCodeManager._COMMIT_COMMAND
:type: typing.ClassVar[typing.List[str]]
:value: >
   []

```{autodoc2-docstring} bumpversion.scm.SourceCodeManager._COMMIT_COMMAND
```

````

````{py:attribute} _ALL_TAGS_COMMAND
:canonical: bumpversion.scm.SourceCodeManager._ALL_TAGS_COMMAND
:type: typing.ClassVar[typing.List[str]]
:value: >
   []

```{autodoc2-docstring} bumpversion.scm.SourceCodeManager._ALL_TAGS_COMMAND
```

````

````{py:method} commit(message: str, current_version: str, new_version: str, extra_args: typing.Optional[list] = None) -> None
:canonical: bumpversion.scm.SourceCodeManager.commit
:classmethod:

```{autodoc2-docstring} bumpversion.scm.SourceCodeManager.commit
```

````

````{py:method} is_usable() -> bool
:canonical: bumpversion.scm.SourceCodeManager.is_usable
:classmethod:

```{autodoc2-docstring} bumpversion.scm.SourceCodeManager.is_usable
```

````

````{py:method} assert_nondirty() -> None
:canonical: bumpversion.scm.SourceCodeManager.assert_nondirty
:abstractmethod:
:classmethod:

```{autodoc2-docstring} bumpversion.scm.SourceCodeManager.assert_nondirty
```

````

````{py:method} latest_tag_info(tag_pattern: str) -> bumpversion.scm.SCMInfo
:canonical: bumpversion.scm.SourceCodeManager.latest_tag_info
:abstractmethod:
:classmethod:

```{autodoc2-docstring} bumpversion.scm.SourceCodeManager.latest_tag_info
```

````

````{py:method} add_path(path: typing.Union[str, pathlib.Path]) -> None
:canonical: bumpversion.scm.SourceCodeManager.add_path
:abstractmethod:
:classmethod:

```{autodoc2-docstring} bumpversion.scm.SourceCodeManager.add_path
```

````

````{py:method} tag(name: str, sign: bool = False, message: typing.Optional[str] = None) -> None
:canonical: bumpversion.scm.SourceCodeManager.tag
:abstractmethod:
:classmethod:

```{autodoc2-docstring} bumpversion.scm.SourceCodeManager.tag
```

````

````{py:method} get_all_tags() -> typing.List[str]
:canonical: bumpversion.scm.SourceCodeManager.get_all_tags
:classmethod:

```{autodoc2-docstring} bumpversion.scm.SourceCodeManager.get_all_tags
```

````

````{py:method} commit_to_scm(files: typing.List[typing.Union[str, pathlib.Path]], config: bumpversion.config.Config, context: typing.MutableMapping, extra_args: typing.Optional[typing.List[str]] = None, dry_run: bool = False) -> None
:canonical: bumpversion.scm.SourceCodeManager.commit_to_scm
:classmethod:

```{autodoc2-docstring} bumpversion.scm.SourceCodeManager.commit_to_scm
```

````

````{py:method} tag_in_scm(config: bumpversion.config.Config, context: typing.MutableMapping, dry_run: bool = False) -> None
:canonical: bumpversion.scm.SourceCodeManager.tag_in_scm
:classmethod:

```{autodoc2-docstring} bumpversion.scm.SourceCodeManager.tag_in_scm
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
```

````{py:attribute} _TEST_USABLE_COMMAND
:canonical: bumpversion.scm.Git._TEST_USABLE_COMMAND
:type: typing.ClassVar[typing.List[str]]
:value: >
   ['git', 'rev-parse', '--git-dir']

```{autodoc2-docstring} bumpversion.scm.Git._TEST_USABLE_COMMAND
```

````

````{py:attribute} _COMMIT_COMMAND
:canonical: bumpversion.scm.Git._COMMIT_COMMAND
:type: typing.ClassVar[typing.List[str]]
:value: >
   ['git', 'commit', '-F']

```{autodoc2-docstring} bumpversion.scm.Git._COMMIT_COMMAND
```

````

````{py:attribute} _ALL_TAGS_COMMAND
:canonical: bumpversion.scm.Git._ALL_TAGS_COMMAND
:type: typing.ClassVar[typing.List[str]]
:value: >
   ['git', 'tag', '--list']

```{autodoc2-docstring} bumpversion.scm.Git._ALL_TAGS_COMMAND
```

````

````{py:method} assert_nondirty() -> None
:canonical: bumpversion.scm.Git.assert_nondirty
:classmethod:

```{autodoc2-docstring} bumpversion.scm.Git.assert_nondirty
```

````

````{py:method} latest_tag_info(tag_pattern: str) -> bumpversion.scm.SCMInfo
:canonical: bumpversion.scm.Git.latest_tag_info
:classmethod:

```{autodoc2-docstring} bumpversion.scm.Git.latest_tag_info
```

````

````{py:method} add_path(path: typing.Union[str, pathlib.Path]) -> None
:canonical: bumpversion.scm.Git.add_path
:classmethod:

```{autodoc2-docstring} bumpversion.scm.Git.add_path
```

````

````{py:method} tag(name: str, sign: bool = False, message: typing.Optional[str] = None) -> None
:canonical: bumpversion.scm.Git.tag
:classmethod:

```{autodoc2-docstring} bumpversion.scm.Git.tag
```

````

`````

`````{py:class} Mercurial
:canonical: bumpversion.scm.Mercurial

Bases: {py:obj}`bumpversion.scm.SourceCodeManager`

```{autodoc2-docstring} bumpversion.scm.Mercurial
```

````{py:attribute} _TEST_USABLE_COMMAND
:canonical: bumpversion.scm.Mercurial._TEST_USABLE_COMMAND
:type: typing.ClassVar[typing.List[str]]
:value: >
   ['hg', 'root']

```{autodoc2-docstring} bumpversion.scm.Mercurial._TEST_USABLE_COMMAND
```

````

````{py:attribute} _COMMIT_COMMAND
:canonical: bumpversion.scm.Mercurial._COMMIT_COMMAND
:type: typing.ClassVar[typing.List[str]]
:value: >
   ['hg', 'commit', '--logfile']

```{autodoc2-docstring} bumpversion.scm.Mercurial._COMMIT_COMMAND
```

````

````{py:attribute} _ALL_TAGS_COMMAND
:canonical: bumpversion.scm.Mercurial._ALL_TAGS_COMMAND
:type: typing.ClassVar[typing.List[str]]
:value: >
   ['hg', 'log', '--rev="tag()"', '--template="{tags}\n"']

```{autodoc2-docstring} bumpversion.scm.Mercurial._ALL_TAGS_COMMAND
```

````

````{py:method} latest_tag_info(tag_pattern: str) -> bumpversion.scm.SCMInfo
:canonical: bumpversion.scm.Mercurial.latest_tag_info
:classmethod:

```{autodoc2-docstring} bumpversion.scm.Mercurial.latest_tag_info
```

````

````{py:method} assert_nondirty() -> None
:canonical: bumpversion.scm.Mercurial.assert_nondirty
:classmethod:

```{autodoc2-docstring} bumpversion.scm.Mercurial.assert_nondirty
```

````

````{py:method} add_path(path: typing.Union[str, pathlib.Path]) -> None
:canonical: bumpversion.scm.Mercurial.add_path
:classmethod:

```{autodoc2-docstring} bumpversion.scm.Mercurial.add_path
```

````

````{py:method} tag(name: str, sign: bool = False, message: typing.Optional[str] = None) -> None
:canonical: bumpversion.scm.Mercurial.tag
:classmethod:

```{autodoc2-docstring} bumpversion.scm.Mercurial.tag
```

````

`````

````{py:function} get_scm_info(tag_pattern: str) -> bumpversion.scm.SCMInfo
:canonical: bumpversion.scm.get_scm_info

```{autodoc2-docstring} bumpversion.scm.get_scm_info
```
````
