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

    def test_env_is_passed_to_subprocess(self):
        """The subprocess receives custom environment variables via env, without shell expansion in args."""
        result = run_command(
            f"{sys.executable} -c \"import os; print(os.environ['TEST_ENV'])\"",
            environment={"TEST_ENV": "Hello"},
        )
        assert isinstance(result, subprocess.CompletedProcess)
        assert result.stdout == "Hello\n"

    def test_non_zero_exit(self):
        """The result shows a non-zero result code."""
        result = run_command(f"{sys.executable} -c \"import sys; sys.exit(1)\"")
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

    def test_no_shell_expansion_of_args(self):
        """With shell=False, $VAR in command args is not expanded by the shell."""
        result = run_command("echo $TEST_ENV", environment={"TEST_ENV": "Hello"})
        # $TEST_ENV is passed literally to echo, not expanded
        assert result.stdout.strip() == "$TEST_ENV"
