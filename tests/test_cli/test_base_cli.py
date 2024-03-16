"""Tests for the base CLI commands."""

from bumpversion import cli


class TestBadOptionRaisesError:
    """Tests to ensure that bad options raise an error."""

    def test_bad_option_raises_error(self, runner):
        """Passing an invalid option should raise an error."""
        result = runner.invoke(cli.cli, ["--bad-option", "bump", "--current-version", "1.0.0", "patch"])
        assert result.exit_code != 0
        assert "No such option" in result.output
