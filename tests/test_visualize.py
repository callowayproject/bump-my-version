"""Tests of the visualize module."""

from pathlib import Path

from bumpversion.visualize import Border, BOX_CHARS, connection_str, lead_string, labeled_line, visualize
from bumpversion.config import get_configuration


class TestLeadString:
    """Tests of the lead_string function."""

    def test_returns_string_with_bump(self):
        assert lead_string("1.0.0", Border(*BOX_CHARS["light"])) == "1.0.0 ── bump ─"

    def test_returns_blank_string(self):
        assert lead_string("1.0.0", Border(*BOX_CHARS["light"]), blank=True) == "               "


class TestConnectionStr:
    """Tests of the connection_str function."""

    def test_returns_correct_connection_string(self):
        border = Border(*BOX_CHARS["light"])
        assert connection_str(border, has_next=True, has_previous=True) == border.divider_right + border.line
        assert connection_str(border, has_next=True, has_previous=False) == border.divider_down + border.line
        assert connection_str(border, has_next=False, has_previous=True) == border.corner_bottom_left + border.line
        assert connection_str(border, has_next=False, has_previous=False) == border.line * 2


class TestLabeledLine:
    """Tests of the labeled_line function."""

    def test_no_label_fill_when_no_fit_length(self):
        """Without a fit_length, there will be no filler in the line."""
        border = Border(*BOX_CHARS["light"])
        assert labeled_line("major", border, fit_length=None) == " major ─ "

    def test_pads_label_if_fit_length(self):
        """Without a fit_length, there will be no filler in the line."""
        border = Border(*BOX_CHARS["light"])
        assert labeled_line("major", border, fit_length=10) == " major ────── "


class TestVisualize:
    """Tests of the visualize function."""

    def test_outputs_using_default_config(self, tmp_path: Path, capsys):
        """Test that the correct string is returned."""
        config = get_configuration(tmp_path.joinpath("missing.toml"), current_version="1.0.0")
        visualize(config, "1.0.0")
        captured = capsys.readouterr()
        assert captured.out == "\n".join(
            ["1.0.0 ── bump ─┬─ major ─ 2.0.0", "               ├─ minor ─ 1.1.0", "               ╰─ patch ─ 1.0.1\n"]
        )

    def test_indicates_invalid_paths(self, tmp_path: Path, fixtures_path: Path, capsys):
        """Test that the correct string is returned."""
        config_content = fixtures_path.joinpath("basic_cfg.toml").read_text()
        config_path = tmp_path.joinpath(".bumpversion-1.toml")
        config_path.write_text(config_content)
        config = get_configuration(config_path)
        visualize(config, "1.0.0")
        captured = capsys.readouterr()
        assert captured.out == "\n".join(
            [
                "1.0.0 ── bump ─┬─ major ─── 2.0.0-dev",
                "               ├─ minor ─── 1.1.0-dev",
                "               ├─ patch ─── 1.0.1-dev",
                "               ╰─ release ─ invalid: The part has already the maximum value among ['dev', 'gamma'] and cannot be bumped.\n",
            ]
        )
