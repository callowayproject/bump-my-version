# Changelog

## 1.0.2 (2025-03-08)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/1.0.1...1.0.2)

### Fixes

- Fix incorrect evaluation. [3578c87](https://github.com/callowayproject/bump-my-version/commit/3578c872ef8143f11c22cb5e83765c6e69cf3eef)
    
  The check for valid files to add should be `filename`, not `self.files`
- Refactor and improve test structure for file modifications. [8b52174](https://github.com/callowayproject/bump-my-version/commit/8b52174651e3c02daf3ba00166cd8f054498313d)
    
  Consolidated and restructured tests for `modify_files` into classes for better organization and clarity. Fixed an issue where empty file configurations were not properly ignored and enhanced filtering logic in configuration handling.

  Fixes #312
### Other

- Replace `list[str]` with `List[str]` for Python 3.8+ compatibility. [6fb977c](https://github.com/callowayproject/bump-my-version/commit/6fb977ca9144a590153e779c59c4c788efd1442f)
    
  Updated all instances of `list[str]` with the generic `List[str]` from the `typing` module to maintain compatibility with older Python versions (3.8 and earlier). This ensures consistent type annotations across the codebase.

  Fixes #313
- [pre-commit.ci] pre-commit autoupdate. [a057743](https://github.com/callowayproject/bump-my-version/commit/a0577433bd069f47d0e1eb368def4309f931a947)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.9.7 → v0.9.9](https://github.com/astral-sh/ruff-pre-commit/compare/v0.9.7...v0.9.9)


## 1.0.1 (2025-03-04)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/1.0.0...1.0.1)

### Fixes

- Fix type hinting compatibility for 3.8. [9c2bb03](https://github.com/callowayproject/bump-my-version/commit/9c2bb03bee4c84ff97af415a47dfc57aea925c41)
    
  Replaced `list` with `List` for type hints to ensure compatibility with earlier Python versions.

## 1.0.0 (2025-03-02)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.33.0...1.0.0)

### Breaking Changes

- Updated the Readme. [5a621c3](https://github.com/callowayproject/bump-my-version/commit/5a621c3ad28bb71e5e3d34fdae35769679c47f1b)
    
### New

- Added breaking change parsing. [00c4e7b](https://github.com/callowayproject/bump-my-version/commit/00c4e7bcaa68040c71123d16c61aae89b525b13f)
    

## 0.33.0 (2025-03-02)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.32.2...0.33.0)

### Fixes

- Fixed warnings in documentation. [782077d](https://github.com/callowayproject/bump-my-version/commit/782077dc438007d4b585991788efe7c5a5c8c19f)
    
- Refactored PEP621 tests into a class. [2a4f12a](https://github.com/callowayproject/bump-my-version/commit/2a4f12a68067bacf81ec536b884e9ec3afb16751)
    
  The tests are pretty much the same but renamed for clarity.
- Fixed: allow omitting the current version in sample-config. [6b369fe](https://github.com/callowayproject/bump-my-version/commit/6b369fec76e9a45b919e32a85d0b894752f6374d)
    
  If the current version is explicitly left empty during the
  `sample-config` questionnaire, the resulting `tool.bumpversion` table
  now lacks a `current_version` key, and will fall back to PEP 621
  `project.version` (if not dynamic). The instruction text specifically
  hints at this new functionality.
### New

- Add test for moveable tags. [df787f1](https://github.com/callowayproject/bump-my-version/commit/df787f153f1dcde8268e83ef3f035d018735e7bb)
    
- New feature: retrieve and update the PEP 621 project version, if possible. [3032450](https://github.com/callowayproject/bump-my-version/commit/3032450098f14abeb0661c62442d1ca03b222e09)
    
  When determining the current version, and if
  `tool.bumpversion.current_version` is not set, attempt to retrieve the
  version from `project.version` à la PEP 621. If that setting is not
  set, or if the version is explicitly marked as dynamically set, then
  continue with querying SCM tags.

  When updating the configuration during bumping, if we previously
  successfully retrieved a PEP 621 version, then update the
  `project.version` field in `pyproject.toml` as well. We always update,
  even if the true current version was read from
  `tool.bumpversion.current_version` instead of `project.version`.

  The docs have been updated; specifically, the "multiple replacements in
  one file" howto and the reference for `current_version`.

  The tests have been adapted: the new `pep621_info` property would
  otherwise trip up the old test output, and the `None` default would trip
  up the TOML serializer. Additionally, new tests assert that
  `project.version` (and correspondingly, the `pep621_info` property) is
  correctly honored or ignored, depending on the other circumstances.
### Other

- [pre-commit.ci] pre-commit autoupdate. [59e8634](https://github.com/callowayproject/bump-my-version/commit/59e863415d9a9f7ef082978ccee7b27c36112ea1)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.9.6 → v0.9.7](https://github.com/astral-sh/ruff-pre-commit/compare/v0.9.6...v0.9.7)

### Updates

- Updated documentation. [8162dd8](https://github.com/callowayproject/bump-my-version/commit/8162dd852b874e36626ad01ad72ea892499a9817)
    

## 0.32.2 (2025-02-22)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.32.1...0.32.2)

### Fixes

- Fixed coverage issue. [b0c46a3](https://github.com/callowayproject/bump-my-version/commit/b0c46a37ff265b5306abf005b5742a85c4281ea2)
    
- Refactor SCMInfo and Config imports. [49995c6](https://github.com/callowayproject/bump-my-version/commit/49995c6a9b2ad59c65cb6c1e27362b1254ce7fb4)
    
  - Fixes #300 incompatibility with Nuitka compiling
### Other

- [pre-commit.ci] pre-commit autoupdate. [b786638](https://github.com/callowayproject/bump-my-version/commit/b786638f152f2044d629c11f38f56713cc5c6dc4)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.9.4 → v0.9.6](https://github.com/astral-sh/ruff-pre-commit/compare/v0.9.4...v0.9.6)


## 0.32.1 (2025-02-10)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.32.0...0.32.1)

### Fixes

- Fix rich-click deprecation. [e1fb9fa](https://github.com/callowayproject/bump-my-version/commit/e1fb9fa52b466f70ebced8f192d4411a5804da60)
    
- Fix Python 3.8 support. [9b2d894](https://github.com/callowayproject/bump-my-version/commit/9b2d894c6ae3fc621789e52dd8b53e088d87f00f)
    

## 0.32.0 (2025-02-06)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.31.1...0.32.0)

### Fixes

- Refactor CLI config-file option to use @config_option decorator. [cd06cbd](https://github.com/callowayproject/bump-my-version/commit/cd06cbda61e54eea05b27eda734efc956d81a28a)
    
  Replaced the manual `--config-file` option setup with the `@config_option` decorator for cleaner and reusable configuration management. This change simplifies the code and enhances maintainability by consolidating the configuration logic.
### New

- Added pytest-localserver as a test dependency. [c84243d](https://github.com/callowayproject/bump-my-version/commit/c84243dba710feebdb571b93ea3cfb120703fd4e)
    
- Add ConfigOption for flexible configuration. [1625248](https://github.com/callowayproject/bump-my-version/commit/1625248c492c8719d6591af38d3ae2799e9f168f)
    
  Introduce `ConfigOption` and related utilities in `bumpversion.click_config` to handle configuration file paths or URLs. Includes tests for processing options, resolving paths/URLs, and handling errors in `resolve_conf_location` and `download_url`.
- Added httpx as a dependency. [450154e](https://github.com/callowayproject/bump-my-version/commit/450154ea19a321e0de44ef764e029abaafd1535a)
    
### Other

- [pre-commit.ci] pre-commit autoupdate. [17e8301](https://github.com/callowayproject/bump-my-version/commit/17e8301e5a3750b349c97cebcbcc5953f32f9af1)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.9.3 → v0.9.4](https://github.com/astral-sh/ruff-pre-commit/compare/v0.9.3...v0.9.4)

- Bump actions/setup-python in the github-actions group. [c0771b0](https://github.com/callowayproject/bump-my-version/commit/c0771b029073feb6a2a3c5e35170f25879b97bc0)
    
  Bumps the github-actions group with 1 update: [actions/setup-python](https://github.com/actions/setup-python).


  Updates `actions/setup-python` from 5.3.0 to 5.4.0
  - [Release notes](https://github.com/actions/setup-python/releases)
  - [Commits](https://github.com/actions/setup-python/compare/v5.3.0...v5.4.0)

  ---
  **updated-dependencies:** - dependency-name: actions/setup-python
dependency-type: direct:production
update-type: version-update:semver-minor
dependency-group: github-actions

  **signed-off-by:** dependabot[bot] <support@github.com>

### Updates

- Updated other subcommands with the new config_option. [279838a](https://github.com/callowayproject/bump-my-version/commit/279838af100dbf3ffc84f500710967944af05f46)
    
- Improve config resolution and add error handling for paths. [43f0435](https://github.com/callowayproject/bump-my-version/commit/43f04357788bfc11bec4c087e69366f8ba38c3e6)
    
  Refactor `process_value` to handle `None` values and raise a `BumpVersionError` for non-existent files. Update related tests to ensure correct behavior for missing, existing, and URL-based config paths. These changes enhance robustness and user feedback in handling configuration inputs.

## 0.31.1 (2025-02-02)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.31.0...0.31.1)

### Fixes

- Fix type hinting incompatibility in Python 3.9. [96b29f5](https://github.com/callowayproject/bump-my-version/commit/96b29f5ff561586e5dfb2da6e51172930bb717bc)
    
  Refactor to use Pathlike type alias for path representation

  Unified path type handling across the codebase by introducing the `Pathlike` type alias (`Union[str, Path]`). This improves readability and consistency in path-related functions and methods, reducing redundancy. Updated corresponding type annotations, imports, and tests accordingly.

## 0.31.0 (2025-02-01)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.30.2...0.31.0)

### New

- Add support for serializing SCMInfo in YAML, JSON, and output. [e8611b2](https://github.com/callowayproject/bump-my-version/commit/e8611b2f6a208b0949d0d148ad0395b3de92b68f)
    
  Ensure SCMInfo objects can be serialized into YAML and JSON formats, improving compatibility with configuration and output displays. Updated dumper functions and tests to reflect the new changes and include SCMInfo details in the configurations.
### Updates

- Update dependencies and adjust package versions. [b6ed073](https://github.com/callowayproject/bump-my-version/commit/b6ed07302799aab29aea142d9927e766a102e109)
    

## 0.30.2 (2025-02-01)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.30.1...0.30.2)

### Fixes

- Fix #388 - `python3.8` type hint compatibility. [5744f86](https://github.com/callowayproject/bump-my-version/commit/5744f86e8d5ff21e39d6e307b6bb26c70591c5e0)
    
  This should address the following error when running `bump-my-version`
  in a `python3.8` environment:

  ```
      def is_subpath(parent: Path | str, path: Path | str) -> bool:
  **typeerror:** unsupported operand type(s) for |: 'type' and 'type'

### Other

- [pre-commit.ci] pre-commit autoupdate. [ea3267a](https://github.com/callowayproject/bump-my-version/commit/ea3267a9114182f1ea9299ac468fc65a379005f1)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.9.2 → v0.9.3](https://github.com/astral-sh/ruff-pre-commit/compare/v0.9.2...v0.9.3)


## 0.30.1 (2025-01-30)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.30.0...0.30.1)

### Fixes

- Fixing issues with 3.9 compatibility. [cd2b193](https://github.com/callowayproject/bump-my-version/commit/cd2b193412b87ef47c3b9129b527eaa826429270)
    
- Fixes #284. Add UTF-8 encoding to subprocess.run in run_command. [6c856b6](https://github.com/callowayproject/bump-my-version/commit/6c856b6db40300de2ba0583bbd092b25d01b0004)
    
  Explicitly set the encoding to "utf-8" in the subprocess.run call to ensure consistent handling of command output. This prevents potential encoding-related issues when processing command results.

## 0.30.0 (2025-01-26)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.29.0...0.30.0)

### Fixes

- Fixed normalized paths in is_subpath. [d1c180b](https://github.com/callowayproject/bump-my-version/commit/d1c180b55cf19a5d3d8212bb102318f6b24a5cab)
    
- Fix formatting in docs. [5fe387c](https://github.com/callowayproject/bump-my-version/commit/5fe387ccf3ea8ce1a4e7b3b9d06f6f4446790cda)
    
### New

- Add handling for git path addition with new test coverage. [8ad5c82](https://github.com/callowayproject/bump-my-version/commit/8ad5c82182ec510ecc426656a8be1a41f3ce28f5)
    
  Enhances the `Git` class by adding the `add_path` method, improving control over tracked files. Includes comprehensive test cases to validate subpath handling, handle command failures, and ensure robustness against invalid inputs. Also includes minor refactoring with updated exception handling and code comments.
- Added tests for `utils.is_subpath`. [4e993ed](https://github.com/callowayproject/bump-my-version/commit/4e993ed423e05a8550342bd1d8b8ca82d4c17cb3)
    
- Add support for 'moveable_tags' configuration option. [2a2f1e6](https://github.com/callowayproject/bump-my-version/commit/2a2f1e6abe4c0d3e34440eacacc4b51bdb49f2df)
    
  This update introduces a new 'moveable_tags' field in the configuration model, with appropriate defaults. Test fixture files have been updated to reflect this change. This allows better handling of tags that can be relocated during versioning operations.
- Add support for 'moveable_tags' configuration option. [dd1efa5](https://github.com/callowayproject/bump-my-version/commit/dd1efa5026db2843f9ec06bcbb691a38a878fdc4)
    
  This update introduces a new 'moveable_tags' field in the configuration model, with appropriate defaults. Test fixture files have been updated to reflect this change. This allows better handling of tags that can be relocated during versioning operations.
- Added additional logging verbosity configuration in setup_logging. [2b420b8](https://github.com/callowayproject/bump-my-version/commit/2b420b82201b7b5ad129f4a6f64e99e446f0e492)
    
  Updated the logging verbosity levels to include formatting options for different verbosity levels. Added a new level (3) with detailed output including file path and line number. Refactored setup_logging to properly handle verbosity and log format settings.
### Other

- Merge remote-tracking branch 'origin/moving-tags' into moving-tags. [a2b7bd1](https://github.com/callowayproject/bump-my-version/commit/a2b7bd152a684234091c5e03c5dd55f50042fcd8)
    
- [pre-commit.ci] pre-commit autoupdate. [d03b1da](https://github.com/callowayproject/bump-my-version/commit/d03b1da16140836ef2c4c0daad12a616fedff498)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.8.6 → v0.9.2](https://github.com/astral-sh/ruff-pre-commit/compare/v0.8.6...v0.9.2)

- [pre-commit.ci] pre-commit autoupdate. [584711b](https://github.com/callowayproject/bump-my-version/commit/584711b7317a03683e442fdd908a55ee70846cca)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.8.4 → v0.8.6](https://github.com/astral-sh/ruff-pre-commit/compare/v0.8.4...v0.8.6)

- [pre-commit.ci] pre-commit autoupdate. [c583694](https://github.com/callowayproject/bump-my-version/commit/c58369411fea04f1979b5dd590862317cdccab9f)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.8.3 → v0.8.4](https://github.com/astral-sh/ruff-pre-commit/compare/v0.8.3...v0.8.4)

- Bump softprops/action-gh-release from 1 to 2 in the github-actions group. [787c241](https://github.com/callowayproject/bump-my-version/commit/787c241236c1f4da2512868135aca75a81558cca)
    
  Bumps the github-actions group with 1 update: [softprops/action-gh-release](https://github.com/softprops/action-gh-release).


  Updates `softprops/action-gh-release` from 1 to 2
  - [Release notes](https://github.com/softprops/action-gh-release/releases)
  - [Changelog](https://github.com/softprops/action-gh-release/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/softprops/action-gh-release/compare/v1...v2)

  ---
  **updated-dependencies:** - dependency-name: softprops/action-gh-release
dependency-type: direct:production
update-type: version-update:semver-major
dependency-group: github-actions

  **signed-off-by:** dependabot[bot] <support@github.com>

### Updates

- Updated some tests. [4013d86](https://github.com/callowayproject/bump-my-version/commit/4013d863c3762fee1802b012689af62a0184d85a)
    
- Remove legacy SCM implementation and add new SCM tests. [ddbe21e](https://github.com/callowayproject/bump-my-version/commit/ddbe21e4a29963caa063e554b84592d4c7a8222f)
    
  Replaced the outdated `scm_old.py` with a focused and updated SCM implementation. Added extensive tests for the new `SCMInfo` behavior, path handling, and commit/tag logic, ensuring robust functionality for Git and Mercurial. Updated fixtures and test configurations accordingly.
- Rename `scm.py` to `scm_old.py` and add new utility functions. [dac965d](https://github.com/callowayproject/bump-my-version/commit/dac965d485802668fedc8c6e329bf10d04f7c795)
    
  Refactored SCM-related imports to use the renamed `scm_old.py` for better module organization. Introduced `is_subpath` utility to simplify path checks and added support for moveable tags in version control systems. These changes improve code structure and extend functionality for tagging.

## 0.29.0 (2024-12-19)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.28.3...0.29.0)

### New

- Add support for specifying current version in `do_show`. [878197f](https://github.com/callowayproject/bump-my-version/commit/878197f186defabf036ddeb940eb91dfed172d0b)
    
  This update introduces a `--current-version` option to the `show` command and passes it into the `do_show` function. If provided, the `current_version` is added to the configuration, allowing more control over version display or manipulation.
### Updates

- Update README to clarify pre_n handling with distance_to_latest_tag. [c027879](https://github.com/callowayproject/bump-my-version/commit/c0278791fad3de1c3d66ab06b49118b2b8314933)
    
  Revised the `parse` expression to exclude `pre_n` and updated `serialize` examples to use `distance_to_latest_tag` instead. Fixes #272

## 0.28.3 (2024-12-17)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.28.2...0.28.3)

### Fixes

- Fixed tag-name output. [0e773ec](https://github.com/callowayproject/bump-my-version/commit/0e773ecc5812a066b8c0f049a597e092722f138b)
    
- Fixed PACKAGE env variable. [76c31c4](https://github.com/callowayproject/bump-my-version/commit/76c31c419759d15d8ea74fce94cee5353056ba76)
    
- Fixed syntax errors in scripts. [56dfac0](https://github.com/callowayproject/bump-my-version/commit/56dfac09a191d3a519bf2de6c0a0b6d0c4e456ba)
    
- Fixes missing runs-on in workflow. [5fe8ce5](https://github.com/callowayproject/bump-my-version/commit/5fe8ce5b1af1d0c915ee7937b664202fec342dca)
    
- Fix: resolve config path to align with the actual repository root. [c872315](https://github.com/callowayproject/bump-my-version/commit/c8723155465cf42d97ef505c54ee983b9880eefb)
    
- Fixed docs. [1d26b55](https://github.com/callowayproject/bump-my-version/commit/1d26b55dd1f37f9559daa6a4ac3a0dbdf167099c)
    
- Fixed doc generation. [aa95762](https://github.com/callowayproject/bump-my-version/commit/aa95762a30648c1afb0e26176041f26a25c26dab)
    
### New

- Added release workflow step. [d56650a](https://github.com/callowayproject/bump-my-version/commit/d56650a26d878e4cfab331004cc7d383bf955131)
    
- Added write permissions for contents in github action. [85f19df](https://github.com/callowayproject/bump-my-version/commit/85f19dfeb7c751fa6ba5a06b79694ca27529da2f)
    
### Other

- Debugging the release workflow. [db2eb9e](https://github.com/callowayproject/bump-my-version/commit/db2eb9ef177d7fcd55c832a3f1f9993b7b19bd4a)
    
- [pre-commit.ci] pre-commit autoupdate. [37c21a4](https://github.com/callowayproject/bump-my-version/commit/37c21a4bc668935a98de931762d1a6b6ffc17311)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.8.2 → v0.8.3](https://github.com/astral-sh/ruff-pre-commit/compare/v0.8.2...v0.8.3)

- Bump actions/setup-python in the github-actions group. [3dd6666](https://github.com/callowayproject/bump-my-version/commit/3dd666668ad099a9ee712bf4679296c7b1df16fb)
    
  Bumps the github-actions group with 1 update: [actions/setup-python](https://github.com/actions/setup-python).


  Updates `actions/setup-python` from 5.1.1 to 5.3.0
  - [Release notes](https://github.com/actions/setup-python/releases)
  - [Commits](https://github.com/actions/setup-python/compare/v5.1.1...v5.3.0)

  ---
  **updated-dependencies:** - dependency-name: actions/setup-python
dependency-type: direct:production
update-type: version-update:semver-minor
dependency-group: github-actions

  **signed-off-by:** dependabot[bot] <support@github.com>

### Updates

- Removed debug stuff. [c0e7ad4](https://github.com/callowayproject/bump-my-version/commit/c0e7ad4b84bcac847039b02ed245b3b9b2b37200)
    

## 0.28.2 (2024-12-14)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.28.1...0.28.2)

### Fixes

- Fixed Ruff errors and workflow permissions. [11c1e42](https://github.com/callowayproject/bump-my-version/commit/11c1e42954281dac9febcac80f10d3775fcfcbbc)
    
- Fixed more uv run workflows. [d829276](https://github.com/callowayproject/bump-my-version/commit/d829276347c5391a9d2233e56e30300b69172d14)
    
- Fixed installation of test dependencies. [cbf10f2](https://github.com/callowayproject/bump-my-version/commit/cbf10f23c33e8d62d4851f11579f93a359553bff)
    
- Fixed issue with python install. [6e2da8d](https://github.com/callowayproject/bump-my-version/commit/6e2da8d54ad79ed3b46976af57d3721b3e50b370)
    
- Fixed GitHub workflows. [86a0a3b](https://github.com/callowayproject/bump-my-version/commit/86a0a3bdbebbde81e17df687bc4d7303d27d490f)
    
- Refactor warning display with Rich formatting. [2b7c905](https://github.com/callowayproject/bump-my-version/commit/2b7c905c792e1cbe22040a5ba890c4440990f99b)
    
  Replace plain click-based warnings with styled Rich panels for better visibility. This enhances user experience by providing clearer and more visually organized warnings.
- Refactored dependencies config. [39fed07](https://github.com/callowayproject/bump-my-version/commit/39fed070669258650cdf5d2a4c180399bf256ad6)
    
  - Changed `project.optional-dependencies` to `dependency-groups`
### New

- Add branch selection for github-push-action. [4ecc07c](https://github.com/callowayproject/bump-my-version/commit/4ecc07cefa435964d0b1476cf95916c56885bdce)
    
### Other

- [pre-commit.ci] auto fixes from pre-commit.com hooks. [183a6f2](https://github.com/callowayproject/bump-my-version/commit/183a6f29a8781eb76029f677aa83678a2ed1d505)
    
  for more information, see https://pre-commit.ci
- [pre-commit.ci] pre-commit autoupdate. [075d0da](https://github.com/callowayproject/bump-my-version/commit/075d0da09b12c91be27ac3f28ba587c308e0c78e)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.7.4 → v0.8.2](https://github.com/astral-sh/ruff-pre-commit/compare/v0.7.4...v0.8.2)

- [pre-commit.ci] pre-commit autoupdate. [6ed9f0e](https://github.com/callowayproject/bump-my-version/commit/6ed9f0e03e83407d8dca0cdf8d9ec920d8479564)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.7.1 → v0.7.4](https://github.com/astral-sh/ruff-pre-commit/compare/v0.7.1...v0.7.4)

- Bump codecov/codecov-action from 4 to 5 in the github-actions group. [4194af8](https://github.com/callowayproject/bump-my-version/commit/4194af89ca515f894447180152c87ef1f3c9be2a)
    
  Bumps the github-actions group with 1 update: [codecov/codecov-action](https://github.com/codecov/codecov-action).


  Updates `codecov/codecov-action` from 4 to 5
  - [Release notes](https://github.com/codecov/codecov-action/releases)
  - [Changelog](https://github.com/codecov/codecov-action/blob/main/CHANGELOG.md)
  - [Commits](https://github.com/codecov/codecov-action/compare/v4...v5)

  ---
  **updated-dependencies:** - dependency-name: codecov/codecov-action
dependency-type: direct:production
update-type: version-update:semver-major
dependency-group: github-actions

  **signed-off-by:** dependabot[bot] <support@github.com>

### Updates

- Updated uv.lock. [09b825b](https://github.com/callowayproject/bump-my-version/commit/09b825b57f71ffdd08ddd50c655097812d5b8987)
    
- Update setup section in contributing guide. [4bc279b](https://github.com/callowayproject/bump-my-version/commit/4bc279b7946b5eebf6ce9509ff02636bed6b83f9)
    
  Use extra dependencies specifier (referring to pyproject.toml) in the instructions, instead of requirements txt files (which were removed in previous commits).

## 0.28.1 (2024-11-03)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.28.0...0.28.1)

### Fixes

- Fix format arg help text for show command. [cf65ec2](https://github.com/callowayproject/bump-my-version/commit/cf65ec27ae68e2bf5b397591ff00fc86d2eab21f)
    
### Other

- [pre-commit.ci] pre-commit autoupdate. [9fb0347](https://github.com/callowayproject/bump-my-version/commit/9fb03472d5cfa16281e2e3f049b660dc503eb167)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.6.9 → v0.7.1](https://github.com/astral-sh/ruff-pre-commit/compare/v0.6.9...v0.7.1)

- Output hooks scripts by default. [0a042aa](https://github.com/callowayproject/bump-my-version/commit/0a042aaa8fabd5c64ea5ffd153c959ccdacf80c6)
    
- Skip scm tests if the command is not installed. [2e68517](https://github.com/callowayproject/bump-my-version/commit/2e68517f890e1da7520486baf102c559ed2f40ea)
    

## 0.28.0 (2024-10-16)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.27.0...0.28.0)

### New

- Added container labels and version hooks. [d4cb8f2](https://github.com/callowayproject/bump-my-version/commit/d4cb8f2231dbe5faa4bc68b769a00ea199beed8e)
    
- Add Docker support and configure Dependabot for Docker updates. [0315db4](https://github.com/callowayproject/bump-my-version/commit/0315db458db260653180ba95a106cecad8eea425)
    
  Introduce a Dockerfile for containerized environments and add a .dockerignore file to exclude unnecessary files. Also, update dependabot.yml to include daily checks for Docker image updates.
- Add `inputs` section in GHA workflow example. [813e7f5](https://github.com/callowayproject/bump-my-version/commit/813e7f526479e278ab12db2bc8a873c9f7fc2dd7)
    
### Other

- Switch from ADD to COPY in Dockerfile. [a5fc5c0](https://github.com/callowayproject/bump-my-version/commit/a5fc5c0e595530650059dd6ab821927933f0ef58)
    
  This change updates the Dockerfile to use the COPY instruction instead of ADD. COPY is preferred when only copying files because it is more explicit and simpler.
- [pre-commit.ci] pre-commit autoupdate. [7c48f98](https://github.com/callowayproject/bump-my-version/commit/7c48f987fd782b1c5665e49dd9e0e491416d39cd)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.6.8 → v0.6.9](https://github.com/astral-sh/ruff-pre-commit/compare/v0.6.8...v0.6.9)

### Updates

- Changed dependency manager to uv. [cce9e1d](https://github.com/callowayproject/bump-my-version/commit/cce9e1dead3507791e866c0daf5e3f6818a55e14)
    

## 0.27.0 (2024-10-06)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.26.1...0.27.0)

### Fixes

- Fixed test to look for warning logs. [538c420](https://github.com/callowayproject/bump-my-version/commit/538c4205c1d711daf732027719f5fa67e0418d5e)
    
- Refactor and enhance error handling. [c84bfa7](https://github.com/callowayproject/bump-my-version/commit/c84bfa7dcb5914c4adbfa9213d377fd705949501)
    
  Updated subprocess calls to disable check, refined lint configurations, fixed type annotations and exceptions, and improved dictionary path validation.
### New

- Add HookError for failed hook execution with tests. [39fc233](https://github.com/callowayproject/bump-my-version/commit/39fc233163222070d5a7c4549e59ea2b292c6ba5)
    
  Raise HookError when a hook script exits with a non-zero status. Modified logger to display warnings instead of debug messages in such scenarios. Added tests to ensure exceptions are raised for failed hooks.
### Other

- [pre-commit.ci] pre-commit autoupdate. [130478d](https://github.com/callowayproject/bump-my-version/commit/130478d664e7ed9abe88a9882b00e7d5e4a5c37a)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.6.5 → v0.6.7](https://github.com/astral-sh/ruff-pre-commit/compare/v0.6.5...v0.6.7)

- Create FUNDING.yml. [2bda200](https://github.com/callowayproject/bump-my-version/commit/2bda20037cf10d714fb906fa05b73103c56bb6c3)
    

## 0.26.1 (2024-09-14)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.26.0...0.26.1)

### Fixes

- Fixed missing new version info in some hook environments. [24a9bdc](https://github.com/callowayproject/bump-my-version/commit/24a9bdc0c8264b1d756d444367f4e6282f38c07f)
    
  Introduce the `new_version_env` function and update existing functions (`get_setup_hook_env` and `get_pre_commit_hook_env`) to include new version environment variables. Added new tests for verifying the inclusion of OS, SCM, current, and new version information in hook environments.
### New

- Add current and previous version outputs to the GHA. [0650ca8](https://github.com/callowayproject/bump-my-version/commit/0650ca8cd4d1a4d155616865ef2cbac39c60c616)
    
- Add environment variable to README example. [88c9790](https://github.com/callowayproject/bump-my-version/commit/88c9790b4cac778d17abe8e3bbeead7adad11274)
    
- Add GitHub action with support for commit/tag push workflow trigger. [2cdb742](https://github.com/callowayproject/bump-my-version/commit/2cdb7420264810396b42d35827291d1dc080d416)
    
### Other

- [pre-commit.ci] pre-commit autoupdate. [d21d6df](https://github.com/callowayproject/bump-my-version/commit/d21d6df85afadf9a4a38f538ad75bda0cdcbea41)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.6.2 → v0.6.4](https://github.com/astral-sh/ruff-pre-commit/compare/v0.6.2...v0.6.4)

- [pre-commit.ci] pre-commit autoupdate. [b6773ac](https://github.com/callowayproject/bump-my-version/commit/b6773acf3cb57d51479fad0a0ab842ebcbc416a1)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.5.7 → v0.6.2](https://github.com/astral-sh/ruff-pre-commit/compare/v0.5.7...v0.6.2)

### Updates

- Updated pre-commit versions. [6f5d56b](https://github.com/callowayproject/bump-my-version/commit/6f5d56b2e5a55171d79a4c14d06f3e15e9174711)
    
- Update example to better showcase the GHA capabilities. [e3ff9a1](https://github.com/callowayproject/bump-my-version/commit/e3ff9a1bf201c440037d9d26b01c7da9941d32c6)
    
- Update README.md. [f280371](https://github.com/callowayproject/bump-my-version/commit/f28037120a978034a8910600eb1826a653c706e2)
    

## 0.26.0 (2024-08-19)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.25.4...0.26.0)

### Fixes

- Fix issues with environment test on windows. [04a98d0](https://github.com/callowayproject/bump-my-version/commit/04a98d00793e80bca2c11e354672168a8a6de9cd)
    
- Fixed redundant tests for SCM. [e50e991](https://github.com/callowayproject/bump-my-version/commit/e50e991fe481ff25791a25987e4c4af133f50817)
    
### New

- Added hook suite documentation. [b73a6e1](https://github.com/callowayproject/bump-my-version/commit/b73a6e120122d1fe28e52c2b9b13eeed95f20a51)
    
- Added hooks to bump command. [3b638e0](https://github.com/callowayproject/bump-my-version/commit/3b638e088edee304d2f0a8305e332eff2eba85e0)
    
- Added tests for hooks. [8446567](https://github.com/callowayproject/bump-my-version/commit/844656717e3799fc418e76ef2b9e3b12116ca0d5)
    
- Add hooks configuration fields. [d6b24f0](https://github.com/callowayproject/bump-my-version/commit/d6b24f01b22fcbfe719ae9954c47e03ec1df3072)
    
  Introduced `setup_hooks`, `pre_bump_hooks`, and `post_bump_hooks` fields to configuration models. Updated corresponding test fixtures to verify these new fields.
- Add current_tag field to scm_info. [304c599](https://github.com/callowayproject/bump-my-version/commit/304c59985d5f71f44754615fee2ded600de237b0)
    
  Updated the scm_info structure to include a new field, current_tag, across various configuration files and source code. This ensures that the current tag is tracked and represented in the output formats correctly.
### Other

- Enhance hook handling and testing across hook types. [49f1953](https://github.com/callowayproject/bump-my-version/commit/49f1953c476a09cc9e7332af6347914935ee982c)
    
  - Introduced unified handling for setup, pre-commit, and post-commit hooks, including dry-run support.

  - Added comprehensive tests to ensure the correct behavior for all hook phases, including cases where no hooks are specified or in dry run mode.

  - Updated environment setup to use a common version environment function.
- [pre-commit.ci] pre-commit autoupdate. [4342198](https://github.com/callowayproject/bump-my-version/commit/434219853b2824cbfff926e3cc79aa1b0ba10b3d)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.5.6 → v0.5.7](https://github.com/astral-sh/ruff-pre-commit/compare/v0.5.6...v0.5.7)

### Updates

- Changed the terminology for hooks. [049b470](https://github.com/callowayproject/bump-my-version/commit/049b4704f245f4ec5c258eb5fc2f10e2b564655a)
    
  Change pre-bump and post-bump to pre-commit and post-commit to better indicate their order of operations.

## 0.25.4 (2024-08-14)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.25.3...0.25.4)

### Fixes

- Fixed terminology in tests. [0338da2](https://github.com/callowayproject/bump-my-version/commit/0338da2b674e3f960fd026485a9ddbb2648dff30)
    
  Updated test parameter and assertion messages to use "version component" instead of "version part" for clarity and consistency. This change affects the test cases that detect bad or missing version inputs.
- Fixed documentation layout. [57958ea](https://github.com/callowayproject/bump-my-version/commit/57958eaed527447bd63e100c08763c8810e4dc8e)
    
- Fixed inconsistent terms in docstrings. [dfdf23e](https://github.com/callowayproject/bump-my-version/commit/dfdf23e04fe6a75341a8943f674c79897f5e0712)
    
  - Switched from using both version parts and version components to simply version components.
### Updates

- Updated documentation. [5aedd64](https://github.com/callowayproject/bump-my-version/commit/5aedd64391ffc6e49ec6cb4ddace847a31ff72fe)
    
- Removed old requirements. [ec95eef](https://github.com/callowayproject/bump-my-version/commit/ec95eef8ddef229eb84577cfac301bf92fd8eceb)
    

## 0.25.3 (2024-08-13)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.25.2...0.25.3)

### Fixes

- Refactor version parsing in visualize function. [5f25300](https://github.com/callowayproject/bump-my-version/commit/5f25300b007cee294a43af64eb970e3e100931a8)
    
  Simplify the version parsing process by utilizing the raise_error parameter in the parse method, removing the need for a separate error check. This change ensures that parsing errors are immediately raised and handled cleanly within the visualize function.
- Refactor and rename `version_part` to `versioning.version_config`. [5b90817](https://github.com/callowayproject/bump-my-version/commit/5b90817e6210f983c691bd06008afa065c961c4f)
    
  Moved `version_part.py` to `versioning/version_config.py` and updated all import statements accordingly. Enhanced error handling in `VersionConfig` by adding `raise_error` flag and relevant exception raising for invalid version strings. Refined tests to reflect these changes.
- Fix version visualization and add verbose logging. [ad46978](https://github.com/callowayproject/bump-my-version/commit/ad469783c0507bf7e4160cf131d2b73b494c52e8)
    
  Raise an exception for unparsable versions and aggregate visualization output in a list before printing. Add a verbose logging option to the `show_bump` command for detailed logging control.

## 0.25.2 (2024-08-11)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.25.1...0.25.2)

### Fixes

- Fix JSON serialization. [d3f3022](https://github.com/callowayproject/bump-my-version/commit/d3f3022bd4c8b8d6e41fa7b5b6ccfc2aa6cf7878)
    
  Extended the default_encoder function to handle Path objects by converting them to their string representation. This ensures that Path objects can be properly serialized to JSON format.

## 0.25.1 (2024-08-07)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.25.0...0.25.1)

### Fixes

- Fixes mypy pre-commit checking. [f7d0909](https://github.com/callowayproject/bump-my-version/commit/f7d0909deb8d0cf06607c4d51090ca23f7d92664)
    
- Fixes repository path checks. [ff3f72a](https://github.com/callowayproject/bump-my-version/commit/ff3f72a9a922dfbb61eea9325fc9dba7c12c7f62)
    
  Checked for relative paths when determining if the file was part of the repo or not.
- Fixed test to use globs. [72f9841](https://github.com/callowayproject/bump-my-version/commit/72f9841a9628e26c6cf06518b0428d3990a08421)
    
### Other

- [pre-commit.ci] pre-commit autoupdate. [58cc73e](https://github.com/callowayproject/bump-my-version/commit/58cc73ed041f978fddd9f81e995901596f6ac722)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.5.5 → v0.5.6](https://github.com/astral-sh/ruff-pre-commit/compare/v0.5.5...v0.5.6)


## 0.25.0 (2024-08-06)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.24.3...0.25.0)

### Fixes

- Refactor error handling and improve logging in utils. [890b692](https://github.com/callowayproject/bump-my-version/commit/890b6922eb13cf36049029e3afe6778cfe0116f9)
    
  Extracted error formatting to a dedicated function and applied it across the codebase. Improved command path handling in `add_path` and enhanced test coverage with necessary imports and logging configurations.
- Fix dictionary merging in SCMInfo. [5fb5ef2](https://github.com/callowayproject/bump-my-version/commit/5fb5ef2337eb12af7c561d834fb6fd33dd053ce4)
    
  Replaced the bitwise OR operator with the update method for merging dictionaries for 3.8 support
- Refactor SCM info retrieval and config file update checks. [500ecd3](https://github.com/callowayproject/bump-my-version/commit/500ecd37e8603ee70253295140ba25d2b28c505d)
    
  Replaced ChainMap with MutableMapping in function signatures and types. Enhanced SCM info handling by splitting code into dedicated methods for commit and revision info retrieval. Added logic to prevent config file updates when the file is outside the repo and implemented corresponding test.
### New

- Add repository_root field and refactor subprocess handling. [25670d0](https://github.com/callowayproject/bump-my-version/commit/25670d0ecfd0b6dc7f7228af157e3a6361a0f9d9)
    
  Introduced the `repository_root` field to store the root path of the repository in the data classes. Refactored subprocess handling to use a new `run_command` utility for improved readability and error handling consistency. Removed unnecessary dependency from `.pre-commit-config.yaml` to streamline dependencies.
### Other

- Simplify run_command return type. [b91224e](https://github.com/callowayproject/bump-my-version/commit/b91224e1bf3628d42d2ab5c26929c274b7e7884e)
    
  Changed the return type of run_command from CompletedProcess[str] to CompletedProcess. This was done to remove unnecessary type specificity and ensure compatibility with different Python versions. The update maintains functionality and improves code readability.
- [pre-commit.ci] pre-commit autoupdate. [e0ba544](https://github.com/callowayproject/bump-my-version/commit/e0ba54435e6ffe1714d4b24f1a483c9e64b7c3c7)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.5.2 → v0.5.5](https://github.com/astral-sh/ruff-pre-commit/compare/v0.5.2...v0.5.5)


## 0.24.3 (2024-07-17)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.24.2...0.24.3)

### Fixes

- Fix KeyError in TOML file handling. [f3c328a](https://github.com/callowayproject/bump-my-version/commit/f3c328a6b11c5be2e285453714d4e7a3148b1078)
    
  The code has been updated to handle KeyErrors when updating TOML files. If a KeyError is raised, it's now caught and managed depending on the file_change attributes 'ignore_missing_file' or 'ignore_missing_version'. This aims to provide more robust handling of edge cases in TOML files. In addition, a new test case has been added to ensure current version is not required in the configuration.

  Fixes #212
### Other

- [pre-commit.ci] pre-commit autoupdate. [536c7b1](https://github.com/callowayproject/bump-my-version/commit/536c7b122aa57576fa770b59ca093fc4444bd402)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.4.10 → v0.5.2](https://github.com/astral-sh/ruff-pre-commit/compare/v0.4.10...v0.5.2)


## 0.24.2 (2024-07-03)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.24.1...0.24.2)

### Fixes

- Fixed tag version extraction. [67eea3d](https://github.com/callowayproject/bump-my-version/commit/67eea3ddd1dbf0f64d610bc46cf22e638925c26f)
    
  The output of `git describe` uses `-` as a delimiter. Parsing tags caused splits in the parsing of version numbers.

  This joins all the remaining parts of the `git describe` with a `-`.
- Fixed pydoclint configuration. [0386073](https://github.com/callowayproject/bump-my-version/commit/0386073d7c298a2bd159fc2c59d08689557e9224)
    

## 0.24.1 (2024-06-26)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.24.0...0.24.1)

### Fixes

- Refactor error handling in SCM and add error handling test. [7ca6356](https://github.com/callowayproject/bump-my-version/commit/7ca63568ef1db9bb7ac3508d02f897c2415b5a5c)
    
  This commit includes a new test in test_scm.py to verify the correct formatting and raising of subprocess errors in the SCM module. Additionally, the subprocess error handling has been refactored in the SCM module to include a new method, format_and_raise_error, for improved code readability and reusability.
### Other

- [pre-commit.ci] pre-commit autoupdate. [60acc2d](https://github.com/callowayproject/bump-my-version/commit/60acc2d42b0acd1f7e6222b27ecdb349346784cf)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.4.9 → v0.4.10](https://github.com/astral-sh/ruff-pre-commit/compare/v0.4.9...v0.4.10)


## 0.24.0 (2024-06-25)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.23.0...0.24.0)

### New

- Add VersionNotFoundError test in test_bump.py. [cb050a8](https://github.com/callowayproject/bump-my-version/commit/cb050a87ae26421024025010a38d9e9a0cdd6f44)
    
  The code in test_bump.py file has been modified to include a test for VersionNotFoundError exception. This ensures that the implementation properly handles cases where a specified version could not be found.
- Add test for no commit on modification error. [7527029](https://github.com/callowayproject/bump-my-version/commit/75270290e412dacf8ce30586059f919d0cf53838)
    
  A test has been added to the bumpversion library to ensure that no commit and tag is made if there is an error modification. Specifically, the test checks the "do_bump" function and asserts that "mock_commit_and_tag" and "mock_update_config_file" are not called under these conditions.
### Other

- [pre-commit.ci] pre-commit autoupdate. [0e3a154](https://github.com/callowayproject/bump-my-version/commit/0e3a154b71b40bb4cae31ec72e35156fef423919)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.4.8 → v0.4.9](https://github.com/astral-sh/ruff-pre-commit/compare/v0.4.8...v0.4.9)

### Updates

- Improve error message for SCM command failures. [8f72f86](https://github.com/callowayproject/bump-my-version/commit/8f72f868045d5f715e11404ed82455c8d5de6eca)
    
  The error message for failures in the SCM command execution has been enhanced. Now it displays not only the command's return code but also the standard output and error, improving the debugging process.

## 0.23.0 (2024-06-14)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.22.0...0.23.0)

### Fixes

- Refactor valid_bumps and invalid_bumps to include_bumps and exclude_bumps. [2df57cc](https://github.com/callowayproject/bump-my-version/commit/2df57cc05433c3d2698afa6a76028af6bea7d7fc)
    
  The configuration parameters `valid_bumps` and `invalid_bumps` were renamed to `include_bumps` and `exclude_bumps` respectively. This new naming better denotes their function, and the changes were consistently applied across all related files and tests. Numerous fixture outputs were also updated to reflect these changes.
- Fixed spelling in CODE_OF_CONDUCT.md. [254ea44](https://github.com/callowayproject/bump-my-version/commit/254ea44c963352a74965eb602e0c4dd56eea665a)
    
### New

- Add file filtering based on valid and invalid bumps. [f9f7f96](https://github.com/callowayproject/bump-my-version/commit/f9f7f96bd5e467666b9a59e3fa8a6dedfaca838a)
    
  This commit introduces the ability to filter files based on whether the specified bump type is valid or not. It adds `valid_bumps` and `invalid_bumps` lists in the file configurations and adjusts the bumping process to consider these configurations. Tests are updated to reflect these new handling of valid and invalid bumps.
- Add new files to .gitignore. [34e4dc1](https://github.com/callowayproject/bump-my-version/commit/34e4dc14b3948a01552685402c0ca71ae23d5975)
    
  Several new file types have been added to .gitignore for ignoring during commits. These include '.python-version', 'requirements-dev.lock', and 'requirements.lock' files.
- Add valid_bumps and invalid_bumps to file configuration. [9458851](https://github.com/callowayproject/bump-my-version/commit/94588518ae96b3c1bdc996d61cf6cdc1c684ac1d)
    
  Updated the configuration file model to support valid_bumps and invalid_bumps. This feature provides control over which version section updates can trigger file changes. Adjusted various test fixtures and cleaned up tests to match these changes. Also, some updates were made to the documentation accordingly.
### Other

- [pre-commit.ci] pre-commit autoupdate. [e44f6af](https://github.com/callowayproject/bump-my-version/commit/e44f6af91dd68c563b2974f21c8d00dc78e42896)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.4.4 → v0.4.8](https://github.com/astral-sh/ruff-pre-commit/compare/v0.4.4...v0.4.8)

### Updates

- Update documentation for clarification. [2224808](https://github.com/callowayproject/bump-my-version/commit/2224808b652143c5179c49848cf2ce91d26ecdbe)
    
  The changes made update the wording in the documentation to clarify the roles of `include_bumps` and `exclude_bumps` in the bump-my-version configuration. Additionally, unnecessary repetition was removed and overlapping examples were also corrected.
- Update docs/reference/configuration.md. [7c801c0](https://github.com/callowayproject/bump-my-version/commit/7c801c0be10f8031cbf04814bc0ead407bb9477c)
    
  **co-authored-by:** wkoot <3715211+wkoot@users.noreply.github.com>


## 0.22.0 (2024-06-11)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.21.1...0.22.0)

### New

- Add extensive documentation for the 'show' subcommand. [91409d8](https://github.com/callowayproject/bump-my-version/commit/91409d81d647a6dc1e39d3cfbc1e0e95a5c67a82)
    
  This commit adds extensive documentation for the `show` subcommand in the program's reference. It also includes smaller updates and corrections to other parts of the documentation. An in-depth example usage of `show` is added both to the dedicated `show.md` file and in the function's docstring.
### Updates

- Renamed version workflow to release. [68f9eee](https://github.com/callowayproject/bump-my-version/commit/68f9eee8f953c23d30b8ef77a3cedf9355ce55a0)
    

## 0.21.1 (2024-05-16)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.21.0...0.21.1)

### Other

- [pre-commit.ci] auto fixes from pre-commit.com hooks. [1b57c2b](https://github.com/callowayproject/bump-my-version/commit/1b57c2b3e5b687e541d611b88b3d5fae4ce8826b)
    
  for more information, see https://pre-commit.ci
- [pre-commit.ci] pre-commit autoupdate. [e813eda](https://github.com/callowayproject/bump-my-version/commit/e813edad628803cd4c9f59ff2b8303b4d779756a)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.4.3 → v0.4.4](https://github.com/astral-sh/ruff-pre-commit/compare/v0.4.3...v0.4.4)

- [pre-commit.ci] pre-commit autoupdate. [05a0dd6](https://github.com/callowayproject/bump-my-version/commit/05a0dd65f31f3962e1ff4d2ee03ee99b2062ea5f)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.4.2 → v0.4.3](https://github.com/astral-sh/ruff-pre-commit/compare/v0.4.2...v0.4.3)

### Updates

- Update README.md. [cad7096](https://github.com/callowayproject/bump-my-version/commit/cad7096c615f646a75c5d23bae745cd1a8e0adb5)
    

## 0.21.0 (2024-05-01)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.20.3...0.21.0)

### Fixes

- Fixed a bug in the glob tests. [1041fe9](https://github.com/callowayproject/bump-my-version/commit/1041fe9b363fc79cb0bb95c301c1c9badb5da9cc)
    
  Was not properly looking in the correct relative directories.
- Fixed test for Windows glob paths. [ea45c4c](https://github.com/callowayproject/bump-my-version/commit/ea45c4c4d156c1b0807a019f4b04982fda195e8f)
    
- Fixed exclusion logic with wcmatch. [1c391be](https://github.com/callowayproject/bump-my-version/commit/1c391beca888797ce669a947373bca907c78dbfa)
    
- Refactored glob matching to use the wcmatch library. [bbf4ae0](https://github.com/callowayproject/bump-my-version/commit/bbf4ae0c9b4c77d78fb534f166c0165dffcb8c76)
    
### New

- Adds `glob_exclude` file specification parameter. [420e3bd](https://github.com/callowayproject/bump-my-version/commit/420e3bd42bf01c3c540ef72c67b55354fd8780e7)
    
  User can prune the files resolved via the `glob` parameter.

  Fixes #184
### Other

- [pre-commit.ci] pre-commit autoupdate. [ce02aa7](https://github.com/callowayproject/bump-my-version/commit/ce02aa759e69ee823b6844626ed2db3dd858d54c)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.4.1 → v0.4.2](https://github.com/astral-sh/ruff-pre-commit/compare/v0.4.1...v0.4.2)


## 0.20.3 (2024-04-26)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.20.2...0.20.3)

### Fixes

- Fixed test logging setup. [3777f27](https://github.com/callowayproject/bump-my-version/commit/3777f2750a146a698ed0d15edd88c82f73e35354)
    
- Fixed the indentation problem. [ec3cd99](https://github.com/callowayproject/bump-my-version/commit/ec3cd998dfa7eaff678262163629abac73640c86)
    
  - Added a dedent when a file does not match the change pattern.
  - Fixes #181
### Other

- [pre-commit.ci] pre-commit autoupdate. [e916f87](https://github.com/callowayproject/bump-my-version/commit/e916f87b519266f62e4b504752bb51bb40fe3a08)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.3.7 → v0.4.1](https://github.com/astral-sh/ruff-pre-commit/compare/v0.3.7...v0.4.1)


## 0.20.2 (2024-04-23)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.20.1...0.20.2)

### Fixes

- Fixed the rendering of numeric version components. [c522c75](https://github.com/callowayproject/bump-my-version/commit/c522c75e9b51cbcf09e7a1a41a0b6d210a3b44be)
    
  - Numeric version components now will attempt to render its value as an integer and fall back to the parsed value.
- Fixed code block in the README. [b4ff9f3](https://github.com/callowayproject/bump-my-version/commit/b4ff9f31557cf39ab3fdf4199c4fbddd03a78bbd)
    
### Other

- [pre-commit.ci] pre-commit autoupdate. [9b09da8](https://github.com/callowayproject/bump-my-version/commit/9b09da8f93d50886f60a63a01ae10a1336ac766e)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.3.5 → v0.3.7](https://github.com/astral-sh/ruff-pre-commit/compare/v0.3.5...v0.3.7)


## 0.20.1 (2024-04-13)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.20.0...0.20.1)

### Fixes

- Fix typos discovered by codespell. [d5c33a3](https://github.com/callowayproject/bump-my-version/commit/d5c33a3e5fe8b7127f7f8473e388c5470e397a82)
    
- Fixed relative references. [2aa1011](https://github.com/callowayproject/bump-my-version/commit/2aa10118e22bced8cc7a1f4a1172c1fbf1aa51d9)
    
- Refactored the docs. [b63a9e7](https://github.com/callowayproject/bump-my-version/commit/b63a9e780ac84e5d1604b6e7ec1bb6205c64ab43)
    
### Other

- [pre-commit.ci] pre-commit autoupdate. [f438bc6](https://github.com/callowayproject/bump-my-version/commit/f438bc677fc6bd3df71dd6c39ef0dfb95e9fc7d3)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.3.4 → v0.3.5](https://github.com/astral-sh/ruff-pre-commit/compare/v0.3.4...v0.3.5)

- Pre-commit: Discover typos with codespell. [2509fc7](https://github.com/callowayproject/bump-my-version/commit/2509fc7690406f95dfc34a6d5e3eeb41205f8569)
    
  Related to:
  * #168
- [pre-commit.ci] pre-commit autoupdate. [be5cb79](https://github.com/callowayproject/bump-my-version/commit/be5cb79b3bb962c4118a77e9c5688e9eaa8b1b4f)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.3.3 → v0.3.4](https://github.com/astral-sh/ruff-pre-commit/compare/v0.3.3...v0.3.4)


## 0.20.0 (2024-03-27)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.19.3...0.20.0)

### Fixes

- Refactored context into its own module. [5a3e05d](https://github.com/callowayproject/bump-my-version/commit/5a3e05d82e7560455ec8332230020c9055aab122)
    
### New

- Added `always_increment` attribute for parts. [53ee848](https://github.com/callowayproject/bump-my-version/commit/53ee848988d3dae0665e47aa29d8fa02e604b87f)
    
  This is a requirement for CalVer to ensure they always increment with each bump, but it will work for any type.
- Added CalVer function and formatting. [7a0e639](https://github.com/callowayproject/bump-my-version/commit/7a0e639da8d372e1960dc3dd1cd0620424a228d1)
    
  - Version parts now have a `calver_format` attribute for CalVer parts.
### Updates

- Updated the documentation. [607609d](https://github.com/callowayproject/bump-my-version/commit/607609d1600fb795443998656229ed4a177f9d96)
    

## 0.19.3 (2024-03-23)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.19.2...0.19.3)

### Fixes

- Fixed packaging of dev releases. [84254e0](https://github.com/callowayproject/bump-my-version/commit/84254e0535f553a17a78ca879c7e73c1c2aa0db8)
    
- Fixed platform-dependent encoding. [f8b4d65](https://github.com/callowayproject/bump-my-version/commit/f8b4d65fbc10e9e758114546de3d9c490bbdcb82)
    
  - Added `encoding="utf-8"` to all writes.
- Fixed version.yaml workflow. [10b007c](https://github.com/callowayproject/bump-my-version/commit/10b007c9434a2fed293a6867310f962f3f22a79b)
    
### Other

- [pre-commit.ci] pre-commit autoupdate. [e92000a](https://github.com/callowayproject/bump-my-version/commit/e92000abea994fbf3db7997c00cacb1da6082236)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.3.2 → v0.3.3](https://github.com/astral-sh/ruff-pre-commit/compare/v0.3.2...v0.3.3)

- Bump the github-actions group with 3 updates. [a422c58](https://github.com/callowayproject/bump-my-version/commit/a422c588f40723ac0f441883bbeca29c0f6e406b)
    
  Bumps the github-actions group with 3 updates: [actions/checkout](https://github.com/actions/checkout), [actions/setup-python](https://github.com/actions/setup-python) and [codecov/codecov-action](https://github.com/codecov/codecov-action).


  Updates `actions/checkout` from 3 to 4
  - [Release notes](https://github.com/actions/checkout/releases)
  - [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)
  - [Commits](https://github.com/actions/checkout/compare/v3...v4)

  Updates `actions/setup-python` from 4 to 5
  - [Release notes](https://github.com/actions/setup-python/releases)
  - [Commits](https://github.com/actions/setup-python/compare/v4...v5)

  Updates `codecov/codecov-action` from 3 to 4
  - [Release notes](https://github.com/codecov/codecov-action/releases)
  - [Changelog](https://github.com/codecov/codecov-action/blob/main/CHANGELOG.md)
  - [Commits](https://github.com/codecov/codecov-action/compare/v3...v4)

  ---
  **updated-dependencies:** - dependency-name: actions/checkout
dependency-type: direct:production
update-type: version-update:semver-major
dependency-group: github-actions

  **signed-off-by:** dependabot[bot] <support@github.com>

- Keep GitHub Actions up to date with GitHub's Dependabot. [2e55fa1](https://github.com/callowayproject/bump-my-version/commit/2e55fa1956012fa8e36c3f91afc6e3825d809779)
    
  * https://docs.github.com/en/code-security/dependabot/working-with-dependabot/keeping-your-actions-up-to-date-with-dependabot
  * https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file#package-ecosystem

## 0.19.2 (2024-03-16)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.19.1...0.19.2)

### Fixes

- Fixed bad options not returning an error code. [e88f0a9](https://github.com/callowayproject/bump-my-version/commit/e88f0a96ea82a2be84ad2781c0d82efcc5188963)
    
  Fixes #153
- Fix issue on version.yaml. [7d14065](https://github.com/callowayproject/bump-my-version/commit/7d1406595e8d2fc6be440012497a8c077c2d6592)
    

## 0.19.1 (2024-03-16)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.19.0...0.19.1)

### Fixes

- Fix commas in legacy multiline options. [62dfe8e](https://github.com/callowayproject/bump-my-version/commit/62dfe8e2d6ed5c8d93f92f5d6128ff5aedadc24f)
    
### New

- Added manual version bumping in the GitHub action. [c9d67b5](https://github.com/callowayproject/bump-my-version/commit/c9d67b5dad3a0f93abe35cd4854ee88677f07e8c)
    
### Other

- [pre-commit.ci] pre-commit autoupdate. [be1a568](https://github.com/callowayproject/bump-my-version/commit/be1a568edfa0e714859423b62a00fd08bfadb583)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.2.2 → v0.3.2](https://github.com/astral-sh/ruff-pre-commit/compare/v0.2.2...v0.3.2)


## 0.19.0 (2024-03-12)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.18.3...0.19.0)

### Fixes

- Fixing version hint generation. [ae1732b](https://github.com/callowayproject/bump-my-version/commit/ae1732b4a9b543992f83677263bb242c49c0f5c5)
    
### Updates

- Removes ability to call the CLI without subcommand. [e56c944](https://github.com/callowayproject/bump-my-version/commit/e56c944699151d589cec2b16a52f15cf56d151e6)
    
  BREAKING CHANGE: You must use bump-my-version bump

## 0.18.3 (2024-02-25)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.18.2...0.18.3)

### Fixes

- Fixed --ignore-missing-version and --ignore-missing-files options. [7635873](https://github.com/callowayproject/bump-my-version/commit/7635873d67c71141e181e2bfffe0a353bb1b6288)
    
  The CLI options were defaulting to `False` when missing. This overrode the configuration.

  Fixes #140

## 0.18.2 (2024-02-25)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.18.1...0.18.2)

### Fixes

- Fixed docs and cli help. [8ac1087](https://github.com/callowayproject/bump-my-version/commit/8ac10871135a1c71c9244901b419f3ab95103d1a)
    

## 0.18.1 (2024-02-24)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.18.0...0.18.1)

### Fixes

- Fixed type annotation in config. [2988ede](https://github.com/callowayproject/bump-my-version/commit/2988ede7d1610d42e2249fb8bdbd5a327a85e307)
    
- Fixed naming issue for docs. [2850aa7](https://github.com/callowayproject/bump-my-version/commit/2850aa7f5a804c554d304e45c56a757f55cc5940)
    
  - renamed changelog.md and contributing.md
### New

- Added how-to doc. [68643a9](https://github.com/callowayproject/bump-my-version/commit/68643a9a4945eee20f5b7c4d8fb2f0bc4dd8e7b7)
    
  - "How to update a date in a file"
### Other

- [pre-commit.ci] pre-commit autoupdate. [c495d3d](https://github.com/callowayproject/bump-my-version/commit/c495d3d183a729a2eeb32262a6c164666103873a)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.2.1 → v0.2.2](https://github.com/astral-sh/ruff-pre-commit/compare/v0.2.1...v0.2.2)

### Updates

- Updated docs and styles. [f4f75fa](https://github.com/callowayproject/bump-my-version/commit/f4f75fa50f447366f4fa0209c6ebd709a38bdf90)
    

## 0.18.0 (2024-02-18)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.17.4...0.18.0)

### New

- Added `--ignore-missing-files` option to bump. [fcfaac7](https://github.com/callowayproject/bump-my-version/commit/fcfaac707a79533814008effabd4a05aafc04c57)
    
- Added configuration option `ignore_missing_files`. [b473a19](https://github.com/callowayproject/bump-my-version/commit/b473a195cd16c6dc8bc49d9574feb948fb0408f8)
    
### Other

- Convert docs to MkDocs. [f805c33](https://github.com/callowayproject/bump-my-version/commit/f805c33fb3e5c7064a84761659fc5d43a0de2975)
    
- Converted documentation to use MkDocs. [1b8c6b3](https://github.com/callowayproject/bump-my-version/commit/1b8c6b3b61904998ec8bb055b65235c3d3b2b96f)
    

## 0.17.4 (2024-02-10)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.17.3...0.17.4)

### Fixes

- Fixed linting errors. [9515afc](https://github.com/callowayproject/bump-my-version/commit/9515afcde882e3e5a9cdb51cd91d43ef5d711485)
    
- Fix encoding when reading text. [c03476a](https://github.com/callowayproject/bump-my-version/commit/c03476ac51b94cd136c39bb9c48fee4f1a815b42)
    
  Fixes #68

### Other

- [pre-commit.ci] pre-commit autoupdate. [491b4aa](https://github.com/callowayproject/bump-my-version/commit/491b4aa4edc0241edbf5d77cfcf609c6de56f301)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.1.14 → v0.2.0](https://github.com/astral-sh/ruff-pre-commit/compare/v0.1.14...v0.2.0)


## 0.17.3 (2024-01-29)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.17.2...0.17.3)

### Fixes

- Refactored VersionComponentConfig to VersionComponentSpec. [b538308](https://github.com/callowayproject/bump-my-version/commit/b53830826c81446576b3979080b05930d71c34e2)
    
  More consistent with VersionSpec

### New

- Added mental model documentation. [5cbd250](https://github.com/callowayproject/bump-my-version/commit/5cbd250ab412f0f56af14a0fcc450cb31643e3e4)
    
### Other

- [pre-commit.ci] pre-commit autoupdate. [a2a3fe6](https://github.com/callowayproject/bump-my-version/commit/a2a3fe65fceaae2eb1aa2ab0137e00bb3565709b)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.1.11 → v0.1.14](https://github.com/astral-sh/ruff-pre-commit/compare/v0.1.11...v0.1.14)

### Updates

- Updated more documentation. [779c84c](https://github.com/callowayproject/bump-my-version/commit/779c84c22bde4f96bc44e13ab1834ab3cbb63ee9)
    

## 0.17.2 (2024-01-27)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.17.1...0.17.2)

### Fixes

- Fixed some tests. [593a4ee](https://github.com/callowayproject/bump-my-version/commit/593a4ee376cac57cf6bd26e704f0f6c2a841b99a)
    
- Refactored serialization. [0ac2cd8](https://github.com/callowayproject/bump-my-version/commit/0ac2cd80925c352b72840c1d5707bb61a18248eb)
    
  - Moved serialization from VersionConfig to version.serialization
- Fixed extra capture group in PEP440 parser. [384fd99](https://github.com/callowayproject/bump-my-version/commit/384fd994f67df1fe1a1d56c94e568a00d2c7176b)
    
- Refactored verioning models. [88e7f71](https://github.com/callowayproject/bump-my-version/commit/88e7f71e200ba0a7ef6f121205d634820a68c150)
    
  - created a "conventions" module for future release
  - added an optional `depends_on` version component configuration
  - The `depends_on` is required for PEP440 versioning
- Fixed None as value for a function. [f8c4d05](https://github.com/callowayproject/bump-my-version/commit/f8c4d05d1b4d8df25335b84823a00888a43349f0)
    
  - Turns None into an empty string
- Fixed bad imports. [5c86d51](https://github.com/callowayproject/bump-my-version/commit/5c86d512916b665f164de08b6c488aa6c3d2ee1e)
    
- Refactored versioning models and tests. [7d05414](https://github.com/callowayproject/bump-my-version/commit/7d05414ebd6deedd110f0333733a2db9cc0df6a8)
    
- Refactored version parsing. [5ed546b](https://github.com/callowayproject/bump-my-version/commit/5ed546bd20831136270cfa0264441faa042d4cd9)
    
- Refactored versioning functions and version parts. [be87721](https://github.com/callowayproject/bump-my-version/commit/be87721268a6ba4cc211fb8fb3fa07c85c4eb553)
    
- Fixed timezone of a test. [0e01253](https://github.com/callowayproject/bump-my-version/commit/0e01253b6262b4b583580c3be955984049df1208)
    

## 0.17.1 (2024-01-25)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.17.0...0.17.1)

### Fixes

- Fixed bad error checking with SCM. [10e5d7d](https://github.com/callowayproject/bump-my-version/commit/10e5d7dceea97b1c26868d35978353f7d7595fd5)
    
- Fix missing current version within the context. [a5dca4c](https://github.com/callowayproject/bump-my-version/commit/a5dca4c210260c6dd395ef034db442d58b0342b1)
    

## 0.17.0 (2024-01-22)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.16.2...0.17.0)

### Fixes

- Fixed Py3.8 type annotation. [c15b23b](https://github.com/callowayproject/bump-my-version/commit/c15b23b1f8505dc9d756acf5b7fb73b7d7b5892a)
    
- Fixed some output in visualizing. [406f97a](https://github.com/callowayproject/bump-my-version/commit/406f97a8c77f9c0fce7f436dffe247542c7b75a5)
    
- Fixed bad type annotation. [8f4bedf](https://github.com/callowayproject/bump-my-version/commit/8f4bedf7fb104a2a683acbaa02621589d9a9de27)
    
- Fixed bad test imports. [a74342b](https://github.com/callowayproject/bump-my-version/commit/a74342bfbdc556a7c5161c2c9cee12736c31ee8f)
    
- Refactored the create subcommand. [f529d28](https://github.com/callowayproject/bump-my-version/commit/f529d283fb3a32eddee9daf368f9ce17ba5efcf1)
    
  - Also organized the CLI tests

### New

- Added `show-bump` subcommand. [0bbd814](https://github.com/callowayproject/bump-my-version/commit/0bbd81489ea0484962e9b3c207e6c6860cab6c55)
    
  - Shows possible resulting versions of the `bump` command
- Added sample-config feature. [3d0f67d](https://github.com/callowayproject/bump-my-version/commit/3d0f67dbf9f42ffad1583e1fe08bd0971262257c)
    
  - Initial implementation

### Updates

- Updated documentation. [4f90348](https://github.com/callowayproject/bump-my-version/commit/4f903486338af31557c3647fc0ae00d7cc8e4213)
    

## 0.16.2 (2024-01-13)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.16.1...0.16.2)

### Fixes

- Fixed a bad import. [46c9c48](https://github.com/callowayproject/bump-my-version/commit/46c9c48ccc02a9b2d0e81d70c15323de3e8a4ce8)
    
- Fixed extra whitespace added when updating pyproject.toml. [839f17f](https://github.com/callowayproject/bump-my-version/commit/839f17fbf7a0902fb15347a31778c55e9a91e7ab)
    
  - Removed dotted-notation from requirements. There is an issue on how dotted-notation sets values in the TOMLkit data structure.

  - Added `get_nested_value` and `set_nested_value` as replacements for dotted-notation.

### Other

- [pre-commit.ci] pre-commit autoupdate. [ee4d2f3](https://github.com/callowayproject/bump-my-version/commit/ee4d2f32af28c650651b9242c09e3b125e0101e2)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.1.9 → v0.1.11](https://github.com/astral-sh/ruff-pre-commit/compare/v0.1.9...v0.1.11)


## 0.16.1 (2024-01-06)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.16.0...0.16.1)

### Fixes

- Fixed empty string replacement bug. [d9965ab](https://github.com/callowayproject/bump-my-version/commit/d9965abbcfb11b611ed032daebada0565809dff4)
    
  Only a missing replacement value will trigger one of the fallback options.

  Fixes #117

## 0.16.0 (2024-01-05)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.15.4...0.16.0)

### New

- Add support for legacy multiline search options (refs #98). [278eae5](https://github.com/callowayproject/bump-my-version/commit/278eae578f283223742b7c55870ad58acc8dc1d9)
    
### Other

- [pre-commit.ci] pre-commit autoupdate. [2e9a400](https://github.com/callowayproject/bump-my-version/commit/2e9a4005f9b3f7d7ccbe443188e12d6217039342)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.1.7 → v0.1.9](https://github.com/astral-sh/ruff-pre-commit/compare/v0.1.7...v0.1.9)


## 0.15.4 (2023-12-29)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.15.3...0.15.4)

### Fixes

- Fix not being able to tag without also committing. [753c990](https://github.com/callowayproject/bump-my-version/commit/753c9904505794dd66b0cda0f29206865eeacb3d)
    
- Fixed testing automation. [19215f1](https://github.com/callowayproject/bump-my-version/commit/19215f1fc4eb6c51c26cf28c5aa7a36d7cd901a2)
    
  - The new commit/tag decoupling requires the `--no-tag` flag

## 0.15.3 (2023-12-18)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.15.2...0.15.3)

### Fixes

- Fix miscast of current_version. [b8ea252](https://github.com/callowayproject/bump-my-version/commit/b8ea2525aad07f370e59066bfb21db33e6656639)
    
  - When using the legacy configuration format, a single-digit version is parsed as an int

  Fixes #99

## 0.15.2 (2023-12-18)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.15.1...0.15.2)

### Fixes

- Fixed regression in config update. [2bbbd74](https://github.com/callowayproject/bump-my-version/commit/2bbbd74fe4b80895b3719692d1fe0023cc388bbb)
    
  Fixes #108

### New

- Added a test case for line-start regexes. [ef4823c](https://github.com/callowayproject/bump-my-version/commit/ef4823c0cdb92660439095aacdbac6801953e4ae)
    

## 0.15.1 (2023-12-18)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.15.0...0.15.1)

### Fixes

- Fixes workflow triggers. [690452e](https://github.com/callowayproject/bump-my-version/commit/690452e6164a529a48c1f2043c00fc315b50bb05)
    
- Fixes mismatched artifact up/downloading versions. [3f61742](https://github.com/callowayproject/bump-my-version/commit/3f6174297498b641e19ce6a02e48496e6e5c97c8)
    
- Fixed PR_NUMBER retrieval. [85a8b48](https://github.com/callowayproject/bump-my-version/commit/85a8b4852e55c493f43db8a5e8dd2c2fcaa5fb14)
    
- Fixes committing and download-artifact. [12ba54f](https://github.com/callowayproject/bump-my-version/commit/12ba54f21e5f1c1853fcd38fca5d23c7350b41a2)
    
- Refactored workflows. [d2f30a8](https://github.com/callowayproject/bump-my-version/commit/d2f30a8e649d099668c03a3e292c2e5a41e3c670)
    
### Other

- Testing PR acquisition. [67ab83d](https://github.com/callowayproject/bump-my-version/commit/67ab83d79d67e729bec62a1d25c735ecad41afdb)
    
- Put in temporary debugging steps. [6ac064e](https://github.com/callowayproject/bump-my-version/commit/6ac064eb9b1889981c32782a915cd25b86e4ffe9)
    
### Updates

- Changed the triggers to cause runs. [23e6c18](https://github.com/callowayproject/bump-my-version/commit/23e6c18cd941e7a8717a8ff62ee9e8aa23a5c242)
    
## 0.15.0 (2023-12-16)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.14.0...0.15.0)

### Fixes

- Fixed requirements for github action. [d96e07a](https://github.com/callowayproject/bump-my-version/commit/d96e07a79aef643a363449b86847008152599f64)
    
### Updates

- Changed default regex CLI value to None. [93191f3](https://github.com/callowayproject/bump-my-version/commit/93191f3c20e0f91224f1c2e1df70c3d477cc67ec)
    
  Fixes #64

  The default value of False was overriding other values.

## 0.14.0 (2023-12-15)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.13.0...0.14.0)

### Fixes

- Fixed issue when adding files. [84556f8](https://github.com/callowayproject/bump-my-version/commit/84556f8afefde297c3e34547a23379321fe26be1)
    
- Fixed missing requirement in GH action. [42bab83](https://github.com/callowayproject/bump-my-version/commit/42bab8328a42237c360ff7079b5dc92ecf816a55)
    
- Fixed regression regarding multiple changes in one file. [e7a7629](https://github.com/callowayproject/bump-my-version/commit/e7a7629b19e89e6272e1dbee5b20692656ff197f)
    
  Changed the method of marking changes from a dict keyed by the file name to a list of FileChanges.

  FileChanges encapsulate a single change to a file.
- Refactored logging to provide indented output. [4e68214](https://github.com/callowayproject/bump-my-version/commit/4e682145817cbe2db9d60645fca0d1b17846b7a7)
    
- Refactored FileConfig to FileChange. [249a999](https://github.com/callowayproject/bump-my-version/commit/249a99992088caf5c2c05bfa9a38d10795c0c896)
    
  This better describes what the class does: describe a file change.

  Also moved `get_search_pattern` to the class, since it is specific to each instance
- Refactored config file management. [a4c90b2](https://github.com/callowayproject/bump-my-version/commit/a4c90b2fdcdf57a17242f67c850446b65a27470a)
    
  Moved the INI format stuff into files_legacy.py
- Fixes generate-requirements.sh to upgrade. [121ef69](https://github.com/callowayproject/bump-my-version/commit/121ef69b2d73606a4cce744ee3f9f762ec16b29d)
    
### New

- Added caching to the resolved filemap. [c96e0bd](https://github.com/callowayproject/bump-my-version/commit/c96e0bd125168c70d42c0c353d9ff9f1a2faaf87)
    
- Added custom GitHub action. [4ce17a9](https://github.com/callowayproject/bump-my-version/commit/4ce17a9716e259357d0097ee8e8302b9400c4683)
    
- Added indented logger to improve console output. [d1d19e3](https://github.com/callowayproject/bump-my-version/commit/d1d19e3d06b6ea9f3e0e4967ce5f79b05729adcd)
    
### Updates

- Changed the management of file changes. [909396d](https://github.com/callowayproject/bump-my-version/commit/909396d7541a5876e19dfd948e5468d90ef43640)
    
  File changes are hashable to weed out duplication.
- Removed some commented lines. [89686b8](https://github.com/callowayproject/bump-my-version/commit/89686b89659814878ed782f21b73c308efbbaf0e)
    

## 0.13.0 (2023-12-06)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.12.0...0.13.0)

### Fixes

- Fixed import of extract_regex_flags. [a980670](https://github.com/callowayproject/bump-my-version/commit/a980670c3f9d789fa20ace553aa07c7d14b2f9ca)
    
- Fixed logging and regex regression in 3.11. [cae12dc](https://github.com/callowayproject/bump-my-version/commit/cae12dc4b86339a5c2e4c9ff7658d391cb8eeecc)
    
- Fixed issue with tag name. [e218264](https://github.com/callowayproject/bump-my-version/commit/e2182645b90830478c1efa4c92d8ccd0e3b2d027)
    
  Fixes #74

  current_version and tag_name now do not need to match exactly
- Fixed logic in auto bump workflow. [909a53f](https://github.com/callowayproject/bump-my-version/commit/909a53f628fc4e79b1b3537e51f1cc47f00eb5a3)
    
- Fixes https://github.com/callowayproject/bump-my-version/issues/85. [97049e0](https://github.com/callowayproject/bump-my-version/commit/97049e078fd4b412431b879e86b9f9ce25fbea83)
    
  HG returns the tags in the order they were created so we want the last one in the list
- Fixed autoversioning. [a308a35](https://github.com/callowayproject/bump-my-version/commit/a308a35edb60096e9ccf9a85f62b4986323c9159)
    
### New

- Added key_path to FileConfig. [e160b40](https://github.com/callowayproject/bump-my-version/commit/e160b401b0d14cef77255bbd87748721db4e2e3d)
    
  - Also made all attributes required except `filename`, `glob`, and `key_path`

### Other

- [pre-commit.ci] auto fixes from pre-commit.com hooks. [8188a42](https://github.com/callowayproject/bump-my-version/commit/8188a42d1e25efab1f45499b448f2c007738cbbe)
    
  for more information, see https://pre-commit.ci
- [pre-commit.ci] pre-commit autoupdate. [4c81ad4](https://github.com/callowayproject/bump-my-version/commit/4c81ad4906ac645887f86b4b5a30497ba93ee921)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.1.3 → v0.1.5](https://github.com/astral-sh/ruff-pre-commit/compare/v0.1.3...v0.1.5)

- [pre-commit.ci] pre-commit autoupdate. [7109d70](https://github.com/callowayproject/bump-my-version/commit/7109d706f15c9e2dcf143896672ac2bbe2b0f5c1)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.1.3 → v0.1.6](https://github.com/astral-sh/ruff-pre-commit/compare/v0.1.3...v0.1.6)

### Updates

- Refactored configuration file updating. [e407974](https://github.com/callowayproject/bump-my-version/commit/e40797470e8c331f1ef6d93ed8e99851b423aa82)
    
  TOML files are parsed, specific values are updated, and re-written to avoid updating the wrong data.

  It uses a two-way parser, so all formatting and comments are maintained.

  INI-type configuration files use the old way, since that format is deprecated.

## 0.12.0 (2023-11-04)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.11.0...0.12.0)

### Fixes

- Fixed versioning. [8769671](https://github.com/callowayproject/bump-my-version/commit/87696710968d1c270c88b39738e2fac79720be51)
    
- Fix dev versioning with PR number. [463082b](https://github.com/callowayproject/bump-my-version/commit/463082b1996d3bbd7cd4b6adfe732ede73f5cf54)
    
- Fix dev versioning. [1eed99b](https://github.com/callowayproject/bump-my-version/commit/1eed99bb93b2144cd033f47c13e324a78e8beb0f)
    
  - added an echo of the PR_NUMBER
- Fix versioning of development versions. [e89599f](https://github.com/callowayproject/bump-my-version/commit/e89599f19843537c2e10d4c97da367d377e95914)
    
- Fixes workflows. [5ebb0d7](https://github.com/callowayproject/bump-my-version/commit/5ebb0d77f3302ed7ee5ce2398834573314908927)
    
- Fixed bug #65 where glob'd files weren't used. [357b9dc](https://github.com/callowayproject/bump-my-version/commit/357b9dc85e248845a331ff9a42bc72de5583c8be)
    
### New

- Add -h for help option. [fda71b0](https://github.com/callowayproject/bump-my-version/commit/fda71b0fce4115514fa85cf1d627e5f3673dba66)
    
  Fixes #67

### Other

- Drop Python3.7 as compatible version. [890edc8](https://github.com/callowayproject/bump-my-version/commit/890edc8a0c0911ad3696a9bc0ddca7a9a72c5afd)
    
  Since this is no longer tested, it's safer to start at 3.8.
- [pre-commit.ci] auto fixes from pre-commit.com hooks. [fbcef03](https://github.com/callowayproject/bump-my-version/commit/fbcef038d3b94ca1aef7a6aab52b16fc614a6a9b)
    
  for more information, see https://pre-commit.ci
- Recommend calling 'bump-my-version' instead of 'bumpversion'. [9fb1a1d](https://github.com/callowayproject/bump-my-version/commit/9fb1a1d2f940ec026358d36e6b3f1a81acd7c7d9)
    
- [pre-commit.ci] pre-commit autoupdate. [e2579d6](https://github.com/callowayproject/bump-my-version/commit/e2579d6cd9b62a5f9b2df15ff0df0af4c4d1b2f2)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.0.290 → v0.0.292](https://github.com/astral-sh/ruff-pre-commit/compare/v0.0.290...v0.0.292)

- [pre-commit.ci] pre-commit autoupdate. [e21fdd9](https://github.com/callowayproject/bump-my-version/commit/e21fdd9b11071315a1500af0bfa0a5f29a5e6e0c)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.0.290 → v0.1.1](https://github.com/astral-sh/ruff-pre-commit/compare/v0.0.290...v0.1.1)

- [pre-commit.ci] pre-commit autoupdate. [7e5d1bc](https://github.com/callowayproject/bump-my-version/commit/7e5d1bc95b2fffa907e0a1321bb393aad6221208)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.0.290 → v0.1.3](https://github.com/astral-sh/ruff-pre-commit/compare/v0.0.290...v0.1.3)

### Updates

- Changed the default regex search to non-regex. [0034716](https://github.com/callowayproject/bump-my-version/commit/0034716e4a8a4a45808a9c563a9957db5c63cac4)
    
  Fixes #59

  - Changed the flags to --regex/--no-regex
  - updated tests and docs

## 0.11.0 (2023-09-26)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.10.0...0.11.0)

### Other

- [pre-commit.ci] pre-commit autoupdate. [4a3d046](https://github.com/callowayproject/bump-my-version/commit/4a3d0460fa7d914cb9d5444660f2b09487ad33df)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.0.285 → v0.0.290](https://github.com/astral-sh/ruff-pre-commit/compare/v0.0.285...v0.0.290)

### Updates

- Removed bumpversion as a duplicate of the bump-my-version script. [a59ced8](https://github.com/callowayproject/bump-my-version/commit/a59ced8e5ed126cf2c43070d26d5a001982de962)
    
- Updated dependency from Pydantic 1 to 2. [577aa4c](https://github.com/callowayproject/bump-my-version/commit/577aa4cd6408c7b6a46e8ba7cb5c54cd38cef769)
    

## 0.10.0 (2023-09-05)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.9.3...0.10.0)

### Updates

- Refactored file resolution, inclusion, and exclusion. [646af54](https://github.com/callowayproject/bump-my-version/commit/646af5438740e5dd17425144c6f2e4f305ffc30b)
    
  - Fixes #61
  - Config now includes `resolved_filemap` property
  - resolved filemap expands all globs
  - Config now includes `files_to_modify` property
  - files to modify resolves inclusions and exclutions
  - Improved Config.add_files property

## 0.9.3 (2023-08-25)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.9.2...0.9.3)

### Fixes

- Fixed file configuration overrides. [c1ef3b2](https://github.com/callowayproject/bump-my-version/commit/c1ef3b290746e10e24dcdcb56c52effb6b324464)
    
  Fixes #55

  The file config was ignoring falsey values when constructing the dict.

  It now ignores `None` values.
- Fixed documentation regarding regex config. [cd71a1a](https://github.com/callowayproject/bump-my-version/commit/cd71a1a4216286e49e0d1b8b9d867a26ee88eff8)
    
  - TOML requires the double backslash while INI doesn't
- Fixed requirements for docs. [7856ee0](https://github.com/callowayproject/bump-my-version/commit/7856ee01559289e943a26af7e36382855973e485)
    
### New

- Added documentation building workflow. [48980d7](https://github.com/callowayproject/bump-my-version/commit/48980d7d3445a323c7f8532a8edd61dc09d3fb51)
    
### Other

- [pre-commit.ci] pre-commit autoupdate. [7c38c40](https://github.com/callowayproject/bump-my-version/commit/7c38c401a3755329bce5f127a956e4603c7c4645)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.0.284 → v0.0.285](https://github.com/astral-sh/ruff-pre-commit/compare/v0.0.284...v0.0.285)

- [pre-commit.ci] pre-commit autoupdate. [c30bd12](https://github.com/callowayproject/bump-my-version/commit/c30bd128ca27adea1a93876a29656c5cb7f6d178)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.0.282 → v0.0.284](https://github.com/astral-sh/ruff-pre-commit/compare/v0.0.282...v0.0.284)

- [pre-commit.ci] pre-commit autoupdate. [95c89fb](https://github.com/callowayproject/bump-my-version/commit/95c89fb94ea6cfa5c9d28ed06ee6def9f98ab59f)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.0.281 → v0.0.282](https://github.com/astral-sh/ruff-pre-commit/compare/v0.0.281...v0.0.282)

### Updates

- Removed mentions of Python 3.7. [a91f690](https://github.com/callowayproject/bump-my-version/commit/a91f690ab2c36bef9243058f9e9bbdc1968e9af1)
    

## 0.9.2 (2023-08-07)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.9.1...0.9.2)

### Fixes

- Fixed modified context when committing. [130bbe0](https://github.com/callowayproject/bump-my-version/commit/130bbe0dc9cbc436ed2d4a74878937fc784fbccd)
    
  - Resets the context before committing and tagging
  - Fixes #14

## 0.9.1 (2023-08-03)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.9.0...0.9.1)

### Other

- [pre-commit.ci] auto fixes from pre-commit.com hooks. [4b457d0](https://github.com/callowayproject/bump-my-version/commit/4b457d0d15b881612de7e8970f729f5ea0556c9d)
    
  for more information, see https://pre-commit.ci
- [pre-commit.ci] pre-commit autoupdate. [adb7e4c](https://github.com/callowayproject/bump-my-version/commit/adb7e4c09eea7d568a3bf3597a5b03f352543c3f)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.0.277 → v0.0.281](https://github.com/astral-sh/ruff-pre-commit/compare/v0.0.277...v0.0.281)

### Updates

- Remove `pygments_style` from docsrc/conf.py. [32798a9](https://github.com/callowayproject/bump-my-version/commit/32798a9bcd4d7f1b52fffc84572567c1f60aed9e)
    
  The theme defaults, subjectively, look better.

## 0.9.0 (2023-08-03)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.8.0...0.9.0)

### New

- Added documentation about regular expressions. [449b70a](https://github.com/callowayproject/bump-my-version/commit/449b70aca09c44be2d834b531c85b6a8ff5dde03)
    
- Added configuration and command-line `no_regex` option. [a295a32](https://github.com/callowayproject/bump-my-version/commit/a295a328caedabfe8a1c270a34a6f3ddc41dff7b)
    
  - Global and individual file configurations available for `no_regex`
  - Command-line flag `--no-regex` flag added for `bump` and `replace` sub-commands
- Adds regular expression searching ability. [0210d74](https://github.com/callowayproject/bump-my-version/commit/0210d74a2a66deb58b59b601d61a1b0409c2b6eb)
    
  - Search strings are treated as regular expressions after the initial substitution
- Added deprecation warning on .cfg files. [a0481b7](https://github.com/callowayproject/bump-my-version/commit/a0481b7fb9d9b210fc8162abcb5d5a8ba2710134)
    

## 0.8.0 (2023-07-13)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.7.1...0.8.0)

### New

- Added documentation for ignore missing version. [e0731c3](https://github.com/callowayproject/bump-my-version/commit/e0731c37b8cc1c5ac558462158c86bcb9467a166)
    
- Added `--ignore-missing-version` flag to `bump` and `replace`. [a5bd008](https://github.com/callowayproject/bump-my-version/commit/a5bd008cd60cde13f13505e7d21ba48b4820174a)
    
- Added `ignore-missing-version` configuration. [45c85be](https://github.com/callowayproject/bump-my-version/commit/45c85be6cd1eea10baa37e4529c3fd9ca7afc78d)
    
  - Defaults to `False`
  - File configurations can also override this value
- Added deprecation warnings. [733438b](https://github.com/callowayproject/bump-my-version/commit/733438beb8ad8e320968ef0b2ba2031dc05bd0a5)
    
  - `--list` option will go bye-bye in 1.0
  - calling `bumpversion` without a subcomand will leave in 1.0

## 0.7.1 (2023-07-12)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.7.0...0.7.1)

### Fixes

- Fix search and replace options for replace. [781e8d8](https://github.com/callowayproject/bump-my-version/commit/781e8d8094ba9f16d915a551b3bc51bd6aa54cfa)
    
  - The `--search` and `--replace` options now completely override any other search and replace logic.

  Fixes #34

### Other

- [pre-commit.ci] pre-commit autoupdate. [531738d](https://github.com/callowayproject/bump-my-version/commit/531738d62d3a2583c7831d17151cb8ae7b14677c)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.0.276 → v0.0.277](https://github.com/astral-sh/ruff-pre-commit/compare/v0.0.276...v0.0.277)

- [pre-commit.ci] pre-commit autoupdate. [61e6747](https://github.com/callowayproject/bump-my-version/commit/61e6747529b347530c7ef3e7a6fe13c19cbe61d9)
    
  **updates:** - https://github.com/charliermarsh/ruff-pre-commit → https://github.com/astral-sh/ruff-pre-commit


## 0.7.0 (2023-07-10)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.6.0...0.7.0)

### Fixes

- Fixed test coverage. [3fe96f0](https://github.com/callowayproject/bump-my-version/commit/3fe96f0e244ab5be4f96ec8ecbe1ca63f1f06e6b)
    
- Fixed wrong pydantic version pinning. [d4b125e](https://github.com/callowayproject/bump-my-version/commit/d4b125ea1e1c0179f3f544cfffed90d27c997ff5)
    
- Fixed typing issue. [bfe5306](https://github.com/callowayproject/bump-my-version/commit/bfe530668d8f176843eedcd7096fcd2b85eef228)
    
  - Declared SourceCodeManager attributes as `ClassVar[List[str]]`
  - `_TEST_USABLE_COMMAND`, `_COMMIT_COMMAND`, and `_ALL_TAGS_COMMAND` affected

### New

- Added tests for CLI replace command. [a53cddc](https://github.com/callowayproject/bump-my-version/commit/a53cddc3c13bb21f5432d1cd331a51027a25981f)
    
- Added and re-organized documentation. [c62d65e](https://github.com/callowayproject/bump-my-version/commit/c62d65e71fdc617d5435976cfa587f43b03ac92b)
    
- Added replace subcommand. [8722a0f](https://github.com/callowayproject/bump-my-version/commit/8722a0f84ab60cbfc254741b2a5bc0d968e423d9)
    
  - Works just like `bump` but
    - doesn't do any version incrementing
    - Will not change the configuration file
    - Will not commit or tag

  - Can use `bumpversion show new_version --increment <versionpart>` to see what the new version would be
- Adds `short_branch_name` to version rendering context. [7f7e50c](https://github.com/callowayproject/bump-my-version/commit/7f7e50c98dc20210468a9cef34baf4374956c2e9)
    
  - `short_branch_name` is the branch name, lower case, containing only a-z and 0-9, and truncated to 20 characters.

  Fixes #28

### Other

- Check config before tagging. [3a6e3ee](https://github.com/callowayproject/bump-my-version/commit/3a6e3eebdbc16ae509754fd977625a4c9b19d82a)
    
- Format version parts. [ee43bdb](https://github.com/callowayproject/bump-my-version/commit/ee43bdb18f3d96ed702094bb75b06a1338c9aa9c)
    
- [pre-commit.ci] auto fixes from pre-commit.com hooks. [5e6f566](https://github.com/callowayproject/bump-my-version/commit/5e6f566b3c3bc96a070780a70c82a92b817e2299)
    
  for more information, see https://pre-commit.ci
- [pre-commit.ci] pre-commit autoupdate. [f1acd35](https://github.com/callowayproject/bump-my-version/commit/f1acd353aa4c58afaa15321f7a7ab9dfb12ce040)
    
  **updates:** - [github.com/charliermarsh/ruff-pre-commit: v0.0.272 → v0.0.275](https://github.com/charliermarsh/ruff-pre-commit/compare/v0.0.272...v0.0.275)


## 0.6.0 (2023-06-23)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.5.1.dev69...0.6.0)

### Fixes

- Fixed `--help` and `bump` invocations. [9d965e5](https://github.com/callowayproject/bump-my-version/commit/9d965e57f2c0a41476d75ec053653416eae966c9)
    
  - `--help` works for individual sub-commands, but not for the command
  - `bump` now works and fixed tests
- Fixed issue regarding TOML types. [8960d24](https://github.com/callowayproject/bump-my-version/commit/8960d249183cf78d8b35967b86fef8701fc9c37e)
    
  - `tomlkit.parse()` returns a `TOMLDocument`.
  - `unwrap()` converts it into a `dict`

### New

- Adds `branch_name` to SCM information. [173be1a](https://github.com/callowayproject/bump-my-version/commit/173be1a7a107639be912d0fb76149accb54b0332)
    
- Added documentation for the show command. [d537274](https://github.com/callowayproject/bump-my-version/commit/d5372742a8cf76777f1bf4450bf31e9310d04681)
    
- Adds `--increment` option to `show` subcommand. [b01fffc](https://github.com/callowayproject/bump-my-version/commit/b01fffcad8479db25375d53fdeebc879d7317b11)
    
  - when specified it increments the current version and adds `new_version` to the available output.
- Added `show` subcommand. [9bce887](https://github.com/callowayproject/bump-my-version/commit/9bce887cf5e72907ae00b45a7b7f4812dcc2f17e)
    
  - supersedes the `--list` option
  - provides much more capability
  - Can output in YAML, JSON, and default
  - Can specify one or more items to display
  - Can use dotted-notation to pull items from nested data structures.

### Updates

- Changes bump-my-version into subcommands. [31ffbcf](https://github.com/callowayproject/bump-my-version/commit/31ffbcf839e2491c31d90b51041d1e840371108f)
    
  - Is backwards-compatible with previous versions
  - `bump-my-version` forwards command to `bump-my-version bump` subcommand
  - Only problem is that Click will not show help automatically, must provide `--help`

## 0.5.1 (2023-06-14)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.5.0...0.5.1)

### Fixes

- Fixes reporting the wrong version missing in a file. [efb04e9](https://github.com/callowayproject/bump-my-version/commit/efb04e94a07fa886253bbfc9cf801040e4c03895)
    
  - Fixes issue #20
  - Renders the correct `current_version` for each file being modified.

### Other

- [pre-commit.ci] auto fixes from pre-commit.com hooks. [5476cdf](https://github.com/callowayproject/bump-my-version/commit/5476cdf8b66666e06e9bfd4d71eaf2610103079a)
    
  for more information, see https://pre-commit.ci
- [pre-commit.ci] pre-commit autoupdate. [6e500c2](https://github.com/callowayproject/bump-my-version/commit/6e500c24592f1688cbb13d3fcb6071aa0815ffe8)
    
  **updates:** - [github.com/charliermarsh/ruff-pre-commit: v0.0.270 → v0.0.272](https://github.com/charliermarsh/ruff-pre-commit/compare/v0.0.270...v0.0.272)


## 0.5.0 (2023-06-12)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.4.1...0.5.0)

### Fixes

- Fixed ruff complaints about subprocess. [c429c68](https://github.com/callowayproject/bump-my-version/commit/c429c682515455558095836cb108a93fa23aa67f)
    
- Fixed issue with formatting. [da7544f](https://github.com/callowayproject/bump-my-version/commit/da7544f18780d5f289381d33a87b331c3eaf4d6b)
    
  There is an underlying edge case where the deriving previous environment variables with multiple ways of formatting version numbers will fail.
### New

- Add test to reproduce issue #14. [d78ff46](https://github.com/callowayproject/bump-my-version/commit/d78ff46d65ce75b7651e5697eef59dbcb71c935e)
    
- Added documentation for replacing strings in different files. [893ec03](https://github.com/callowayproject/bump-my-version/commit/893ec03f6ceaf2a050c31f10006aa63c0411af4e)
    
  Fixes #6

### Other

- Made `VERSION_PART` optional. [f236b7d](https://github.com/callowayproject/bump-my-version/commit/f236b7de94d9f58e493c617848e3eb02e85a24c7)
    
  - Fixes #16
  - `VERSION_PART` is detected from the arguments based on the configuration

### Updates

- Updated docs indicated VERSION_PART is optional. [22edeac](https://github.com/callowayproject/bump-my-version/commit/22edeac9018e75f79d7167fbfc6ca56cda4d3b07)
    
- Updated tests for bad version parts. [23be62d](https://github.com/callowayproject/bump-my-version/commit/23be62deed9fb7d51a8bbc195433d1a4ce74c11f)
    
- Changed exception type raised when bad version part is detected. [1e3ebc5](https://github.com/callowayproject/bump-my-version/commit/1e3ebc5b144294771b7bfe812299af4f92ae212a)
    
  - ValueError -> click.BadArgumentUsage
- Updated readme. [7780265](https://github.com/callowayproject/bump-my-version/commit/7780265b97ce49492fef73ca3ac8a1cce27a2fad)
    
  Fixes #7

## 0.4.1 (2023-06-09)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.4.0...0.4.1)

### Fixes

- Fixes release.yaml. [01870d5](https://github.com/callowayproject/bump-my-version/commit/01870d5878b5f0a6e601863c4b9c25572db6cbb0)
    
  Outputs the notes to a file instead of an environment variable.

### Other

- [pre-commit.ci] auto fixes from pre-commit.com hooks. [266002f](https://github.com/callowayproject/bump-my-version/commit/266002f4d60ed6fe3623ba5f713318dc6220ec00)
    
  for more information, see https://pre-commit.ci
- [pre-commit.ci] pre-commit autoupdate. [edc444f](https://github.com/callowayproject/bump-my-version/commit/edc444f0328c27d905b35a5c970320a7171d738f)
    
  **updates:** - [github.com/charliermarsh/ruff-pre-commit: v0.0.261 → v0.0.270](https://github.com/charliermarsh/ruff-pre-commit/compare/v0.0.261...v0.0.270)


## 0.4.0 (2023-04-20)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.3.0...0.4.0)

### Fixes

- Fixed pre-commit hook for dependency checking. [3d5c253](https://github.com/callowayproject/bump-my-version/commit/3d5c2533333112577c43cfe84d2091b1b60564b0)
    
- Fixed installing test dependencies. [c1034eb](https://github.com/callowayproject/bump-my-version/commit/c1034ebb0ae08ef140d8d36b345deb8c5f7b33dd)
    
- Fixed dependency spec. [4782745](https://github.com/callowayproject/bump-my-version/commit/47827452afa41906fb8cb108e4ab61e1b9aa908d)
    
- Fixed missing python in pypi test. [e5ed27d](https://github.com/callowayproject/bump-my-version/commit/e5ed27dee7850a011ac50a063ad055c1bed613d7)
    
- Fixed some CI issues. [d4b03d7](https://github.com/callowayproject/bump-my-version/commit/d4b03d7c0d8dacc4f8c726b208763071202e76c5)
    
- Fixed vague commit and tagging info. [4fb5158](https://github.com/callowayproject/bump-my-version/commit/4fb515851f3ddf78916c624db86c0b3e1869293b)
    
  - If commit is configured false, it will report that it will not commit

  - If commit is configured false, tagging is disabled and it reports that

  - If tagging is configured false, it will report it is not tagging
- Fixes test package. [7c12072](https://github.com/callowayproject/bump-my-version/commit/7c12072b11938385ec81c5e9cd285d91ac1c00d7)
    
  - The build-and-inspect action didn't save the dist packages

### New

- Added tests for logging branches. [f8f0278](https://github.com/callowayproject/bump-my-version/commit/f8f027846349df4c66377c2cf4cc6903cd1f9bf7)
    
- Added path restrictions on release-hints. [e1af658](https://github.com/callowayproject/bump-my-version/commit/e1af65865e16f93441bb07e82800df469232b253)
    
- Added test build to CI. [8738f3f](https://github.com/callowayproject/bump-my-version/commit/8738f3f58b8c940ec44ecc8559192b75b45ccbac)
    
- Added doc files to table of contents. [49858c0](https://github.com/callowayproject/bump-my-version/commit/49858c0fef25f167f221e4c00070492f48f47070)
    
### Other

- Completely migrated setuptools to use pyproject.toml. [f10f8b2](https://github.com/callowayproject/bump-my-version/commit/f10f8b25303c503753b33b434a344600c94409ee)
    
- [pre-commit.ci] pre-commit autoupdate. [d626f7d](https://github.com/callowayproject/bump-my-version/commit/d626f7d6240bfae07ab5a6795df222bdbf48d985)
    
  **updates:** - https://github.com/python/black → https://github.com/psf/black

### Updates

- Removed pre-commit dependency hook. [ac6cdd0](https://github.com/callowayproject/bump-my-version/commit/ac6cdd03e5260d319146ea0d93cc093496e79a19)
    
- Changed the version serialization. [c529452](https://github.com/callowayproject/bump-my-version/commit/c529452b043e8ab1b5711065c1ef96d73030978b)
    
  - can bump "dev" to get a development release
- Updated formatting documentation. [8006f3e](https://github.com/callowayproject/bump-my-version/commit/8006f3efc749a2b8ad21fd365da4d29ebf81cc3b)
    

## 0.3.0 (2023-04-17)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.2.0...0.3.0)

### Fixes

- Fixed bug in SCMInfo setup. [e8fddc9](https://github.com/callowayproject/bump-my-version/commit/e8fddc99ec5f4632f097790ca6b851d8854e09bd)
    
- Fixed missing xml coverage report. [696503f](https://github.com/callowayproject/bump-my-version/commit/696503fff800ea1f3ffb559108cde726296f2d98)
    
- Fixed assertion in failing test. [7afe58c](https://github.com/callowayproject/bump-my-version/commit/7afe58c4a15e0b48f223c3f2c80c48679e44aebc)
    
- Fixes issue when new version equals current version. [64b0de3](https://github.com/callowayproject/bump-my-version/commit/64b0de39828367c6c6f3e7103497256ce3f44f41)
    
  - Now it reports they are the same and exits.
- Fixes issue of duplicate tags. [c025650](https://github.com/callowayproject/bump-my-version/commit/c0256509cb39c3e78c09d35205007191fbf3732e)
    
  - Now it checks if the tag exists and reports a warning
- Fixed automation tooling. [19f13b7](https://github.com/callowayproject/bump-my-version/commit/19f13b7c0c388f15af45cf3fa04424a2946b4a04)
    
  - changed name to bump-my-version in setup.cfg
  - added PAT in release pipeline to (hopefully) allow committing and tagging to master without issue.

### New

- Added codecov to workflow. [a5009e0](https://github.com/callowayproject/bump-my-version/commit/a5009e04068787bb98363c3e6803f84a338ee798)
    
### Other

- Migrated setuptools metadata to pyproject.toml. [0bd54dc](https://github.com/callowayproject/bump-my-version/commit/0bd54dca1230021de266042014164fada25e0837)
    
### Updates

- Updated the readme. [1b1d910](https://github.com/callowayproject/bump-my-version/commit/1b1d910756be07638e6cb113ee05a6f5261f6393)
    
- Updated documentation. [6c3b4fe](https://github.com/callowayproject/bump-my-version/commit/6c3b4fe4995ea67b1cc13ca265d16506bde4dd02)
    

## 0.2.0 (2023-04-14)
[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.1.0...0.2.0)

### Fixes

- Fixed configuration to allow_dirty in bumpversion. [b042e31](https://github.com/callowayproject/bump-my-version/commit/b042e31c47fe03978847552e1efea6a1acb8729e)
    
- Fixes issue with generate-changelog and git. [2a977af](https://github.com/callowayproject/bump-my-version/commit/2a977af4f7a7d860dbe012ae3b29eb20e482d854)
    
- Fixes the quoting in the bumpversion expressions. [9a55d6d](https://github.com/callowayproject/bump-my-version/commit/9a55d6d410bc6da6c451bda45f8228990bb542ab)
    
- Fixed issue with windows testing. [b8abc44](https://github.com/callowayproject/bump-my-version/commit/b8abc44e77d62e85f7315e4866b772f0cf6c5eff)
    
  - different methods for reporting paths was resolved by casting them the pathlib.Paths
- Fixes windows testing error. [556853b](https://github.com/callowayproject/bump-my-version/commit/556853bd017360651b3600cce00cdd6bf00d59f0)
    
  - the differences in path specifications seems to be causing problems.
- Fixed type issue in Python 3.7, 3.8. [ddfd3bf](https://github.com/callowayproject/bump-my-version/commit/ddfd3bf1e72109ef45307e8c76576dfe9f3e575c)
    
- Fixed configuration file detection. [fbf85c2](https://github.com/callowayproject/bump-my-version/commit/fbf85c2134b454043465c0211cc2204e25365ca4)
    
  Doesn't just stop when it finds one, it checks for the existence of the header.
- Fixed logging output and output in general. [0aea9dc](https://github.com/callowayproject/bump-my-version/commit/0aea9dcd84eca1cc9b47acacbada3fc0783a5ee9)
    
### New

- Added additional option to manual runs: verbose. [81eb097](https://github.com/callowayproject/bump-my-version/commit/81eb097e1e30f48f8afb7962c9af5f6a4c80ed96)
    
- Added new workflows. [a9cac5b](https://github.com/callowayproject/bump-my-version/commit/a9cac5b7728fabd46551926b552aba12ed91bd0c)
    
  - Added bumpversion.yaml to increase the version when a PR is closed

  - Added release.yaml to create a github release and upload things to PyPI

- Added PYTHONUTF8 mode. [91a73e2](https://github.com/callowayproject/bump-my-version/commit/91a73e26af94185194aea1ddb803ac621c0ae84a)
    
  - see https://docs.python.org/3/using/windows.html#utf-8-mode

- Added explicit environment variable declarations. [80fe7ef](https://github.com/callowayproject/bump-my-version/commit/80fe7ef0cf1005333143cce38835dbc9ad811884)
    
- Added a github CI workflow. [2b3b358](https://github.com/callowayproject/bump-my-version/commit/2b3b3585afe3fdcf13ff47a229b4e3d3b5dacdc9)
    
- Added files for coverage to ignore. [cfbba08](https://github.com/callowayproject/bump-my-version/commit/cfbba08f23c44dd8e44b545961cbca2599b96e69)
    
  - __main__.py
  - aliases.py

- Added LICENSE. [34a9be5](https://github.com/callowayproject/bump-my-version/commit/34a9be5617a24b9d7eb042dc12e657ef1eb4258c)
    
- Added tests for version parsing errors. [71a204b](https://github.com/callowayproject/bump-my-version/commit/71a204b0eb1ea2e7ae291055f26f5c499d429f1b)
    
- Added utf8 test in files. [9cb8f60](https://github.com/callowayproject/bump-my-version/commit/9cb8f605ba9f8095cb2b8f961f7a7a8000be16dc)
    
- Added more tests for scm. [fe794dd](https://github.com/callowayproject/bump-my-version/commit/fe794dd71aa3b500635379aabc3eae4d47bcb2ea)
    
- Added --list function. [88709fd](https://github.com/callowayproject/bump-my-version/commit/88709fd602c94c2b1bb44a503e91f4ed3ceb0e6c)
    
### Other

- Removing testing for Python 3.7. [19eaeef](https://github.com/callowayproject/bump-my-version/commit/19eaeef7a29112ec96cf171df5f89c69916926f3)
    
- Moved configuration to pyproject.toml. [d339007](https://github.com/callowayproject/bump-my-version/commit/d3390074e8a68db0c2624d1609d166a932d20a2e)
    
- Initial conversion. [f5d1cab](https://github.com/callowayproject/bump-my-version/commit/f5d1cab933f44648ad4a2e6669edffdb907f6779)
    
- Initial commit. [d7dec79](https://github.com/callowayproject/bump-my-version/commit/d7dec79f4cad1952ea6c573e8d5975d1d4944928)
    
### Updates

- Updated workflows. [857835d](https://github.com/callowayproject/bump-my-version/commit/857835d7ce10fe52633fb3cc12f52a55a117cd31)
    
  - Added better changelog parsing
  - Added workflow dispatch inputs for manual runs
- Improved documentation. [f3b7a0f](https://github.com/callowayproject/bump-my-version/commit/f3b7a0f4b1ec72e584677ff59ce4b0b6d59cd083)
    
- Renamed tox job to test. [a9b6db3](https://github.com/callowayproject/bump-my-version/commit/a9b6db35abae273a44e6f196e75603cb83f0c228)
    
- Updated README and other documentation. [e0cebb3](https://github.com/callowayproject/bump-my-version/commit/e0cebb3ecaac58a8b7a8773847079fe1a7cd3035)
    
- Improved Mercurial support. [560999d](https://github.com/callowayproject/bump-my-version/commit/560999dba12366837e329a2d68931d1d4f81a4d3)
    
- Improved logging output. [6ccfa7d](https://github.com/callowayproject/bump-my-version/commit/6ccfa7d9c65a84347368e4409b37fcf7d84bab56)
    
- Changed errors to subclass UsageError. [a447651](https://github.com/callowayproject/bump-my-version/commit/a4476516bd799cc047cab4cd6b42939e851a4907)
    
- Changed BaseVCS to SourceCodeManager. [11c5609](https://github.com/callowayproject/bump-my-version/commit/11c560982700fe4a649bd65f74dbeee2a28d8fc5)
    
  Just for consistency.
- Modified the group command back to a single command. [6d4179b](https://github.com/callowayproject/bump-my-version/commit/6d4179b9bbba6fd81453de274468716528832b15)
    
  Will eventually change to a group command, but later.

## 0.1.0 (2023-03-24)

* Initial creation
