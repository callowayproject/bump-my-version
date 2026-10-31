# Mocking with unittest.mock and pytest-mock

The [pytest-mock plugin](https://pytest-mock.readthedocs.io/en/latest/) provides a `mocker` fixture,
a thin wrapper around the patching API of the [mock package](http://pypi.python.org/pypi/mock).
Use the `mocker` fixture when a test requires mocking external resources.

The `mocker` fixture has the same API as [mock.patch](https://docs.python.org/3/library/unittest.mock.html#patch), supporting the same arguments.

The supported methods are:

- [mocker.patch](https://docs.python.org/3/library/unittest.mock.html#patch)
- [mocker.patch.object](https://docs.python.org/3/library/unittest.mock.html#patch-object)
- [mocker.patch.multiple](https://docs.python.org/3/library/unittest.mock.html#patch-multiple)
- [mocker.patch.dict](https://docs.python.org/3/library/unittest.mock.html#patch-dict)
- [mocker.stopall](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch.stopall)
- [mocker.stop](https://docs.python.org/3/library/unittest.mock.html#patch-methods-start-and-stop)
- `mocker.resetall()`: calls [reset_mock()](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.reset_mock) in all mocked objects up to this point.

Also, as a convenience, these names from the `mock` module are accessible directly from `mocker`:

- [Mock](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock)
- [MagicMock](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.MagicMock)
- [PropertyMock](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.PropertyMock)
- [AsyncMock](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.AsyncMock)
- [ANY](https://docs.python.org/3/library/unittest.mock.html#any)
- [DEFAULT](https://docs.python.org/3/library/unittest.mock.html#default)
- [call](https://docs.python.org/3/library/unittest.mock.html#call)
- [sentinel](https://docs.python.org/3/library/unittest.mock.html#sentinel)
- [mock_open](https://docs.python.org/3/library/unittest.mock.html#mock-open)
- [seal](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.seal)

Here is a simple API client in `api_client.py`

```python
# api_client.py
import requests


class APIClient:
    def get_data(self, url: str):
        response = requests.get(url)
        return response.json()
```

Here is a set of tests that mock the external request call:

```python
# tests/test_api_client.py
from api_client import APIClient


class TestGetData:
    "Tests for the APIClient.get_data method."

    def test_returns_json_object(self, mocker):
        """The result of a successful get_data call is a JSON object."""
        # Arrange
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"key": "value"}

        # Patch 'requests.get' to return the mock response
        mock_get = mocker.patch("requests.get", return_value=mock_response)

        # Act
        client = APIClient()
        result = client.get_data("http://example.com/api")

        # Assert
        assert result == {"key": "value"}
        mock_get.assert_called_once_with("http://example.com/api")
```
