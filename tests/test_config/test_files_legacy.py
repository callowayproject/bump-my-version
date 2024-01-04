import difflib
import json
from pathlib import Path
from textwrap import dedent

import pytest
from _pytest.mark import param

from bumpversion.config.files_legacy import read_ini_file, update_ini_config_file
from bumpversion import config
from ..conftest import inside_dir


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


@pytest.fixture(params=[".bumpversion.cfg", "setup.cfg"])
def cfg_file(request) -> str:
    """Return both config-file styles ('.bumpversion.cfg', 'setup.cfg')."""
    return request.param


@pytest.mark.parametrize(
    ["conf_file", "expected_file"],
    [
        param("basic_cfg.cfg", "basic_cfg_expected.json", id="ini basic cfg"),
        param("legacy_multiline_search.cfg", "legacy_multiline_search_expected.json", id="multiline search cfg"),
    ],
)
def test_read_ini_file(conf_file: str, expected_file: str, fixtures_path: Path) -> None:
    """Parsing the config file should match the expected results."""
    result = read_ini_file(fixtures_path.joinpath(conf_file))
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


CFG_EXPECTED_DIFF = (
    "*** \n"
    "--- \n"
    "***************\n"
    "*** 11 ****\n"
    "! current_version = 1.0.0\n"
    "--- 11 ----\n"
    "! current_version = 1.0.1\n"
)


@pytest.mark.parametrize(
    [
        "cfg_file_name",
    ],
    [
        (".bumpversion.cfg",),
        ("setup.cfg",),
    ],
)
def test_update_ini_config_file(tmp_path: Path, cfg_file_name: str, fixtures_path: Path) -> None:
    """
    Make sure only the version string is updated in the config file.
    """
    expected_diff = CFG_EXPECTED_DIFF
    cfg_path = tmp_path / cfg_file_name
    orig_path = fixtures_path / f"basic_cfg{cfg_path.suffix}"
    cfg_path.write_text(orig_path.read_text())
    original_content = orig_path.read_text().splitlines(keepends=True)

    update_ini_config_file(cfg_path, "1.0.0", "1.0.1")
    new_content = cfg_path.read_text().splitlines(keepends=True)
    difference = difflib.context_diff(original_content, new_content, n=0)
    assert "".join(difference) == expected_diff


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


def test_current_version_is_always_a_string(tmp_path: Path):
    cfg_path = tmp_path / ".bumpversion.cfg"
    initial_config = (
        "[bumpversion]\n"
        "current_version = 2\n"
        "commit = False\n"
        "tag = False\n"
        "parse = (?P<major>\d+)\n"
        "serialize = \n"
        "	{major}\n"
    )
    cfg_path.write_bytes(initial_config.encode("utf-8"))

    with inside_dir(tmp_path):
        cfg = config.get_configuration(cfg_path)

    assert cfg.current_version == "2"
