"""Tests for environment generation for hooks."""

import datetime
import os
import subprocess
from pathlib import Path

from bumpversion.hooks import (
    scm_env,
    PREFIX,
    base_env,
    version_env,
    new_version_env,
    get_setup_hook_env,
    get_pre_commit_hook_env,
)
from tests.conftest import inside_dir, get_config_data


def assert_os_environ_items_included(result_env: dict) -> None:
    """Assert that the OS environment variables are in the result."""
    for var, value in os.environ.items():
        assert var in result_env
        assert result_env[var] == value


def assert_scm_info_included(result_env: dict):
    """Assert the SCM information is included in the result."""
    assert f"{PREFIX}COMMIT_SHA" in result_env
    assert f"{PREFIX}DISTANCE_TO_LATEST_TAG" in result_env
    assert f"{PREFIX}IS_DIRTY" in result_env
    assert f"{PREFIX}BRANCH_NAME" in result_env
    assert f"{PREFIX}SHORT_BRANCH_NAME" in result_env
    assert f"{PREFIX}CURRENT_VERSION" in result_env
    assert f"{PREFIX}CURRENT_TAG" in result_env


def assert_current_version_info_included(result_env: dict):
    """Assert the current version information is included in the result."""
    assert f"{PREFIX}CURRENT_MAJOR" in result_env
    assert f"{PREFIX}CURRENT_MINOR" in result_env
    assert f"{PREFIX}CURRENT_PATCH" in result_env


def assert_new_version_info_included(result_env: dict):
    """Assert the new version information is included in the result."""
    assert f"{PREFIX}NEW_MAJOR" in result_env
    assert f"{PREFIX}NEW_MINOR" in result_env
    assert f"{PREFIX}NEW_PATCH" in result_env
    assert f"{PREFIX}NEW_VERSION" in result_env
    assert f"{PREFIX}NEW_VERSION_TAG" in result_env


def test_scm_env_returns_correct_info(git_repo: Path):
    """Should return information about the latest tag."""
    readme = git_repo.joinpath("readme.md")
    readme.touch()
    tag_prefix = "v"
    overrides = {"current_version": "0.1.0", "commit": True, "tag": True, "tag_name": f"{tag_prefix}{{new_version}}"}

    with inside_dir(git_repo):
        # Add a file and tag
        subprocess.run(["git", "add", "readme.md"])
        subprocess.run(["git", "commit", "-m", "first"])
        subprocess.run(["git", "tag", f"{tag_prefix}0.1.0"])
        conf, _, _ = get_config_data(overrides)

    result = scm_env(conf)
    assert result[f"{PREFIX}BRANCH_NAME"] == "main"
    assert len(result[f"{PREFIX}COMMIT_SHA"]) == 40
    assert result[f"{PREFIX}CURRENT_TAG"] == "v0.1.0"
    assert result[f"{PREFIX}CURRENT_VERSION"] == "0.1.0"
    assert result[f"{PREFIX}DISTANCE_TO_LATEST_TAG"] == "0"
    assert result[f"{PREFIX}IS_DIRTY"] == "False"
    assert result[f"{PREFIX}SHORT_BRANCH_NAME"] == "main"


class MockDatetime(datetime.datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(2022, 2, 1, 17) if tz else cls(2022, 2, 1, 12)


class TestBaseEnv:
    """Tests for base_env function."""

    def test_includes_now_and_utcnow(self, mocker):
        """The output includes NOW and UTCNOW."""
        mocker.patch("datetime.datetime", new=MockDatetime)
        config, _, _ = get_config_data({"current_version": "0.1.0"})
        result_env = base_env(config)

        assert f"{PREFIX}NOW" in result_env
        assert f"{PREFIX}UTCNOW" in result_env
        assert result_env[f"{PREFIX}NOW"] == "2022-02-01T12:00:00"
        assert result_env[f"{PREFIX}UTCNOW"] == "2022-02-01T17:00:00"

    def test_includes_os_environ(self):
        """The output includes the current process' environment."""
        config, _, _ = get_config_data({"current_version": "0.1.0"})
        result_env = base_env(config)

        assert_os_environ_items_included(result_env)

    def test_includes_scm_info(self):
        """The output includes SCM information."""
        config, _, _ = get_config_data({"current_version": "0.1.0"})
        result_env = base_env(config)

        assert_scm_info_included(result_env)


def test_current_version_env_includes_correct_info():
    """The version_env for a version should include all its parts"""
    config, _, current_version = get_config_data(
        {"current_version": "0.1.0", "parse": r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)"}
    )
    result = version_env(current_version, "CURRENT_")

    assert result[f"{PREFIX}CURRENT_MAJOR"] == "0"
    assert result[f"{PREFIX}CURRENT_MINOR"] == "1"
    assert result[f"{PREFIX}CURRENT_PATCH"] == "0"


def test_new_version_env_includes_correct_info():
    """The new_version_env should return the serialized version and tag name."""

    config, _, current_version = get_config_data(
        {"current_version": "0.1.0", "parse": r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)"}
    )
    new_version = current_version.bump("minor")
    result = new_version_env(config, current_version, new_version)

    assert result[f"{PREFIX}NEW_VERSION"] == "0.2.0"
    assert result[f"{PREFIX}NEW_VERSION_TAG"] == "v0.2.0"


def test_get_setup_hook_env_includes_correct_info():
    """The setup hook environment should contain specific information."""
    config, _, current_version = get_config_data({"current_version": "0.1.0"})
    result_env = get_setup_hook_env(config, current_version)

    assert_os_environ_items_included(result_env)
    assert_scm_info_included(result_env)
    assert_current_version_info_included(result_env)


def test_get_pre_commit_hook_env_includes_correct_info():
    """The pre-commit hook environment should contain specific information."""
    config, _, current_version = get_config_data({"current_version": "0.1.0"})
    new_version = current_version.bump("minor")
    result_env = get_pre_commit_hook_env(config, current_version, new_version)

    assert_os_environ_items_included(result_env)
    assert_scm_info_included(result_env)
    assert_current_version_info_included(result_env)
    assert_new_version_info_included(result_env)
