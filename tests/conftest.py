"""Testing fixtures for Pytest."""

import subprocess
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, Tuple

import pytest
from click.testing import CliRunner

from bumpversion.config import DEFAULTS, Config
from bumpversion.scm.models import SCMConfig
from bumpversion.versioning.models import Version
from bumpversion.versioning.version_config import VersionConfig


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


def get_config_data(overrides: dict) -> Tuple[Config, VersionConfig, Version]:
    """Get the configuration, version_config and version."""
    from bumpversion import config

    conf = config.get_configuration(config_file="missing", **overrides)
    version_config = VersionConfig(conf.parse, conf.serialize, conf.search, conf.replace, conf.parts)
    version = version_config.parse(conf.current_version)

    return conf, version_config, version


def get_semver(version: str) -> Version:
    """Get a semantic version from a string."""
    _, _, version = get_config_data({"current_version": version})
    return version


@pytest.fixture
def git_repo(tmp_path: Path) -> Path:
    """Generate a simple temporary git repo and return the path."""
    subprocess.run(  # noqa: S603
        ["git", "init", "--initial-branch=main"], cwd=tmp_path, check=True, capture_output=True  # noqa: S607
    )
    return tmp_path


@pytest.fixture
def hg_repo(tmp_path: Path) -> Path:
    """Generate a simple temporary mercurial repo and return the path."""
    subprocess.run(["hg", "init"], cwd=tmp_path, check=True, capture_output=True)  # noqa: S603, S607
    return tmp_path


@pytest.fixture
def runner() -> CliRunner:
    """Return a CliRunner instance."""
    return CliRunner()


@pytest.fixture
def scm_config() -> SCMConfig:
    """Dummy SCMConfig fixture."""
    return SCMConfig(
        tag=DEFAULTS["tag"],
        sign_tags=DEFAULTS["sign_tags"],
        tag_name=DEFAULTS["tag_name"],
        allow_dirty=DEFAULTS["allow_dirty"],
        commit=DEFAULTS["commit"],
        message=DEFAULTS["message"],
        moveable_tags=DEFAULTS["moveable_tags"],
        parse_pattern=DEFAULTS["parse"],
        tag_message=DEFAULTS["tag_message"],
        commit_args=DEFAULTS["commit_args"],
    )
