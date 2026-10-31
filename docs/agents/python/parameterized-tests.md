# Parameterized Tests

The built-in [pytest.mark.parametrize](https://docs.pytest.org/en/stable/reference/reference.html#pytest-mark-parametrize-ref) decorator enables the parametrization of arguments for a test function.

Each parameter should be within a `param` call, include the arguments,
and include an `id` keyword argument with a descriptive name for what is being tested.

Here is a typical example of a test function that implements checking that a certain input leads to an expected output:

```python
# test_validation.py
import pytest
from pytest import param


@pytest.mark.parametrize("email,expected", [
    param("user@example.com", True, id="contains user and domain"),
    param("test.user@domain.co.uk", True, id="accepts dots in user"),
    param("invalid.email", False, id="missing user and @ fails"),
    param("@example.com", False, id="missing user fails"),
    param("user@domain", False, id="missing top-level domain fails"),
    param("", False, id="empty address fails"),
])
def test_is_valid_email(email: str, expected: bool):
    """Test email validation with various inputs."""
    assert is_valid_email(email) == expected
```
