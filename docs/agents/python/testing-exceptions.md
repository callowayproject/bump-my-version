# Testing Exceptions

You test for expected exceptions using the `pytest.raises()` context manager.
This ensures that a specific code block or function call raises the expected exception.
If the expected exception is not raised, the test fails.

For convenience, `pytest.raises()` accepts a `match` keyword argument
to test the exception message using a regular expression.

To test multiple failure cases efficiently, you can use `@pytest.mark.parametrize`.
A common pattern is to use `contextlib.nullcontext` when _no_ exception is expected.

To test the code:

```python
# divide.py

def divide(a: float, b: float) -> float:
    """Divide a by b."""
    if b == 0:
        raise ZeroDivisionError("Division by zero")
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Arguments must be numbers")
    return a / b
```

Here is an example

```python
# test_exceptions.py

import pytest
from pytest import param
from divide import divide
from contextlib import nullcontext as does_not_raise


@pytest.mark.parametrize(  
    "num1, num2, expectation, expected_result",  
    [  
        param(30, 2.5, does_not_raise(), 12.0, id="divides by non-zero value"),  
        param(  
            10,  
            0,  
            pytest.raises(ZeroDivisionError, match="Division by zero"),  
            None,  
            id="raises exception when denominator is zero",  
        ),  
        param(  
            "a",  
            2,  
            pytest.raises(TypeError, match="must be numbers"),  
            None,  
            id="raises exception when non-numeric argument",  
        ),  
    ],  
)  
def test_divide_cases(num1, num2, expectation, expected_result):  
    """Test divide function with various cases."""  
    with expectation:  
        result = divide(num1, num2)  
        assert result == expected_result
```
