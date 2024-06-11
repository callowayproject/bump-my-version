# Changelog

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
