# Temporary Files and Directories

## `tmp_path` — per-test temporary directory

`tmp_path` provides a temporary directory unique to each test invocation.
It is a [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path) object and is cleaned up automatically after the test.

```python
# test_file_operations.py
import pytest
from pathlib import Path


def save_data(filepath: Path, data: str):
    """Save data to file."""
    filepath.write_text(data)


def load_data(filepath: Path) -> str:
    """Load data from file."""
    return filepath.read_text()


def test_file_operations(tmp_path: Path):
    """Test file operations with temporary directory."""
    test_file = tmp_path / "test_data.txt"

    # Save data
    save_data(test_file, "Hello, World!")

    # Verify file exists and content is correct
    assert test_file.exists()
    assert load_data(test_file) == "Hello, World!"
```

## `tmp_path_factory` — shared temporary directory

When multiple tests or a fixture need a single shared temporary directory (e.g. to avoid repeatedly generating a large file), use `tmp_path_factory` with a broader fixture scope:

```python
# tests/conftest.py
import pytest
from pathlib import Path


@pytest.fixture(scope="module")
def shared_data_dir(tmp_path_factory) -> Path:
    """Create a temporary directory shared across all tests in the module."""
    data_dir = tmp_path_factory.mktemp("data")
    (data_dir / "sample.csv").write_text("id,name\n1,Alice\n2,Bob\n")
    return data_dir
```

```python
# tests/test_csv_reader.py
from pathlib import Path


class TestCsvReader:
    def test_reads_correct_row_count(self, shared_data_dir: Path):
        csv_file = shared_data_dir / "sample.csv"
        rows = csv_file.read_text().strip().splitlines()
        assert len(rows) == 3  # header + 2 data rows

    def test_first_data_row_contains_alice(self, shared_data_dir: Path):
        csv_file = shared_data_dir / "sample.csv"
        content = csv_file.read_text()
        assert "Alice" in content
```

`tmp_path_factory.mktemp("data")` creates a uniquely named subdirectory inside the base temp directory. The directory persists for the lifetime of the fixture scope (here, `module`).
