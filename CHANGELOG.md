# Changelog

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
    
  There is an underlying edge case where the deriving previous environment variables with multple ways of formatting version numbers will fail.
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

  - Added release.yaml to create a github relase and upload things to PyPI
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
