import subprocess
from typing import Callable

import pytest
from pytest import param
from bumpversion.hooks import run_setup_hooks, run_pre_commit_hooks, run_post_commit_hooks
from tests.conftest import get_config_data, get_semver


def get_hook_env(*args, **kwargs) -> dict:
    """Mocked function for the environment setup"""
    return {}


def run_command(script: str, env: dict) -> subprocess.CompletedProcess:
    """Mocked function for command execution"""
    return subprocess.CompletedProcess(args=script, returncode=0)


CURRENT_VERSION = get_semver("1.0.0")
NEW_VERSION = get_semver("1.1.0")


class TestHookSuites:
    """Run each hook suite through the same set of tests."""

    suites = (
        param("setup", run_setup_hooks, (CURRENT_VERSION,), id="setup"),
        param(
            "pre_commit",
            run_pre_commit_hooks,
            (
                CURRENT_VERSION,
                NEW_VERSION,
            ),
            id="pre_commit",
        ),
        param(
            "post_commit",
            run_post_commit_hooks,
            (
                CURRENT_VERSION,
                NEW_VERSION,
            ),
            id="post_commit",
        ),
    )

    @pytest.mark.parametrize(["suite_name", "suite_func", "suite_args"], suites)
    def test_calls_each_hook(self, mocker, suite_name: str, suite_func: Callable, suite_args: tuple):
        """The suite hook runs each hook."""
        # Arrange
        env = {"var": "value"}
        mock_env = mocker.patch(f"bumpversion.hooks.get_{suite_name}_hook_env")
        mock_env.return_value = env
        mock_run_command = mocker.patch("bumpversion.hooks.run_command")
        mock_run_command.return_value = mocker.MagicMock(stdout="output", stderr="error", returncode=0)
        mock_logger = mocker.patch("bumpversion.hooks.logger")

        config, _, _ = get_config_data({"current_version": "1.0.0", f"{suite_name}_hooks": ["script1", "script2"]})

        # Act
        suite_func(config, *suite_args)

        # Assert
        expected_info_calls = [
            mocker.call(f"Running {suite_name} hooks:".replace("_", "-")),
            mocker.call("Running 'script1'"),
            mocker.call("Running 'script2'"),
        ]
        mock_logger.info.assert_has_calls(expected_info_calls)
        mock_env.assert_called_once_with(config, *suite_args)
        expected_run_command_calls = [
            mocker.call("script1", env),
            mocker.call("script2", env),
        ]
        mock_run_command.assert_has_calls(expected_run_command_calls)

    @pytest.mark.parametrize(["suite_name", "suite_func", "suite_args"], suites)
    def test_does_not_run_hooks_if_none_are_specified(
        self, mocker, suite_name: str, suite_func: Callable, suite_args: tuple
    ):
        """If no setup_hooks are defined, nothing is run."""
        # Arrange
        env = {"var": "value"}
        mock_env = mocker.patch(f"bumpversion.hooks.get_{suite_name}_hook_env")
        mock_env.return_value = env
        mock_run_command = mocker.patch("bumpversion.hooks.run_command")
        mock_run_command.return_value = mocker.MagicMock(stdout="output", stderr="error", returncode=0)
        mock_logger = mocker.patch("bumpversion.hooks.logger")

        config, _, _ = get_config_data({"current_version": "1.0.0", f"{suite_name}_hooks": []})

        # Act
        suite_func(config, *suite_args)

        # Asserts
        mock_logger.info.assert_called_once_with(f"No {suite_name} hooks defined".replace("_", "-"))
        mock_env.assert_called_once_with(config, *suite_args)
        assert mock_run_command.call_count == 0

    @pytest.mark.parametrize(["suite_name", "suite_func", "suite_args"], suites)
    def test_does_not_run_hooks_if_dry_run_is_true(
        self, mocker, suite_name: str, suite_func: Callable, suite_args: tuple
    ):
        """If dry_run is True, nothing is run."""
        # Arrange
        env = {"var": "value"}
        mock_env = mocker.patch(f"bumpversion.hooks.get_{suite_name}_hook_env")
        mock_env.return_value = env
        mock_run_command = mocker.patch("bumpversion.hooks.run_hooks")
        mock_logger = mocker.patch("bumpversion.hooks.logger")

        config, _, _ = get_config_data({"current_version": "1.0.0", f"{suite_name}_hooks": ["script1", "script2"]})

        # Act
        args = [*suite_args, True]
        suite_func(config, *args)

        # Asserts
        mock_logger.info.assert_called_once_with(f"Would run {suite_name} hooks:".replace("_", "-"))
        mock_env.assert_called_once_with(config, *suite_args)
        assert mock_run_command.call_count == 1
