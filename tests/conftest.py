"""Testing fixtures for Pytest."""
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def tests_path() -> Path:
    """Return the path containing the tests."""
    return Path(__file__).parent


@pytest.fixture
def fixtures_path(tests_path: Path) -> Path:
    """Return the path containing the testing fixtures."""
    return tests_path / "fixtures"


@contextmanager
def inside_dir(dirpath: Path) -> Generator:
    """
    Temporarily switch to a specific directory.

    Args:
        dirpath: Path of the directory to switch to
    """
    import os

    old_path = os.getcwd()
    try:
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(old_path)


def get_config_data(overrides: dict) -> tuple:
    """Get the configuration, version_config and version."""
    from bumpversion import config
    from bumpversion.version_part import VersionConfig

    conf = config.get_configuration(config_file="missing", **overrides)
    version_config = VersionConfig(conf.parse, conf.serialize, conf.search, conf.replace, conf.parts)
    version = version_config.parse(conf.current_version)

    return conf, version_config, version
