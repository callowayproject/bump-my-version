---
title: Hooks
description: Details about writing and setting up hooks
icon: 
date: 2024-08-15
comments: true
---
# Hooks

## Hook Suites

A _hook suite_ is a list of _hooks_ to run sequentially. A _hook_ is either an individual shell command or an executable script.

There are three hook suites: _setup, pre-commit,_ and _post-commit._ During the version increment process this is the order of operations:

1. Run _setup_ hooks
2. Increment version
3. Change files
4. Run _pre-commit_ hooks
5. Commit and tag
6. Run _post-commit_ hooks

!!! Note

    Don't confuse the _pre-commit_ and _post-commit_ hook suites with Git pre- and post-commit hooks. Those hook suites are named for their adjacency to the commit and tag operation.


## Configuration

Configure each hook suite with the `setup_hooks`, `pre_commit_hooks`, or `post_commit_hooks` keys.

Each suite takes a list of strings. The strings may be individual commands:

```toml title="Calling individual commands"
[tool.bumpversion]
setup_hooks = [
    "git config --global user.email \"bump-my-version@github.actions\"",
    "git config --global user.name \"Testing Git\"",
    "git --version",
    "git config --list",
]
pre_commit_hooks = ["cat CHANGELOG.md"]
post_commit_hooks = ["echo Done"]
```

or the path to an executable script:

```toml title="Calling a shell script"
[tool.bumpversion]
setup_hooks = ["path/to/setup.sh"]
pre_commit_hooks = ["path/to/pre-commit.sh"]
post_commit_hooks = ["path/to/post-commit.sh"]
```

!!! Note

    You can make a script executable using the following steps:

    1. Add a [shebang](https://en.wikipedia.org/wiki/Shebang_(Unix)) line to the top like `#!/bin/bash`
    2. Run `chmod u+x path/to/script.sh` to set the executable bit

## Hook Environments

Each hook has these environment variables set when executed.

### Inherited environment

All environment variables set before bump-my-version was run are available.

### Date and time fields

::: field-list

    `BVHOOK_NOW`
    : The ISO-8601-formatted current local time without a time zone reference.
    
    `BVHOOK_UTCNOW`
    : The ISO-8601-formatted current local time in the UTC time zone.

### Source code management fields

!!! Note

    These fields will only have values if the code is in a Git or Mercurial repository.

::: field-list

    `BVHOOK_COMMIT_SHA`
    : The latest commit reference.
    
    `BHOOK_DISTANCE_TO_LATEST_TAG`
    : The number of commits since the latest tag.
    
    `BVHOOK_IS_DIRTY`
    : A boolean indicating if the current repository has pending changes.
    
    `BVHOOK_BRANCH_NAME`
    : The current branch name.
    
    `BVHOOK_SHORT_BRANCH_NAME`
    : The current branch name, converted to lowercase, with non-alphanumeric characters removed and truncated to 20 characters. For example, `feature/MY-long_branch-name` would become `featuremylongbranchn`.


### Current version fields

::: field-list
    `BVHOOK_CURRENT_VERSION`
    : The current version serialized as a string

    `BVHOOK_CURRENT_TAG`
    : The current tag
    
    `BVHOOK_CURRENT_<version component>`
    : Each version component defined by the [version configuration parsing regular expression](configuration/global.md#parse). The default configuration would have `BVHOOK_CURRENT_MAJOR`, `BVHOOK_CURRENT_MINOR`, and `BVHOOK_CURRENT_PATCH` available.


### New version fields

!!! Note

    These are not available in the _setup_ hook suite.

::: field-list
    `BVHOOK_NEW_VERSION`
    : The new version serialized as a string

    `BVHOOK_NEW_TAG`
    : The new tag
    
    `BVHOOK_NEW_<version component>`
    : Each version component defined by the [version configuration parsing regular expression](configuration/global.md#parse). The default configuration would have `BVHOOK_NEW_MAJOR`, `BVHOOK_NEW_MINOR`, and `BVHOOK_NEW_PATCH` available.

## Outputs

The `stdout` and `stderr` streams are echoed to the console if you pass the `-vv` option.

## Dry-runs

Bump my version does not execute any hooks during a dry run. With the verbose output option it will state which hooks it would have run.
