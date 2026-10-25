# Testing Async Code

[pytest-asyncio](https://pytest-asyncio.readthedocs.io/en/stable/index.html) is a pytest plugin.
It facilitates testing of code that uses the [asyncio](https://docs.python.org/3/library/asyncio.html) library.
Specifically, pytest-asyncio supports coroutines as test functions.
This allows users to `await` code in their tests.

## Configuration

Set `asyncio_mode = "auto"` in `pyproject.toml` to avoid decorating every async test with `@pytest.mark.asyncio`:

```toml
# pyproject.toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
```

Without this, each async test function requires `@pytest.mark.asyncio` explicitly.

## Basic async test

```python
# test_async.py
import pytest

@pytest.mark.asyncio
async def test_some_asyncio_code():
    res = await library.do_something()
    assert res == b"expected result"
```

## Async fixtures

Use `@pytest_asyncio.fixture` (not `@pytest.fixture`) for async setup/teardown:

```python
# tests/test_async_client.py
import pytest
import pytest_asyncio
from typing import AsyncGenerator
from my_client import AsyncClient

@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    c = AsyncClient()
    await c.connect()
    yield c
    await c.disconnect()

async def test_fetch_returns_data(client: AsyncClient):
    result = await client.fetch("/data")
    assert result == {"status": "ok"}
```

> If `asyncio_mode = "auto"`, the `@pytest.mark.asyncio` decorator on tests is optional.

## Mocking coroutines with AsyncMock

Use `AsyncMock` when the code under test `await`s a dependency:

```python
# tests/test_service.py
import pytest
from unittest.mock import AsyncMock
from my_service import DataService

async def test_process_calls_fetch_and_returns_result(mocker):
    # Arrange
    mock_fetch = mocker.patch(
        "my_service.DataService.fetch",
        new_callable=AsyncMock,
        return_value={"id": 1},
    )

    # Act
    service = DataService()
    result = await service.process(1)

    # Assert
    assert result == {"id": 1}
    mock_fetch.assert_awaited_once_with(1)
```
