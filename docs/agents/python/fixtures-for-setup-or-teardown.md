# Fixtures for Setup and Teardown

Fixtures that require setup and teardown use `yield` instead of `return`. With these fixtures, we can run code and return an object to the requesting fixture/test, just as with the other fixtures. The only differences are:

1. `return` is swapped out for `yield`.
2. Any teardown code for that fixture is placed _after_ the `yield`.

Once `pytest` determines a linear order for the fixtures, it runs each one until it returns or yields, then moves on to the next fixture in the list and repeats the process.

Once the test is finished, `pytest` will go back down the list of fixtures in reverse order, taking each one that yielded and running the code inside it that came _after_ the `yield` statement.

For example, the code file `database.py`:

```python
# database.py


class Database:
    """Simple database class."""

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connected = False

    def connect(self):
        """Connect to database."""
        self.connected = True

    def disconnect(self):
        """Disconnect from database."""
        self.connected = False

    def query(self, sql: str) -> list:
        """Execute query."""
        if not self.connected:
            raise RuntimeError("Not connected")
        return [{"id": 1, "name": "Test"}]
```

Testing the `query` method requires a connected database, `tests/test_database.py`:

```python
# test_database.py
import pytest
from typing import Generator
from database import Database


@pytest.fixture
def db() -> Generator[Database, None, None]:
    """Fixture that provides a connected database."""
    # Setup
    database = Database("sqlite:///:memory:")
    database.connect()

    # Provide to test
    yield database

    # Teardown
    database.disconnect()


class TestQuery:
    """Tests for the `Database.query` method."""

    def test_returns_one_record(self, db: Database):
        """The query method should return a single record."""
        # Arrange
        expected = [{"id": 1, "name": "Test"}]

        # Act
        results = db.query("SELECT * FROM users")

        # Assert
        assert results == expected
```
