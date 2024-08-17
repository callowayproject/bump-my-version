import subprocess

from bumpversion.config import Config
from bumpversion.hooks import run_setup_hooks
from tests.conftest import get_config_data


def setup_hook_env(config: Config) -> dict:
    """Mocked function for the environment setup"""
    return {}


def run_command(script: str, env: dict) -> subprocess.CompletedProcess:
    """Mocked function for command execution"""
    return subprocess.CompletedProcess(args=script, returncode=0)


def test_run_setup_hooks_calls_each_hook(mocker):
    """The run_setup_hooks function runs each hook."""
    # Assemble
    setup_hook_env_mock = mocker.patch("bumpversion.hooks.setup_hook_env", side_effect=setup_hook_env)
    run_command_mock = mocker.patch("bumpversion.hooks.run_command", side_effect=run_command)

    config, _, _ = get_config_data({"current_version": "0.1.0", "setup_hooks": ["script1", "script2"]})

    # Act
    result = run_setup_hooks(config)

    # Asserts for function's behavior
    setup_hook_env_mock.assert_called_once_with(config)
    assert run_command_mock.call_count == len(config.setup_hooks)
    run_command_mock.assert_any_call("script1", {})
    run_command_mock.assert_any_call("script2", {})
