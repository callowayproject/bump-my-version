"""Tests of the configuration utilities."""

from pathlib import Path
from typing import Any, List

import tomlkit
import pytest
from pytest import param

from bumpversion.config.utils import get_all_file_configs, resolve_glob_files
from bumpversion.config.models import FileChange
from bumpversion.config import DEFAULTS
from tests.conftest import inside_dir, get_config_data


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

    def test_finds_all_files(self, fixtures_path: Path):
        """Test that all files are found."""
        overrides = {
            "current_version": "1.2.3",
            "files": [{"glob": "glob/**/*.txt", "ignore_missing_file": True, "ignore_missing_version": True}],
        }
        with inside_dir(fixtures_path):
            conf, version_config, current_version = get_config_data(overrides)
            assert len(conf.files_to_modify) == 3

    @pytest.mark.parametrize(
        ["glob_exclude", "expected_number"],
        [
            param(["**/*.cfg"], 0, id="recursive cfg excludes all"),
            param(["*.cfg"], 1, id="top level cfg excludes 1"),
            param(["subdir/*.cfg"], 1, id="subdir cfg excludes 1"),
            param(["subdir/adir/*.cfg"], 2, id="non-matching excludes 0"),
            param(["subdir/"], 2, id="raw subdir excludes 0"),
            param(["*.cfg", "subdir/*.cfg"], 0, id="combined top level and subdir cfg excludes all"),
        ],
    )
    def test_excludes_configured_patterns(self, tmp_path: Path, glob_exclude: List[str], expected_number: int):
        """Test that excludes configured patterns work."""
        file1 = tmp_path.joinpath("setup.cfg")
        file2 = tmp_path.joinpath("subdir/setup.cfg")
        file1.touch()
        file2.parent.mkdir()
        file2.touch()

        file_cfg = FileChange(
            filename=None,
            glob="**/*.cfg",
            glob_exclude=glob_exclude,
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

        assert len(resolved_files) == expected_number

    @pytest.mark.parametrize(
        ["glob_pattern", "expected_number"],
        [
            param("**/*.cfg|*.txt", 3, id="recursive cfg and text finds 3"),
            param("*.cfg|*.txt", 2, id="top level cfg and txt finds 2"),
            param("subdir/adir/*.cfg|*.toml", 0, id="non-matching finds 0"),
            param("subdir/|*.txt", 2, id="raw subdir and text finds 2"),
        ],
    )
    def test_combination_glob_patterns(self, tmp_path: Path, glob_pattern: str, expected_number: int):
        """Test that excludes configured patterns work."""
        file1 = tmp_path.joinpath("setup.cfg")
        file2 = tmp_path.joinpath("subdir/setup.cfg")
        file3 = tmp_path.joinpath("config.txt")
        file1.touch()
        file2.parent.mkdir()
        file2.touch()
        file3.touch()

        file_cfg = FileChange(
            filename=None,
            glob=glob_pattern,
            glob_exclude=[],
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
        print([x.filename for x in resolved_files])
        assert len(resolved_files) == expected_number
