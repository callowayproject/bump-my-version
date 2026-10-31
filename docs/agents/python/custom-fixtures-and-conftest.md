# Custom Fixtures and Conftest

The `conftest.py` file is a special file used by pytest to share [fixtures](https://docs.pytest.org/en/stable/explanation/fixtures.html) across multiple test files in a directory and its subdirectories.
Pytest automatically discovers and uses `conftest.py` files without needing to import them explicitly in test files.

Key Use Cases for `conftest.py`

- **Sharing Fixtures:** The primary use case is allowing multiple test files to access the same setup/teardown logic
  without explicit imports.
- **Modifying `sys.path`:** Pytest automatically adds the directory containing the `conftest.py` file to `sys.path`,
  helping Python find application modules for testing without needing to set `PYTHONPATH` explicitly.

## Example: Sharing a fixture across test files

Define the fixture once in `conftest.py`:

```python
# tests/conftest.py
import pytest
from typing import Generator
from myapp.database import Database


@pytest.fixture
def db() -> Generator[Database, None, None]:
    """Provide a connected in-memory database for any test that needs it."""
    database = Database("sqlite:///:memory:")
    database.connect()
    yield database
    database.disconnect()
```

Any test file in the same directory (or subdirectory) can request it by name — no import needed:

```python
# tests/test_users.py
from myapp.database import Database


class TestUserQueries:
    def test_returns_empty_list_when_no_users(self, db: Database):
        result = db.query("SELECT * FROM users")
        assert result == []
```

```python
# tests/test_products.py
from myapp.database import Database


class TestProductQueries:
    def test_returns_empty_list_when_no_products(self, db: Database):
        result = db.query("SELECT * FROM products")
        assert result == []
```

Both tests receive a fresh, connected database instance without any imports or duplication of setup code.
