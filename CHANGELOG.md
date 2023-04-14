# Changelog

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
