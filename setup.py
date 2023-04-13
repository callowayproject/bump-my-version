"""The setup script."""
from pathlib import Path
from typing import List, Optional

from setuptools import setup


def parse_reqs_in(filepath: Path, visited: Optional[set] = None) -> List[str]:  # noqa: C901
    """
    Parse a file path containing a pip-tools requirements.in and return a list of requirements.

    Will properly follow ``-r`` and ``-c`` links like ``pip-tools``. This
    means layered requirements will be returned as one list.

    Other ``pip-tools`` and ``pip``-specific lines are excluded.

    Args:
        filepath (Path): The path to the requirements file
        visited (set, optional): A set of paths that have already been visited.

    Returns:
        All the requirements as a list.
    """
    if visited is None:
        visited = set()
    reqstr: str = filepath.read_text()
    reqs: List[str] = []
    for line in reqstr.splitlines(keepends=False):
        line = line.strip()  # noqa: PLW2901
        if not line:
            continue
        elif not line or line.startswith("#"):
            # comments are lines that start with # only
            continue
        elif line.startswith("-c"):
            _, new_filename = line.split()
            new_file_path = filepath.parent / new_filename.replace(".txt", ".in")
            if new_file_path not in visited:
                visited.add(new_file_path)
                reqs.extend(parse_reqs_in(new_file_path, visited))
        elif line.startswith(("-r", "--requirement")):
            _, new_filename = line.split()
            new_file_path = filepath.parent / new_filename
            if new_file_path not in visited:
                visited.add(new_file_path)
                reqs.extend(parse_reqs_in(new_file_path, visited))
        elif line.startswith("-f") or line.startswith("-i") or line.startswith("--"):
            continue
        elif line.startswith("-Z") or line.startswith("--always-unzip"):
            continue
        else:
            reqs.append(line)
    return reqs


here: Path = Path(__file__).parent.absolute()
requirements = parse_reqs_in(here / "requirements/prod.in")
dev_requirements = parse_reqs_in(here / "requirements/dev.in")
test_requirements = parse_reqs_in(here / "requirements/test.in")

setup(
    install_requires=requirements,
    tests_require=test_requirements,
    extras_require={"dev": dev_requirements, "test": test_requirements},
)
