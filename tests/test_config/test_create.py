"""Test the create function in the config module."""

from pathlib import Path
import pytest

from tests.conftest import inside_dir
from tomlkit import dumps

from bumpversion.config.create import create_configuration, get_defaults_from_dest
from bumpversion.config import DEFAULTS


BASIC_CONFIG = {
    "tool": {
        "bumpversion": {
            "commit": True,
            "tag": True,
            "current_version": "1.0.0",
            "parse": "(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+)(\\-(?P<release>[a-z]+))?",
            "serialize": ["{major}.{minor}.{patch}-{release}", "{major}.{minor}.{patch}"],
            "files": [
                {"filename": "setup.py"},
                {"filename": "bumpversion/__init__.py"},
                {"filename": "CHANGELOG.md", "search": "**unreleased**", "replace": "**v{new_version}**"},
            ],
            "parts": {
                "release": {
                    "optional_value": "gamma",
                    "values": ["dev", "gamma"],
                }
            },
        }
    }
}


@pytest.fixture
def default_config() -> dict:
    """The default configuration with the scm_info and parts removed."""
    defaults = DEFAULTS.copy()
    del defaults["scm_info"]
    del defaults["parts"]
    del defaults["files"]
    return defaults


class TestGetDefaultsFromDest:
    """Test the get_defaults_from_dest function."""

    def test_existing_path_returns_existing_config(self, tmp_path: Path, default_config: dict):
        """If the destination exists, the existing config should be returned."""
        dest_path = tmp_path / "pyproject-1.toml"
        dest_path.write_text(dumps(BASIC_CONFIG))

        with inside_dir(tmp_path):
            config, destination_config = get_defaults_from_dest("pyproject-1.toml")

        default_config.update(BASIC_CONFIG["tool"]["bumpversion"])
        del default_config["files"]
        del default_config["parts"]

        assert config == default_config

    def test_missing_path_returns_default_config(self, tmp_path: Path, default_config: dict):
        """If the destination does not exist, the default config should be returned."""
        with inside_dir(tmp_path):
            config, destination_config = get_defaults_from_dest("pyproject-2.toml")

        default_config["current_version"] = "0.1.0"

        assert config == default_config

    def test_existing_path_with_no_config_returns_default_config(self, tmp_path: Path, default_config: dict):
        """If the destination exists but has no config, the default config should be returned."""
        dest_path = tmp_path / "pyproject-3.toml"
        dest_path.write_text(dumps({"tool": {"poetry": {}}}))

        with inside_dir(tmp_path):
            config, destination_config = get_defaults_from_dest("pyproject-3.toml")

        default_config["current_version"] = "0.1.0"

        assert config == default_config

    def test_existing_path_with_project_version_uses_project_version(self, tmp_path: Path, default_config: dict):
        """If the destination exists and has a project version, the project version should be used as current_version."""
        dest_path = tmp_path / "pyproject-4.toml"
        dest_path.write_text(dumps({"tool": {"poetry": {}}, "project": {"version": "1.2.3"}}))

        with inside_dir(tmp_path):
            config, destination_config = get_defaults_from_dest("pyproject-4.toml")

        default_config["current_version"] = "1.2.3"
        assert config == default_config


class TestCreateConfiguration:
    """Test the create_configuration function."""

    def test_destination_without_prompt_returns_default_config(self, tmp_path: Path, default_config: dict):
        """If the destination is provided and no prompt is requested, the default config should be returned."""
        with inside_dir(tmp_path):
            destination_config = create_configuration("pyproject.toml", prompt=False)

        default_config["current_version"] = "0.1.0"
        default_config["commit_args"] = ""

        assert destination_config["tool"]["bumpversion"] == default_config

    def test_prompt_true_asks_questions_and_updates_result(self, tmp_path: Path, default_config: dict, mocker):
        """If prompt is True, the user should be prompted for the configuration."""
        answer = {
            "current_version": "1.2.3",
            "commit": True,
            "allow_dirty": True,
            "tag": True,
            "commit_args": "--no-verify",
        }
        mocked_questionary = mocker.patch("bumpversion.config.create.questionary", autospec=True)
        mocked_questionary.form.return_value.ask.return_value = answer
        with inside_dir(tmp_path):
            destination_config = create_configuration("pyproject.toml", prompt=True)

        default_config.update(answer)

        assert destination_config["tool"]["bumpversion"] == default_config
        assert mocked_questionary.form.return_value.ask.call_count == 1
