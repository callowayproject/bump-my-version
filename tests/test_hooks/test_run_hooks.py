"""Tests for the run_hooks function."""

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
