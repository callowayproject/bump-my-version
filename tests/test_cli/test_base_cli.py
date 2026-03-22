"""Tests for the base CLI commands."""

from bumpversion import cli


class TestBadOptionRaisesError:
    """Tests to ensure that bad options raise an error."""

    def test_bad_option_raises_error(self, runner):
        """Passing an invalid option should raise an error."""
        result = runner.invoke(cli.cli, ["--bad-option", "bump", "--current-version", "1.0.0", "patch"])
        assert result.exit_code != 0
        assert "No such option" in result.output


class TestCommandRegistration:
    """Ensure all expected commands are registered on the root CLI group."""

    def test_bump_registered(self):
        """The bump command must be registered."""
        assert "bump" in cli.cli.commands

    def test_show_registered(self):
        """The show command must be registered."""
        assert "show" in cli.cli.commands

    def test_replace_registered(self):
        """The replace command must be registered."""
        assert "replace" in cli.cli.commands

    def test_sample_config_registered(self):
        """The sample-config command must be registered."""
        assert "sample-config" in cli.cli.commands

    def test_show_bump_registered(self):
        """The show-bump command must be registered."""
        assert "show-bump" in cli.cli.commands


def _get_param(command_name: str, param_name: str):
    """Return the Click parameter object for *param_name* on *command_name*."""
    cmd = cli.cli.commands[command_name]
    return next((p for p in cmd.params if p.name == param_name), None)


class TestBumpDefaults:
    """Critical default-value assertions for the bump command."""

    def test_regex_default_is_none(self):
        """bump --regex/--no-regex must default to None (tri-state, not True/False)."""
        param = _get_param("bump", "regex")
        assert param is not None, "regex param not found on bump"
        assert param.default is None

    def test_ignore_missing_files_default_is_none(self):
        """bump --ignore-missing-files must be a tri-state flag defaulting to None."""
        param = _get_param("bump", "ignore_missing_files")
        assert param is not None, "ignore_missing_files param not found on bump"
        assert param.default is None

    def test_ignore_missing_version_default_is_none(self):
        """bump --ignore-missing-version must be a tri-state flag defaulting to None."""
        param = _get_param("bump", "ignore_missing_version")
        assert param is not None, "ignore_missing_version param not found on bump"
        assert param.default is None


class TestReplaceDefaults:
    """Critical default-value assertions for the replace command."""

    def test_regex_default_is_none(self):
        """replace --regex/--no-regex must default to None (tri-state)."""
        param = _get_param("replace", "regex")
        assert param is not None, "regex param not found on replace"
        assert param.default is None

    def test_ignore_missing_files_is_flag(self):
        """replace --ignore-missing-files must be a simple boolean flag (no --no- counterpart)."""
        param = _get_param("replace", "ignore_missing_files")
        assert param is not None, "ignore_missing_files param not found on replace"
        assert param.is_flag
        assert param.default is False

    def test_ignore_missing_version_is_flag(self):
        """replace --ignore-missing-version must be a simple boolean flag (no --no- counterpart)."""
        param = _get_param("replace", "ignore_missing_version")
        assert param is not None, "ignore_missing_version param not found on replace"
        assert param.is_flag
        assert param.default is False
