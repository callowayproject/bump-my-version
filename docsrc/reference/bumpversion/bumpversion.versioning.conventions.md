# {py:mod}`bumpversion.versioning.conventions`

```{py:module} bumpversion.versioning.conventions
```

```{autodoc2-docstring} bumpversion.versioning.conventions
:parser: myst
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`pep440_version_spec <bumpversion.versioning.conventions.pep440_version_spec>`
  - ```{autodoc2-docstring} bumpversion.versioning.conventions.pep440_version_spec
    :parser: myst
    :summary:
    ```
* - {py:obj}`semver_spec <bumpversion.versioning.conventions.semver_spec>`
  - ```{autodoc2-docstring} bumpversion.versioning.conventions.semver_spec
    :parser: myst
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`PEP440_PATTERN <bumpversion.versioning.conventions.PEP440_PATTERN>`
  - ```{autodoc2-docstring} bumpversion.versioning.conventions.PEP440_PATTERN
    :parser: myst
    :summary:
    ```
* - {py:obj}`PEP440_SERIALIZE_PATTERNS <bumpversion.versioning.conventions.PEP440_SERIALIZE_PATTERNS>`
  - ```{autodoc2-docstring} bumpversion.versioning.conventions.PEP440_SERIALIZE_PATTERNS
    :parser: myst
    :summary:
    ```
* - {py:obj}`PEP440_COMPONENT_CONFIGS <bumpversion.versioning.conventions.PEP440_COMPONENT_CONFIGS>`
  - ```{autodoc2-docstring} bumpversion.versioning.conventions.PEP440_COMPONENT_CONFIGS
    :parser: myst
    :summary:
    ```
* - {py:obj}`SEMVER_PATTERN <bumpversion.versioning.conventions.SEMVER_PATTERN>`
  - ```{autodoc2-docstring} bumpversion.versioning.conventions.SEMVER_PATTERN
    :parser: myst
    :summary:
    ```
* - {py:obj}`SEMVER_SERIALIZE_PATTERNS <bumpversion.versioning.conventions.SEMVER_SERIALIZE_PATTERNS>`
  - ```{autodoc2-docstring} bumpversion.versioning.conventions.SEMVER_SERIALIZE_PATTERNS
    :parser: myst
    :summary:
    ```
* - {py:obj}`SEMVER_COMPONENT_CONFIGS <bumpversion.versioning.conventions.SEMVER_COMPONENT_CONFIGS>`
  - ```{autodoc2-docstring} bumpversion.versioning.conventions.SEMVER_COMPONENT_CONFIGS
    :parser: myst
    :summary:
    ```
````

### API

````{py:data} PEP440_PATTERN
:canonical: bumpversion.versioning.conventions.PEP440_PATTERN
:value: <Multiline-String>

```{autodoc2-docstring} bumpversion.versioning.conventions.PEP440_PATTERN
:parser: myst
```

````

````{py:data} PEP440_SERIALIZE_PATTERNS
:canonical: bumpversion.versioning.conventions.PEP440_SERIALIZE_PATTERNS
:value: >
   ['{major}.{minor}.{patch}{pre_l}{pre_n}.{post}.{dev}+{local}', '{major}.{minor}.{patch}{pre_l}{pre_n...

```{autodoc2-docstring} bumpversion.versioning.conventions.PEP440_SERIALIZE_PATTERNS
:parser: myst
```

````

````{py:data} PEP440_COMPONENT_CONFIGS
:canonical: bumpversion.versioning.conventions.PEP440_COMPONENT_CONFIGS
:value: >
   None

```{autodoc2-docstring} bumpversion.versioning.conventions.PEP440_COMPONENT_CONFIGS
:parser: myst
```

````

````{py:function} pep440_version_spec() -> bumpversion.versioning.models.VersionSpec
:canonical: bumpversion.versioning.conventions.pep440_version_spec

```{autodoc2-docstring} bumpversion.versioning.conventions.pep440_version_spec
:parser: myst
```
````

````{py:data} SEMVER_PATTERN
:canonical: bumpversion.versioning.conventions.SEMVER_PATTERN
:value: <Multiline-String>

```{autodoc2-docstring} bumpversion.versioning.conventions.SEMVER_PATTERN
:parser: myst
```

````

````{py:data} SEMVER_SERIALIZE_PATTERNS
:canonical: bumpversion.versioning.conventions.SEMVER_SERIALIZE_PATTERNS
:value: >
   ['{major}.{minor}.{patch}-{pre_l}{pre_n}+{buildmetadata}', '{major}.{minor}.{patch}-{pre_l}{pre_n}',...

```{autodoc2-docstring} bumpversion.versioning.conventions.SEMVER_SERIALIZE_PATTERNS
:parser: myst
```

````

````{py:data} SEMVER_COMPONENT_CONFIGS
:canonical: bumpversion.versioning.conventions.SEMVER_COMPONENT_CONFIGS
:value: >
   None

```{autodoc2-docstring} bumpversion.versioning.conventions.SEMVER_COMPONENT_CONFIGS
:parser: myst
```

````

````{py:function} semver_spec() -> bumpversion.versioning.models.VersionSpec
:canonical: bumpversion.versioning.conventions.semver_spec

```{autodoc2-docstring} bumpversion.versioning.conventions.semver_spec
:parser: myst
```
````
