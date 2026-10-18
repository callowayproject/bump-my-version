---
name: python-tester
description: Implement comprehensive Python testing strategies with pytest. USE WHEN writing Python unit/integration/functional/perf tests or TDD workflow (Red-Green-Refactor cycle, naming conventions, quality principles) refer to @tdd-best-practices.md
---

# Python Testing Patterns

Implement comprehensive Python testing strategies with pytest.

## Use When

Writing Python unit/integration/functional/perf tests.

## Core Rules

- AAA: Arrange / Act / Assert
- Isolated, deterministic tests
- Descriptive names (why, not just what)
- Fixtures for setup/teardown
- Parametrize to reduce duplication
- Mock externals
- Test edges/errors
- Coverage: meaningful > %

For TDD workflow (Red-Green-Refactor cycle, naming conventions, quality principles) refer to @tdd-best-practices.md

## Patterns

### 1) Class method

```python
# calculator.py
class Calculator:
    def add(self, a: float, b: float) -> float:
        return a + b
```

```python
# tests/test_calculator.py
from calculator import Calculator


class TestAdd:
    def test_commutative(self):
        c = Calculator()
        assert c.add(2, 3) == c.add(3, 2)

    def test_identity(self):
        c = Calculator()
        assert c.add(8, 0) == c.add(0, 8) == 8

    def test_inverse(self):
        c = Calculator()
        assert c.add(8, -8) == c.add(-8, 8) == 0
```

### 2) Function

```python
# calculator.py
def add(a: float, b: float) -> float:
    return a + b
```

```python
# tests/test_calculator.py
from calculator import add


class TestAdd:
    def test_commutative(self):
        assert add(2, 3) == add(3, 2)
```

### 3) Fixtures (setup/teardown via yield)

```python
# database.py
class Database:
    def __init__(self, cs: str):
        self.cs = cs
        self.connected = False

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False

    def query(self, sql: str):
        if not self.connected:
            raise RuntimeError("Not connected")
        return [{"id": 1, "name": "Test"}]
```

```python
# tests/test_database.py
import pytest
from typing import Generator
from database import Database


@pytest.fixture
def db() -> Generator[Database, None, None]:
    database = Database("sqlite:///:memory:")
    database.connect()
    yield database
    database.disconnect()


class TestQuery:
    def test_returns_one_record(self, db: Database):
        # Arrange
        expected = [{"id": 1, "name": "Test"}]
        # Act
        results = db.query("SELECT * FROM users")
        # Assert
        assert results == expected
```

### 4) Parametrize

```python
import pytest
from pytest import param


@pytest.mark.parametrize(
    "email,expected",
    [
        param("user@example.com", True, id="valid"),
        param("invalid.email", False, id="missing @"),
    ],
)
def test_is_valid_email(email, expected):
    assert is_valid_email(email) == expected
```

### 5) Mocking (pytest-mock)

```python
# api_client.py
import requests


class APIClient:
    def get_data(self, url: str):
        return requests.get(url).json()
```

```python
# tests/test_api_client.py
from api_client import APIClient


def test_returns_json(mocker):
    mock_resp = mocker.Mock()
    mock_resp.json.return_value = {"key": "value"}
    mocker.patch("requests.get", return_value=mock_resp)

    assert APIClient().get_data("http://x") == {"key": "value"}
```

### 6) Exceptions

```python
import pytest
from pytest import param
from contextlib import nullcontext as does_not_raise


@pytest.mark.parametrize(
    "a,b,expect,ans",
    [
        param(30, 2.5, does_not_raise(), 12.0, id="ok"),
        param(10, 0, pytest.raises(ZeroDivisionError, match="zero"), None, id="zero"),
    ],
)
def test_divide(a, b, expect, ans):
    with expect:
        assert divide(a, b) == ans
```

For more information refer to @testing-exceptions.md

### 7) Async

```python
import pytest


@pytest.mark.asyncio
async def test_do_something_returns_expected_result():
    res = await library.do_something()
    assert res == b"expected result"
```

For more information refer to @testing-async-code.md

### 8) tmp_path

```python
def test_write_text_is_successful(tmp_path):
    p = tmp_path / "test.txt"
    p.write_text("Hello")
    assert p.read_text() == "Hello"
```

For more details refer to @temporary-files-and-dirs.md

### 9) conftest.py

Use `conftest.py` to share fixtures; pytest auto-discovers it.

For more details refer to @custom-fixtures-and-conftest.md

### 10) Fixture scopes

Control how often a fixture is created/destroyed with the `scope` parameter:

```python
@pytest.fixture(scope="function")  # default: new instance per test
def func_scoped(): ...


@pytest.fixture(scope="class")  # one instance per test class
def class_scoped(): ...


@pytest.fixture(scope="module")  # one instance per test file
def module_scoped(): ...


@pytest.fixture(scope="session")  # one instance for the entire test run
def session_scoped(): ...
```

Use broader scopes for expensive setup (e.g. DB connections, server processes).

### 11) monkeypatch

Use the built-in `monkeypatch` fixture to temporarily set env vars, replace attributes, or modify dicts:

```python
def test_uses_custom_env_var(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-key-123")
    assert get_api_key() == "test-key-123"


def test_patches_attribute(monkeypatch):
    monkeypatch.setattr("mymodule.DEFAULT_TIMEOUT", 0)
    assert fetch_with_timeout() == "ok"
```

All changes are automatically undone after the test.

## Organization

```text
tests/
  conftest.py
  test_module1/
    test_models.py
  test_utils.py
```

## Naming

- Class: `Test<Thing>`
- Test names explain behavior/intent
- Examples:
    - `test_is_not_adult_if_age_less_than_18`
    - `test_fails_if_account_invalid`

## Coverage

```sh
uv run pytest --cov-report=term-missing tests/
```

For coverage thresholds, critical path rules, and avoiding coverage theater refer to @tdd-best-practices.md
