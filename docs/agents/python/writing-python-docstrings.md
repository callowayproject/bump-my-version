---
name: writing-python-docstrings
description: USE WHEN writing python docstrings or asked to document Python code.
---

# Python Docstring Guide

## TL;DR Rules

- Use triple double quotes: `"""`.
- Docstring is the first statement in module/class/function.
- Summary line: one sentence, present tense, ends with `.`, `?`, or `!`.
- If more content exists: blank line, then body aligned with opening quotes.
- Use Google-style sections with 4-space hanging indent.
- Do not repeat the function/class name or include types in `Args`.
- `Args` order matches signature; omit `self` and `cls`.
- Use `Deprecated:` section when applicable.
- Use Markdown for inline styling and object links: `[name][full.path.to.name]`.

## Section Order (Google Style)

Common order (include only what applies):

1. Summary Line
2. Extended Summary (optional)
3. Deprecated (if applicable)
4. Args (if applicable)
5. Returns or Yields (if applicable)
6. Raises (if applicable)
7. Examples (optional)

## By Object Type

- Module: Summary, Extended Summary, Deprecated (if needed).
- Class: Summary, Extended Summary, Deprecated, Examples; put init params in `Args`.
- Function/Method/Property/Generator: use full section order as needed.
- Constant/Attribute: Summary; optional Extended Summary/Deprecated/Examples.

## Summary Line

Do not use variable names or the object name.

Yes:

```python
class CheeseShopAddress:
    """The address of a cheese shop."""
```

No:

```python
class CheeseShopAddress:
    """Class that describes the address of a cheese shop."""
```

## Extended Summary

Short prose that clarifies behavior. Keep parameter details in `Args`.

## Deprecated

Include: removal version, reason (if useful), replacement.

```python
def count_by_twos(start: int, end: int) -> list:
    """
    Provide a list of every other number between two numbers.

    Deprecated:
        Removed in 2.0. Use [`count_by`][full.path.to.count_by].
    """
```

## Args

- List in signature order.
- Omit `self`/`cls`.
- No types; rely on type hints.
- Optional args start with `Optional;` and may include default.

```text
Args:
    table_handle: An open `smalltable.Table` instance.
    keys: A sequence of strings representing the key of each table row.
    require_all_keys: Optional; If `True`, only rows with values set for all keys
        will be returned. (Default: `False`)
```

## Returns

Describe the returned value(s), especially if complex.

```text
Returns:
    A dict mapping keys to row tuples.
```

## Yields

Use like `Returns`, but for generators.

## Raises

List exceptions and conditions.

```text
Raises:
    IOError: Error accessing the smalltable.
```

## Examples

Use doctest or fenced code blocks. Separate multiple examples with blank lines.

```python
"""
Examples:
    >>> print("hello!")
    hello!

    >>> a = 0
    >>> a += 1
    >>> a
    1
"""
```

## Placement

- Module docstring comes after any file header and before imports.
- Class docstring is indented to class scope.
- Attribute/constant docstring goes immediately below the definition.

```python
NAME: str = "Simple Simon"
"""Name of the project."""
```

## Notes

These guidelines follow Google style, not PEP-287.
Derived from the LSST DM Developer Guide.
