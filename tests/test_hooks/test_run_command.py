import subprocess
import sys

import pytest

from bumpversion.hooks import run_command


class TestRunCommand:
    """Test the run_command function."""

    def test_runs_a_str_command(self):
        """Runs the command formatted as a string."""
        result = run_command("echo Hello")
        assert isinstance(result, subprocess.CompletedProcess)
        assert result.stdout == "Hello\n"

    def test_can_access_env(self):
        """The command can access custom environment variables."""
        cmd = "echo %TEST_ENV%" if sys.platform == "win32" else "echo $TEST_ENV"
        result = run_command(cmd, environment={"TEST_ENV": "Hello"})
        assert isinstance(result, subprocess.CompletedProcess)
        assert result.stdout == "Hello\n"

    def test_non_zero_exit(self):
        """The result shows a non-zero result code."""
        result = run_command("exit 1")
        assert result.returncode == 1

    @pytest.mark.parametrize(
        "invalid_script",
        [(123,), (None,), (["exit", "1"])],
    )
    def test_an_invalid_script_raises_type_error(self, invalid_script):
        with pytest.raises(TypeError):
            run_command(invalid_script)

    @pytest.mark.parametrize(
        "invalid_env",
        [("string",), (123,), (None,)],
    )
    def test_an_invalid_env_raises_type_error(self, invalid_env):
        with pytest.raises(TypeError):
            run_command("echo Hello", environment=invalid_env)
