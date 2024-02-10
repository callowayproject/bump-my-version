"""Test configuration parsing."""

import difflib
import json
from pathlib import Path

from click.testing import CliRunner, Result
import pytest
from pytest import LogCaptureFixture, param, TempPathFactory

from bumpversion.utils import get_context
from bumpversion import config
from bumpversion.config.files import find_config_file, CONFIG_FILE_SEARCH_ORDER
import bumpversion.config.utils

from tests.conftest import inside_dir, get_config_data


class TestFindConfigFile:
    """Tests for finding the config file."""

    class TestWhenExplictConfigFileIsPassed:
        """Tests for when an explicit config file is passed."""

        def test_returns_path_to_existing_file(self, tmp_path: Path) -> None:
            """If an explicit config file is passed, it should be returned."""
            cfg_file = tmp_path / "bump.toml"
            cfg_file.write_text('[tool.bumpversion]\ncurrent_version = "1.0.0"')
            assert find_config_file(cfg_file) == cfg_file

        def test_returns_none_when_missing_file(self, tmp_path: Path) -> None:
            """If an explicit config file is passed, it should be returned."""
            cfg_file = tmp_path / "bump.toml"
            assert find_config_file(cfg_file) is None

    class TestWhenNoExplicitConfigFileIsPassed:
        """Tests for when no explicit config file is passed."""

        @pytest.mark.parametrize(
            ["cfg_file_name"],
            (param(item, id=item) for item in CONFIG_FILE_SEARCH_ORDER),
        )
        def test_returns_path_to_existing_default_file(self, tmp_path: Path, cfg_file_name: str) -> None:
            """If no explicit config file is passed, it returns the path to an existing expected file."""
            cfg_file = tmp_path / cfg_file_name
            cfg_file.write_text('[tool.bumpversion]\ncurrent_version = "1.0.0"')
            with inside_dir(tmp_path):
                assert find_config_file() == cfg_file

        def test_returns_none_when_missing_file(self, tmp_path: Path) -> None:
            """If an explicit config file is passed, it should be returned."""
            with inside_dir(tmp_path):
                assert find_config_file() is None

        def test_returns_path_to_existing_file_in_correct_order(self, tmp_path: Path) -> None:
            """If no explicit config file is passed, it returns the path to an existing expected file."""
            expected_order = list(CONFIG_FILE_SEARCH_ORDER)[:]  # make a copy so we can mutate it
            cfg_file_paths = [tmp_path / cfg_file_name for cfg_file_name in expected_order]
            for cfg_file in cfg_file_paths:  # create all the files
                cfg_file.write_text('[tool.bumpversion]\ncurrent_version = "1.0.0"')

            with inside_dir(tmp_path):
                while expected_order:
                    expected_file = expected_order.pop(0)  # the top item in the list is the next expected file
                    expected_path = tmp_path / expected_file
                    assert find_config_file() == expected_path
                    expected_path.unlink()  # remove the file so it doesn't get found again


class TestReadConfigFile:
    """Tests for reading the config file."""

    class TestWhenExplictConfigFileIsPassed:
        def test_returns_empty_dict_when_missing_file(
            self, tmp_path_factory: TempPathFactory, caplog: LogCaptureFixture
        ) -> None:
            """If an explicit config file is passed and doesn't exist, it returns an empty dict."""
            caplog.set_level("INFO")
            tmp_path = tmp_path_factory.mktemp("explicit-file-passed-")
            cfg_file = tmp_path / "bump.toml"
            with inside_dir(tmp_path):
                assert config.read_config_file(cfg_file) == {}
                assert "Configuration file not found" in caplog.text

        def test_returns_dict_of_cfg_file(self, fixtures_path: Path) -> None:
            """Files with a .cfg suffix is parsed into a dict and returned."""
            cfg_file = fixtures_path / "basic_cfg.cfg"
            expected = json.loads(fixtures_path.joinpath("basic_cfg_expected.json").read_text())
            assert config.read_config_file(cfg_file) == expected

        def test_returns_dict_of_toml_file(self, fixtures_path: Path) -> None:
            """Files with a .toml suffix is parsed into a dict and returned."""
            cfg_file = fixtures_path / "basic_cfg.toml"
            expected = json.loads(fixtures_path.joinpath("basic_cfg_expected.json").read_text())
            assert config.read_config_file(cfg_file) == expected

        def test_returns_empty_dict_with_unknown_suffix(
            self, tmp_path_factory: TempPathFactory, caplog: LogCaptureFixture
        ) -> None:
            """Files with an unknown suffix return an empty dict."""
            caplog.set_level("INFO")
            tmp_path = tmp_path_factory.mktemp("explicit-file-passed-")
            cfg_file = tmp_path / "basic_cfg.unknown"
            cfg_file.write_text('[tool.bumpversion]\ncurrent_version = "1.0.0"')
            with inside_dir(tmp_path):
                assert config.read_config_file(cfg_file) == {}
            assert "Unknown config file suffix" in caplog.text

    class TestWhenNoConfigFileIsPassed:
        """Tests for when no explicit config file is passed."""

        def test_returns_empty_dict(self, caplog: LogCaptureFixture) -> None:
            """If no explicit config file is passed, it returns an empty dict."""
            caplog.set_level("INFO")
            assert config.read_config_file() == {}
            assert "No configuration file found." in caplog.text


@pytest.mark.parametrize(
    ["conf_file", "expected_file"],
    [
        param("basic_cfg.toml", "basic_cfg_expected.json", id="toml basic cfg"),
    ],
)
def test_read_toml_file(conf_file: str, expected_file: str, fixtures_path: Path) -> None:
    """Parsing the config file should match the expected results."""
    result = bumpversion.config.files.read_toml_file(fixtures_path.joinpath(conf_file))
    expected = json.loads(fixtures_path.joinpath(expected_file).read_text())
    assert result == expected


def test_multiple_config_files(tmp_path: Path):
    """If there are multiple config files, the first one with content wins."""
    setup_cfg = tmp_path / "setup.cfg"
    setup_cfg.write_text("[metadata]\nname: just-a-name\n")
    bumpversion_cfg = tmp_path / ".bumpversion.cfg"
    bumpversion_cfg.write_text("\n")
    pyproject_toml = tmp_path / "pyproject.toml"
    pyproject_toml.write_text(
        "[tool.bumpversion]\n"
        'current_version = "0.10.5"\n'
        'parse = "(?P<major>\\\\d+)\\\\.(?P<minor>\\\\d+)\\\\.(?P<patch>\\\\d+)(\\\\-(?P<release>[a-z]+))?"\n'
        "serialize = [\n"
        '    "{major}.{minor}.{patch}-{release}",\n'
        '    "{major}.{minor}.{patch}"\n'
        "]\n"
    )
    with inside_dir(tmp_path):
        cfg_file = bumpversion.config.files.find_config_file()
        cfg = config.get_configuration(cfg_file)

    assert cfg.current_version == "0.10.5"
    assert cfg.parse == "(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+)(\\-(?P<release>[a-z]+))?"
    assert cfg.serialize == ("{major}.{minor}.{patch}-{release}", "{major}.{minor}.{patch}")


TOML_EXPECTED_DIFF = (
    "*** \n"
    "--- \n"
    "***************\n"
    "*** 23 ****\n"
    '! current_version = "1.0.0"\n'
    "--- 23 ----\n"
    '! current_version = "1.0.1"\n'
)


@pytest.mark.parametrize(
    [
        "cfg_file_name",
    ],
    [
        ("pyproject.toml",),
    ],
)
def test_update_config_file(tmp_path: Path, cfg_file_name: str, fixtures_path: Path) -> None:
    """
    Make sure only the version string is updated in the config file.
    """
    expected_diff = TOML_EXPECTED_DIFF
    cfg_path = tmp_path / cfg_file_name
    orig_path = fixtures_path / f"basic_cfg{cfg_path.suffix}"
    cfg_path.write_text(orig_path.read_text())
    original_content = orig_path.read_text().splitlines(keepends=True)
    with inside_dir(tmp_path):
        cfg = config.get_configuration(cfg_path)
        ctx = get_context(cfg)
    current_version = cfg.version_config.parse("1.0.0")
    new_version = cfg.version_config.parse("1.0.1")
    bumpversion.config.files.update_config_file(cfg_path, cfg, current_version, new_version, ctx)
    new_content = cfg_path.read_text().splitlines(keepends=True)
    difference = difflib.context_diff(original_content, new_content, n=0)
    assert "".join(difference) == expected_diff


def test_pep440_config(git_repo: Path, fixtures_path: Path):
    """
    Check the PEP440 config file.
    """
    from bumpversion.utils import get_context
    from bumpversion.bump import get_next_version
    from bumpversion import cli
    import subprocess

    # Arrange

    cfg_path = git_repo / "pyproject.toml"
    orig_path = fixtures_path / "pep440.toml"
    cfg_path.write_text(orig_path.read_text())
    version_path = git_repo / "VERSION"
    version_path.write_text("1.0.0")
    readme_path = git_repo / "README.md"
    runner: CliRunner = CliRunner()

    with inside_dir(git_repo):
        subprocess.run(["git", "add", "VERSION"], check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "initial commit"], check=True, capture_output=True)
        subprocess.run(["git", "tag", "v1.0.0"], check=True, capture_output=True)

        cfg = config.get_configuration(cfg_path)
        ctx = get_context(cfg)
        version = cfg.version_config.parse(cfg.current_version)
        next_version = get_next_version(version, cfg, "patch", None)
        next_version_str = cfg.version_config.serialize(next_version, ctx)
        assert next_version_str == "1.0.1"

        subprocess.run(["git", "checkout", "-b", "my-really-LONG-branch_name"], check=True, capture_output=True)
        readme_path.write_text("This is my branch!")
        result: Result = runner.invoke(cli.cli, ["bump", "dev_label", "--no-tag"])
        assert result.exit_code == 0
        cfg = config.get_configuration(cfg_path)
        assert cfg.current_version == "1.0.0.dev0+myreallylongbranchna"


@pytest.mark.parametrize(
    ["glob_pattern", "file_list"],
    [
        param("*.txt", {Path("file1.txt"), Path("file2.txt")}, id="simple-glob"),
        param("**/*.txt", {Path("file1.txt"), Path("file2.txt"), Path("directory/file3.txt")}, id="recursive-glob"),
    ],
)
def test_get_glob_files(glob_pattern: str, file_list: set, fixtures_path: Path):
    """Get glob files should return all the globbed files and nothing else."""
    overrides = {
        "current_version": "1.0.0",
        "parse": r"(?P<major>\d+)\.(?P<minor>\d+)(\.(?P<release>[a-z]+))?",
        "serialize": ["{major}.{minor}.{release}", "{major}.{minor}"],
        "files": [
            {
                "glob": glob_pattern,
            }
        ],
    }
    conf, version_config, current_version = get_config_data(overrides)
    with inside_dir(fixtures_path.joinpath("glob")):
        result = bumpversion.config.utils.resolve_glob_files(conf.files[0])

    assert len(result) == len(file_list)
    for f in result:
        assert Path(f.filename) in file_list


def test_file_overrides_config(fixtures_path: Path):
    """If a file has a different config, it should override the main config."""
    cfg_file = fixtures_path / "file_config_overrides.toml"
    conf = config.get_configuration(cfg_file)
    file_map = {f.filename: f for f in conf.files}
    assert file_map["should_contain_defaults.txt"].parse == conf.parse
    assert file_map["should_contain_defaults.txt"].serialize == conf.serialize
    assert file_map["should_contain_defaults.txt"].search == conf.search
    assert file_map["should_contain_defaults.txt"].replace == conf.replace
    assert file_map["should_contain_defaults.txt"].regex == conf.regex
    assert file_map["should_contain_defaults.txt"].ignore_missing_version == conf.ignore_missing_version

    assert file_map["should_override_search.txt"].parse == conf.parse
    assert file_map["should_override_search.txt"].serialize == conf.serialize
    assert file_map["should_override_search.txt"].search == "**unreleased**"
    assert file_map["should_override_search.txt"].replace == conf.replace
    assert file_map["should_override_search.txt"].regex == conf.regex
    assert file_map["should_override_search.txt"].ignore_missing_version == conf.ignore_missing_version

    assert file_map["should_override_replace.txt"].parse == conf.parse
    assert file_map["should_override_replace.txt"].serialize == conf.serialize
    assert file_map["should_override_replace.txt"].search == conf.search
    assert file_map["should_override_replace.txt"].replace == "**unreleased**"
    assert file_map["should_override_replace.txt"].regex == conf.regex
    assert file_map["should_override_replace.txt"].ignore_missing_version == conf.ignore_missing_version

    assert file_map["should_override_parse.txt"].parse == r"version(?P<major>\d+)"
    assert file_map["should_override_parse.txt"].serialize == conf.serialize
    assert file_map["should_override_parse.txt"].search == conf.search
    assert file_map["should_override_parse.txt"].replace == conf.replace
    assert file_map["should_override_parse.txt"].regex == conf.regex
    assert file_map["should_override_parse.txt"].ignore_missing_version == conf.ignore_missing_version

    assert file_map["should_override_serialize.txt"].parse == conf.parse
    assert file_map["should_override_serialize.txt"].serialize == ("{major}",)
    assert file_map["should_override_serialize.txt"].search == conf.search
    assert file_map["should_override_serialize.txt"].replace == conf.replace
    assert file_map["should_override_serialize.txt"].regex == conf.regex
    assert file_map["should_override_serialize.txt"].ignore_missing_version == conf.ignore_missing_version

    assert file_map["should_override_ignore_missing.txt"].parse == conf.parse
    assert file_map["should_override_ignore_missing.txt"].serialize == conf.serialize
    assert file_map["should_override_ignore_missing.txt"].search == conf.search
    assert file_map["should_override_ignore_missing.txt"].replace == conf.replace
    assert file_map["should_override_ignore_missing.txt"].regex == conf.regex
    assert file_map["should_override_ignore_missing.txt"].ignore_missing_version is False

    assert file_map["should_override_regex.txt"].parse == conf.parse
    assert file_map["should_override_regex.txt"].serialize == conf.serialize
    assert file_map["should_override_regex.txt"].search == conf.search
    assert file_map["should_override_regex.txt"].replace == conf.replace
    assert file_map["should_override_regex.txt"].regex is False
    assert file_map["should_override_regex.txt"].ignore_missing_version == conf.ignore_missing_version
