"""Tests for the run_hooks function."""

from bumpversion import hooks


def test_calls_each_hook(mocker):
    """It should call each hook passed to it."""
    # Assemble
    mock_logger = mocker.patch("bumpversion.hooks.logger")
    mock_run_command = mocker.patch("bumpversion.hooks.run_command")
    hooks_list = ["script1", "script2"]
    env = {"var": "value"}
    mock_run_command.return_value = mocker.MagicMock(stdout="output", stderr="error", returncode=0)

    # Act
    hooks.run_hooks(hooks_list, env)

    # Assert
    expected_calls = [
        mocker.call("Running 'script1'"),
        mocker.call("output"),
        mocker.call("error"),
        mocker.call("Exited with 0"),
        mocker.call("Running 'script2'"),
        mocker.call("output"),
        mocker.call("error"),
        mocker.call("Exited with 0"),
    ]
    mock_logger.debug.assert_has_calls(expected_calls)
    mock_run_command.assert_any_call("script1", env)
    mock_run_command.assert_any_call("script2", env)


def test_does_not_call_each_hook_when_dry_run(mocker):
    """It should not call each hook passed to it when dry_run is True."""
    # Assemble
    mock_logger = mocker.patch("bumpversion.hooks.logger")
    mock_run_command = mocker.patch("bumpversion.hooks.run_command")
    hooks_list = ["script1", "script2"]
    env = {"var": "value"}

    # Act
    hooks.run_hooks(hooks_list, env, dry_run=True)

    # Assert
    expected_calls = [mocker.call("Would run 'script1'"), mocker.call("Would run 'script2'")]
    mock_logger.debug.assert_has_calls(expected_calls)
    mock_run_command.assert_not_called()
