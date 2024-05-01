"""Tests of the configuration utilities."""

from pathlib import Path
from typing import Any, List

import tomlkit
import pytest
from pytest import param

from bumpversion.config.utils import get_all_file_configs, resolve_glob_files, glob_exclude_pattern
from bumpversion.config.models import FileChange
from bumpversion.config import DEFAULTS
from tests.conftest import inside_dir


def write_config(tmp_path: Path, overrides: dict) -> Path:
    """Write a configuration file."""
    config_file = tmp_path / ".bumpversion.toml"
    defaults = DEFAULTS.copy()
    defaults.pop("parts")
    defaults.pop("scm_info")
    defaults["current_version"] = defaults["current_version"] or "1.2.3"
    defaults["commit_args"] = ""
    config = {"tool": {"bumpversion": {**defaults, **overrides}}}
    config_file.write_text(tomlkit.dumps(config), encoding="utf-8")
    return config_file


class TestGetAllFileConfigs:
    """Tests for the get_all_file_configs function."""

    def test_uses_defaults_for_missing_keys(self, tmp_path: Path):
        """Test the get_all_file_configs function."""
        config_file = write_config(tmp_path, {"files": [{"filename": "setup.cfg"}]})
        config_dict = tomlkit.loads(config_file.read_text())["tool"]["bumpversion"]
        file_configs = get_all_file_configs(config_dict)

        for key in FileChange.model_fields.keys():
            global_key = key if key != "ignore_missing_file" else "ignore_missing_files"
            if key not in ["filename", "glob", "key_path", "glob_exclude"]:
                file_val = getattr(file_configs[0], key)
                assert file_val == DEFAULTS[global_key]

    @pytest.mark.parametrize(
        ["attribute", "global_value", "file_value"],
        [
            param("parse", DEFAULTS["parse"], r"v(?P<major>\d+)", id="parse"),
            param("serialize", DEFAULTS["serialize"], ("v{major}",), id="serialize"),
            param("search", DEFAULTS["search"], "v{current_version}", id="search"),
            param("replace", DEFAULTS["replace"], "v{new_version}", id="replace"),
            param("ignore_missing_version", True, False, id="ignore_missing_version"),
            param("ignore_missing_files", True, False, id="ignore_missing_files"),
            param("regex", True, False, id="regex"),
        ],
    )
    def test_overrides_defaults(self, tmp_path: Path, attribute: str, global_value: Any, file_value: Any):
        """Configured attributes in the file should override global options."""
        file_attribute = attribute if attribute != "ignore_missing_files" else "ignore_missing_file"
        config_file = write_config(
            tmp_path,
            {
                attribute: global_value,
                "files": [
                    {
                        "filename": "setup.cfg",
                        file_attribute: file_value,
                    }
                ],
            },
        )
        config_dict = tomlkit.loads(config_file.read_text())["tool"]["bumpversion"]
        file_configs = get_all_file_configs(config_dict)
        assert len(file_configs) == 1
        assert file_configs[0].filename == "setup.cfg"
        assert getattr(file_configs[0], file_attribute) == file_value


class TestResolveGlobFiles:
    """Tests for the resolve_glob_files function."""

    def test_all_attributes_are_copied(self, tmp_path: Path):
        """Test that all attributes are copied."""
        file1 = tmp_path.joinpath("setup.cfg")
        file2 = tmp_path.joinpath("subdir/setup.cfg")
        file1.touch()
        file2.parent.mkdir()
        file2.touch()

        file_cfg = FileChange(
            filename=None,
            glob="**/*.cfg",
            key_path=None,
            parse=r"v(?P<major>\d+)",
            serialize=("v{major}",),
            search="v{current_version}",
            replace="v{new_version}",
            ignore_missing_version=True,
            ignore_missing_file=True,
            regex=True,
        )
        with inside_dir(tmp_path):
            resolved_files = resolve_glob_files(file_cfg)

        assert len(resolved_files) == 2
        for resolved_file in resolved_files:
            assert resolved_file.filename.endswith("setup.cfg")
            assert resolved_file.glob is None
            assert resolved_file.key_path is None
            assert resolved_file.parse == r"v(?P<major>\d+)"
            assert resolved_file.serialize == ("v{major}",)
            assert resolved_file.search == "v{current_version}"
            assert resolved_file.replace == "v{new_version}"
            assert resolved_file.ignore_missing_version is True
            assert resolved_file.ignore_missing_file is True
            assert resolved_file.regex is True

    def test_excludes_configured_patterns(self, tmp_path: Path):
        """Test that excludes configured patterns work."""
        file1 = tmp_path.joinpath("setup.cfg")
        file2 = tmp_path.joinpath("subdir/setup.cfg")
        file1.touch()
        file2.parent.mkdir()
        file2.touch()

        file_cfg = FileChange(
            filename=None,
            glob="**/*.cfg",
            glob_exclude=["subdir/**"],
            key_path=None,
            parse=r"v(?P<major>\d+)",
            serialize=("v{major}",),
            search="v{current_version}",
            replace="v{new_version}",
            ignore_missing_version=True,
            ignore_missing_file=True,
            regex=True,
        )
        with inside_dir(tmp_path):
            resolved_files = resolve_glob_files(file_cfg)

        assert len(resolved_files) == 1


class TestGlobExcludePattern:
    """Tests for the glob_exclude_pattern function."""

    @pytest.mark.parametrize(["empty_pattern"], [param([], id="empty list"), param(None, id="None")])
    def test_empty_list_returns_empty_string_pattern(self, empty_pattern: Any):
        """When passed an empty list, it should return a pattern that only matches an empty string."""
        assert glob_exclude_pattern(empty_pattern).pattern == r"^$"

    @pytest.mark.parametrize(
        ["patterns", "expected"],
        [
            param(["foo.txt", ""], "(?s:foo\\.txt)\\Z", id="empty string"),
            param(["foo.txt", None], "(?s:foo\\.txt)\\Z", id="None value"),
            param(["foo.txt", "", "bar.txt"], "(?s:foo\\.txt)\\Z|(?s:bar\\.txt)\\Z", id="Empty string in the middle"),
        ],
    )
    def test_empty_values_are_excluded(self, patterns: List, expected: str):
        """Empty values are excluded from the compiled pattern."""
        assert glob_exclude_pattern(patterns).pattern == expected

    def test_list_of_empty_patterns_return_empty_string_pattern(self):
        """When passed a list of empty strings, it should return a pattern that only matches an empty string."""
        assert glob_exclude_pattern(["", "", None]).pattern == r"^$"

    def test_trailing_slash_appends_stars(self):
        """
        When a string has a trailing slash, two asterisks are appended.

        `fnmatch.translate` converts `**` to `.*`
        """
        assert glob_exclude_pattern(["foo/"]).pattern == "(?s:foo/.*)\\Z"

    @pytest.mark.parametrize(
        ["file_path", "excluded"],
        [param("node_modules/foo/file.js", True), param("build/foo/file.js", True), param("code/file.js", False)],
    )
    def test_output_pattern_matches_files(self, file_path: str, excluded: bool):
        """The output pattern should match file paths appropriately."""
        exclude_matcher = glob_exclude_pattern(["node_modules/", "build/"])

        if excluded:
            assert exclude_matcher.match(file_path)
        else:
            assert not exclude_matcher.match(file_path)
