"""Tests for the run_hooks function."""

import sys

from bumpversion import hooks
import pytest

from bumpversion.exceptions import HookError


def test_calls_each_hook(mocker):
    """It should call each hook passed to it."""
    # Arrange
    mock_logger = mocker.patch("bumpversion.hooks.logger")
    mock_run_command = mocker.patch("bumpversion.hooks.run_command")
    hooks_list = ["script1", "script2"]
    env = {"var": "value"}
    mock_run_command.return_value = mocker.MagicMock(stdout="output", stderr="error", returncode=0)

    # Act
    hooks.run_hooks(hooks_list, env)

    # Assert
    expected_info_calls = [
        mocker.call("Running 'script1'"),
        mocker.call("Running 'script2'"),
    ]
    mock_logger.info.assert_has_calls(expected_info_calls)
    expected_debug_calls = [
        mocker.call("Exited with 0"),
        mocker.call("output"),
        mocker.call("error"),
        mocker.call("Exited with 0"),
        mocker.call("output"),
        mocker.call("error"),
    ]
    mock_logger.debug.assert_has_calls(expected_debug_calls)
    mock_run_command.assert_any_call("script1", env)
    mock_run_command.assert_any_call("script2", env)


def test_raises_exception_if_hook_fails(mocker):
    """If a hook responds with an error, an exception should be raised."""
    # Arrange
    mock_logger = mocker.patch("bumpversion.hooks.logger")
    mock_run_command = mocker.patch("bumpversion.hooks.run_command")
    hooks_list = ["script1", "script2"]
    env = {"var": "value"}
    mock_run_command.return_value = mocker.MagicMock(stdout="output", stderr="error", returncode=1)

    # Act
    with pytest.raises(HookError):
        hooks.run_hooks(hooks_list, env)

    # Assert
    expected_info_calls = [mocker.call("Running 'script1'")]
    expected_warning_calls = [mocker.call("output"), mocker.call("error")]
    mock_logger.info.assert_has_calls(expected_info_calls)
    mock_logger.warning.assert_has_calls(expected_warning_calls)
    mock_run_command.assert_any_call("script1", env)


def test_does_not_call_each_hook_when_dry_run(mocker):
    """It should not call each hook passed to it when dry_run is True."""
    # Arrange
    mock_logger = mocker.patch("bumpversion.hooks.logger")
    mock_run_command = mocker.patch("bumpversion.hooks.run_command")
    hooks_list = ["script1", "script2"]
    env = {"var": "value"}

    # Act
    hooks.run_hooks(hooks_list, env, dry_run=True)

    # Assert
    expected_calls = [mocker.call("Would run 'script1'"), mocker.call("Would run 'script2'")]
    mock_logger.info.assert_has_calls(expected_calls)
    mock_run_command.assert_not_called()


def test_shell_syntax_raises_hook_error_by_default():
    """A hook with shell syntax raises HookError when allow_shell_hooks is False (the default)."""
    env = {"var": "value"}
    shell_hooks = ["echo hello | cat"]

    with pytest.raises(HookError, match="allow_shell_hooks"):
        hooks.run_hooks(shell_hooks, env, allow_shell_hooks=False)


def test_shell_variable_expansion_raises_hook_error_by_default():
    """A hook using $VAR expansion raises HookError when allow_shell_hooks is False."""
    env = {"var": "value"}
    shell_hooks = ["echo $MY_VAR"]

    with pytest.raises(HookError, match="allow_shell_hooks"):
        hooks.run_hooks(shell_hooks, env, allow_shell_hooks=False)


def test_shell_syntax_allowed_when_opt_in_enabled():
    """A hook with shell syntax runs successfully when allow_shell_hooks=True."""
    env = {}
    shell_hooks = [f"{sys.executable} -c \"import sys; sys.exit(0)\""]

    # No error raised; pipe-free hook with allow_shell_hooks just runs normally
    hooks.run_hooks(shell_hooks, env, allow_shell_hooks=True)


def test_shell_pipe_runs_when_opt_in_enabled(mocker):
    """A hook using a pipe executes with shell=True when allow_shell_hooks=True."""
    mocker.patch("bumpversion.hooks.logger")
    mock_subprocess = mocker.patch("bumpversion.hooks.subprocess.run")
    mock_subprocess.return_value = mocker.MagicMock(stdout="output", stderr="", returncode=0)

    env = {}
    hooks.run_hooks(["echo hello | cat"], env, allow_shell_hooks=True)

    mock_subprocess.assert_called_once_with(
        "echo hello | cat",
        env=env,
        encoding="utf-8",
        shell=True,
        text=True,
        capture_output=True,
        check=False,
    )


def test_shell_opt_in_emits_warning(mocker):
    """When a shell-syntax hook runs under allow_shell_hooks=True, a warning is logged."""
    mock_logger = mocker.patch("bumpversion.hooks.logger")
    mock_subprocess = mocker.patch("bumpversion.hooks.subprocess.run")
    mock_subprocess.return_value = mocker.MagicMock(stdout="", stderr="", returncode=0)

    hooks.run_hooks(["echo $VAR"], {}, allow_shell_hooks=True)

    mock_logger.warning.assert_any_call(
        "Hook 'echo $VAR' uses shell syntax. Consider rewriting as an explicit command."
    )
