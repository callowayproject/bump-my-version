---
title: Hooks
description: Details about writing and setting up hooks
icon: 
date: 2024-08-15
comments: true
---
# Hooks

- Each global configuration of `setup_hooks`, `pre_commit_hooks`, and `post_commit_hooks` is a list of commands run in a shell
- Explanation of the context passed into the environment
- Run in sequentially

Order of operations

- Run setup hooks
- Increment version
- Change files
- Run pre-commit hooks
- commit and tag
- Run post-commit hooks

## Setup Hooks

```toml title="Calling individual commands"
[tool.bumpversion]
setup_hooks = [
    "git config --global user.email \"bump-my-version@github.actions\"",
    "git config --global user.name \"Testing Git\"",
    "git --version",
    "git config --list",
]
```

or

```toml title="Calling a shell script"
[tool.bumpversion]
setup_hooks = ["path/to/setup.sh"]
```

```bash title="path/to/setup.sh"
#!/usr/bin/env bash

git config --global user.email "bump-my-version@github.actions"
git config --global user.name "Testing Git"
git --version
git config --list
```
### Environment

- The existing OS environment is available

#### Date and time fields

::: field-list

    `BVHOOK_NOW`
    : The ISO-8601-formatted current local time without a time zone reference.
    
    `BVHOOK_UTCNOW`
    : The ISO-8601-formatted current local time in the UTC time zone.

#### Source code management fields

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


#### Version fields

::: field-list
    `BVHOOK_CURRENT_VERSION`
    : The current version serialized as a string

    `BVHOOK_CURRENT_TAG`
    : The current tag
    
    `BVHOOK_CURRENT_<version component>`
    : Each version component defined by the [version configuration parsing regular expression](configuration/global.md#parse). The default configuration would have `current_major`, `current_minor`, and `current_patch` available.
