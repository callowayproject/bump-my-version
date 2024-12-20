# How to update a date in a file

Many times when bumping a version, you will also want to update a date in a file. This is a common use case for changelogs, but it could be any file that contains a date. In this example, we have an `__init__.py` that looks like this:

```python title="my_package/__init__.py"
__date__ = '2022-12-19'
__version__ = '0.4.0'
```

The desired outcome is to update the date to the current date. For example, if today is February 23, 2024, the `__init__.py` file should look like this after a `minor` bump:

```python title="my_package/__init__.py"
__date__ = '2024-02-23'
__version__ = '0.5.0'
```

## Setting up the file configurations

We need Bump My Version to update the `__init__.py` file twice: once for the version and once for the date. Here is the necessary configuration:

```toml title=".bumpversion.toml or other config file"
[[tool.bumpversion.files]]
filename = '__init__.py'
search = "__date__ = '\\d{{4}}-\\d{{2}}-\\d{{2}}'"
replace = "__date__ = '{now:%Y-%m-%d}'"
regex = true

[[tool.bumpversion.files]]
filename = '__init__.py'
```
