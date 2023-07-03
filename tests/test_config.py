"""Test configuration parsing."""
import difflib
import json
from pathlib import Path
from textwrap import dedent

import pytest
from click.testing import CliRunner, Result
from pytest import param

from bumpversion import config
from tests.conftest import inside_dir


@pytest.fixture(params=[".bumpversion.cfg", "setup.cfg"])
def cfg_file(request) -> str:
    """Return both config-file styles ('.bumpversion.cfg', 'setup.cfg')."""
    return request.param


@pytest.fixture(
    params=[
        "file",
        "file(suffix)",
        "file (suffix with space)",
        "file (suffix lacking closing paren",
    ]
)
def cfg_file_keyword(request):
    """Return multiple possible styles for the bumpversion:file keyword."""
    return request.param


@pytest.mark.parametrize(
    ["conf_file", "expected_file"],
    [
        param("basic_cfg.cfg", "basic_cfg_expected.json", id="ini basic cfg"),
    ],
)
def test_read_ini_file(conf_file: str, expected_file: str, fixtures_path: Path) -> None:
    """Parsing the config file should match the expected results."""
    result = config.read_ini_file(fixtures_path.joinpath(conf_file))
    expected = json.loads(fixtures_path.joinpath(expected_file).read_text())
    assert result == expected


@pytest.mark.parametrize(
    ["conf_file", "expected_file"],
    [
        param("basic_cfg.toml", "basic_cfg_expected.json", id="toml basic cfg"),
    ],
)
def test_read_toml_file(conf_file: str, expected_file: str, fixtures_path: Path) -> None:
    """Parsing the config file should match the expected results."""
    result = config.read_toml_file(fixtures_path.joinpath(conf_file))
    expected = json.loads(fixtures_path.joinpath(expected_file).read_text())
    assert result == expected


def test_independent_falsy_value_in_config_does_not_bump_independently(tmp_path: Path):
    # tmp_path.joinpath("VERSION").write_text("2.1.0-5123")
    config_file = tmp_path.joinpath(".bumpversion.cfg")
    config_file.write_text(
        dedent(
            r"""
        [bumpversion]
        current_version: 2.1.0-5123
        parse = (?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)\-(?P<build>\d+)
        serialize = {major}.{minor}.{patch}-{build}

        [bumpversion:file:VERSION]

        [bumpversion:part:build]
        independent = 0
        """
        )
    )

    conf = config.get_configuration(config_file)
    assert conf.parts["build"].independent is False


def test_correct_interpolation_for_setup_cfg_files(tmp_path: Path, fixtures_path: Path):
    """
    Reported here: https://github.com/c4urself/bump2version/issues/21.
    """
    test_fixtures_path = fixtures_path.joinpath("interpolation")
    setup_cfg = config.get_configuration(test_fixtures_path.joinpath("setup.cfg"))
    bumpversion_cfg = config.get_configuration(test_fixtures_path.joinpath(".bumpversion.cfg"))
    pyproject_toml = config.get_configuration(test_fixtures_path.joinpath("pyproject.toml"))

    assert setup_cfg.replace == "{now:%m-%d-%Y} v. {new_version}"
    assert bumpversion_cfg.replace == "{now:%m-%d-%Y} v. {new_version}"
    assert pyproject_toml.replace == "{now:%m-%d-%Y} v. {new_version}"


def test_file_keyword_with_suffix_is_accepted(tmp_path: Path, cfg_file: str, cfg_file_keyword: str):
    cfg_file_path = tmp_path / cfg_file
    cfg_file_path.write_text(
        "[bumpversion]\n"
        "current_version = 0.10.2\n"
        "new_version = 0.10.3\n"
        "[bumpversion:file (foobar):file2]\n"
        "search = version {current_version}\n"
        "replace = version {new_version}\n"
        f"[bumpversion:{cfg_file_keyword}:file2]\n"
        "search = The current version is {current_version}\n"
        "replace = The current version is {new_version}\n"
    )
    setup_cfg = config.get_configuration(cfg_file_path)
    assert len(setup_cfg.files) == 2
    assert all(f.filename == "file2" for f in setup_cfg.files)


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
        cfg_file = config.find_config_file()
        cfg = config.get_configuration(cfg_file)

    assert cfg.current_version == "0.10.5"
    assert cfg.parse == "(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+)(\\-(?P<release>[a-z]+))?"
    assert cfg.serialize == ["{major}.{minor}.{patch}-{release}", "{major}.{minor}.{patch}"]


def test_utf8_message_from_config_file(tmp_path: Path, cfg_file):
    cfg_path = tmp_path / cfg_file
    initial_config = (
        "[bumpversion]\n"
        "current_version = 500.0.0\n"
        "commit = True\n"
        "message = Nová verze: {current_version} ☃, {new_version} ☀\n"
    )
    cfg_path.write_bytes(initial_config.encode("utf-8"))

    with inside_dir(tmp_path):
        cfg = config.get_configuration(cfg_path)

    assert cfg.message == "Nová verze: {current_version} ☃, {new_version} ☀"


CFG_EXPECTED_DIFF = (
    "*** \n"
    "--- \n"
    "***************\n"
    "*** 11 ****\n"
    "! current_version = 1.0.0\n"
    "--- 11 ----\n"
    "! current_version = 1.0.1\n"
)

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
    ["cfg_file_name", "expected_diff"],
    [
        (".bumpversion.cfg", CFG_EXPECTED_DIFF),
        ("setup.cfg", CFG_EXPECTED_DIFF),
        ("pyproject.toml", TOML_EXPECTED_DIFF),
    ],
)
def test_update_config_file(tmp_path: Path, cfg_file_name: str, expected_diff: str, fixtures_path: Path) -> None:
    """
    Make sure only the version string is updated in the config file.
    """
    cfg_path = tmp_path / cfg_file_name
    orig_path = fixtures_path / f"basic_cfg{cfg_path.suffix}"
    cfg_path.write_text(orig_path.read_text())
    original_content = orig_path.read_text().splitlines(keepends=True)

    config.update_config_file(cfg_path, "1.0.0", "1.0.1")
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

        # try:
        #     subprocess.run(["git", "add", "README.md"], check=True, capture_output=True)
        #     subprocess.run(["git", "commit", "-am", "my branch commit"], check=True, capture_output=True)
        # except subprocess.CalledProcessError as e:
        #     print(e.stdout)
        #     print(e.stderr)
        #     raise
        # result: Result = runner.invoke(cli.cli, ["bump", "dev_label", "--no-tag"])
        # assert result.exit_code == 0
        # cfg = config.get_configuration(cfg_path)
        # assert cfg.current_version == "1.0.0.dev1+myreallylongbranchna"
