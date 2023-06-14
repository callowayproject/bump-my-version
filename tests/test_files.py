"""File processing tests."""
import os
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent

import pytest
from pytest import param

from bumpversion import exceptions, files
from bumpversion.utils import get_context
from bumpversion.exceptions import VersionNotFoundError
from tests.conftest import get_config_data, inside_dir


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
        result = files.get_glob_files(conf.files[0], version_config)

    assert len(result) == len(file_list)
    for f in result:
        assert Path(f.path) in file_list


def test_single_file_processed_twice(tmp_path: Path):
    """
    Verify that a single file "file2" can be processed twice.

    Use two file_ entries, both with a different suffix after
    the underscore.
    Employ different parse/serialize and search/replace configs
    to verify correct interpretation.
    """
    filepath = tmp_path.joinpath("file2")
    filepath.write_text("dots: 0.10.2\ndashes: 0-10-2")
    overrides = {
        "current_version": "0.10.2",
        "files": [
            {
                "filename": str(filepath),
                "search": "dots: {current_version}",
                "replace": "dots: {new_version}",
            },
            {
                "filename": str(filepath),
                "search": "dashes: {current_version}",
                "replace": "dashes: {new_version}",
                "parse": r"(?P<major>\d+)-(?P<minor>\d+)-(?P<patch>\d+)",
                "serialize": ["{major}-{minor}-{patch}"],
            },
        ],
    }
    conf, version_config, current_version = get_config_data(overrides)
    new_version = current_version.bump("patch", version_config.order)
    ctx = get_context(conf)

    assert len(conf.files) == 2
    for file_cfg in conf.files:
        cfg_file = files.ConfiguredFile(file_cfg, version_config)
        cfg_file.replace_version(current_version, new_version, ctx)

    assert filepath.read_text() == "dots: 0.10.3\ndashes: 0-10-3"


def test_multi_file_configuration(tmp_path: Path):
    full_vers_path = tmp_path / "FULL_VERSION.txt"
    full_vers_path.write_text("1.0.3")
    maj_vers_path = tmp_path / "MAJOR_VERSION.txt"
    maj_vers_path.write_text("1")
    readme_path = tmp_path / "README.txt"
    readme_path.write_text("MyAwesomeSoftware(TM) v1.0")
    build_num_path = tmp_path / "BUILD_NUMBER"
    build_num_path.write_text("1.0.3+joe+38943")

    overrides = {
        "current_version": "1.0.3+joe+38943",
        "parse": r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(?:\+.*)?",
        "serialize": [
            "{major}.{minor}.{patch}+{$USER}+{$BUILD_NUMBER}",
            "{major}.{minor}.{patch}",
        ],
        "files": [
            {
                "filename": str(full_vers_path),
            },
            {
                "filename": str(maj_vers_path),
                "parse": r"\d+",
                "serialize": ["{major}"],
            },
            {
                "filename": str(readme_path),
                "parse": r"(?P<major>\d+)\.(?P<minor>\d+)",
                "serialize": ["{major}.{minor}"],
            },
            {
                "filename": str(build_num_path),
                "serialize": ["{major}.{minor}.{patch}+{$USER}+{$BUILD_NUMBER}"],
            },
        ],
    }
    conf, version_config, current_version = get_config_data(overrides)
    major_version = current_version.bump("major", version_config.order)

    os.environ["BUILD_NUMBER"] = "38944"
    os.environ["USER"] = "bob"
    ctx = get_context(conf)
    del os.environ["BUILD_NUMBER"]
    del os.environ["USER"]

    for file_cfg in conf.files:
        cfg_file = files.ConfiguredFile(file_cfg, version_config)
        cfg_file.replace_version(current_version, major_version, ctx)

    assert full_vers_path.read_text() == "2.0.0"
    assert maj_vers_path.read_text() == "2"
    assert readme_path.read_text() == "MyAwesomeSoftware(TM) v2.0"
    assert build_num_path.read_text() == "2.0.0+bob+38944"

    os.environ["BUILD_NUMBER"] = "38945"
    os.environ["USER"] = "jane"
    conf.current_version = "2.0.0+bob+38944"
    ctx = get_context(conf)
    del os.environ["BUILD_NUMBER"]
    del os.environ["USER"]
    major_version = version_config.parse(conf.current_version)
    major_patch_version = major_version.bump("patch", version_config.order)
    for file_cfg in conf.files:
        cfg_file = files.ConfiguredFile(file_cfg, version_config)
        cfg_file.replace_version(major_version, major_patch_version, ctx)

    assert full_vers_path.read_text() == "2.0.1"
    assert maj_vers_path.read_text() == "2"
    assert readme_path.read_text() == "MyAwesomeSoftware(TM) v2.0"
    assert build_num_path.read_text() == "2.0.1+jane+38945"


def test_raises_correct_missing_version_string(tmp_path: Path):
    full_vers_path = tmp_path / "FULL_VERSION.txt"
    full_vers_path.write_text("3.1.0-rc+build.1031")
    assembly_path = tmp_path / "AssemblyInfo.cs"
    assembly_path.write_text(
        '[assembly: AssemblyFileVersion("3.1.0-rc+build.1031")]\n' '[assembly: AssemblyVersion("3.1.1031.0")]'
    )
    csv_path = tmp_path / "Version.csv"
    csv_path.write_text("1;3-1;0;rc;build.1031")

    overrides = {
        "current_version": "3.1.0-rc+build.1031",
        "parse": r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(-(?P<release>[0-9A-Za-z]+))?(\+build\.(?P<build>.[0-9A-Za-z]+))?",
        "serialize": ["{major}.{minor}.{patch}-{release}+build.{build}", "{major}.{minor}.{patch}+build.{build}"],
        "commit": True,
        "message": "Bump version: {current_version} -> {new_version}",
        "tag": False,
        "tag_name": "{new_version}",
        "tag_message": "Version {new_version}",
        "allow_dirty": True,
        "files": [
            {
                "filename": str(full_vers_path),
            },
            {
                "filename": str(assembly_path),
                "search": '[assembly: AssemblyFileVersion("{current_version}")]',
                "replace": '[assembly: AssemblyFileVersion("{new_version}")]',
            },
            {
                "filename": str(assembly_path),
                "parse": r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<build>\d+)\.(?P<patch>\d+)",
                "serialize": ["{major}.{minor}.{build}.{patch}"],
                "search": '[assembly: AssemblyVersion("{current_version}")]',
                "replace": '[assembly: AssemblyVersion("{new_version}")]',
            },
            {
                "filename": str(csv_path),
                "parse": r"(?P<major>\d+);(?P<minor>\d+);(?P<patch>\d+);(?P<release>[0-9A-Za-z]+)?;(build\.(?P<build>.[0-9A-Za-z]+))?",
                "serialize": [
                    "{major};{minor};{patch};{release};build.{build}",
                    "{major};{minor};{patch};;build.{build}",
                ],
                "search": "1;{current_version}",
                "replace": "1;{new_version}",
            },
        ],
        "parts": {
            "release": {"values": ["beta", "rc", "final"], "optional_value": "final"},
            "build": {
                "first_value": 1000,
                "independent": True,
            },
        },
    }
    conf, version_config, current_version = get_config_data(overrides)
    major_version = current_version.bump("patch", version_config.order)

    ctx = get_context(conf)

    configured_files = [files.ConfiguredFile(file_cfg, version_config) for file_cfg in conf.files]

    with pytest.raises(VersionNotFoundError) as e:
        files.modify_files(configured_files, current_version, major_version, ctx)
        assert e.message.startswith("Did not find '1;3;1;0;rc;build.1031'")


def test_search_replace_to_avoid_updating_unconcerned_lines(tmp_path: Path):
    req_path = tmp_path / "requirements.txt"
    req_path.write_text("Django>=1.5.6,<1.6\nMyProject==1.5.6")

    changelog_path = tmp_path / "CHANGELOG.md"
    changelog_path.write_text(
        dedent(
            """
    # https://keepachangelog.com/en/1.0.0/

    ## [Unreleased]
    ### Added
    - Foobar

    ## [0.0.1] - 2014-05-31
    ### Added
    - This CHANGELOG file to hopefully serve as an evolving example of a
      standardized open source project CHANGELOG.
    """
        )
    )

    overrides = {
        "current_version": "1.5.6",
        "files": [
            {
                "filename": str(req_path),
                "search": "MyProject=={current_version}",
                "replace": "MyProject=={new_version}",
            },
            {
                "filename": str(changelog_path),
                "search": "## [Unreleased]",
                "replace": "## [Unreleased]\n\n## [{new_version}] - {utcnow:%Y-%m-%d}",
            },
        ],
    }

    conf, version_config, current_version = get_config_data(overrides)
    new_version = current_version.bump("minor", version_config.order)

    for file_cfg in conf.files:
        cfg_file = files.ConfiguredFile(file_cfg, version_config)
        cfg_file.replace_version(current_version, new_version, get_context(conf))

    utc_today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    expected_chglog = dedent(
        f"""
    # https://keepachangelog.com/en/1.0.0/

    ## [Unreleased]

    ## [1.6.0] - {utc_today}
    ### Added
    - Foobar

    ## [0.0.1] - 2014-05-31
    ### Added
    - This CHANGELOG file to hopefully serve as an evolving example of a
      standardized open source project CHANGELOG.
    """
    )

    assert req_path.read_text() == "Django>=1.5.6,<1.6\nMyProject==1.6.0"
    assert changelog_path.read_text() == expected_chglog


def test_non_matching_search_does_not_modify_file(tmp_path: Path):
    changelog_path = tmp_path / "CHANGELOG.md"
    changelog_content = dedent(
        """
    # Unreleased

    * bullet point A

    # Release v'older' (2019-09-17)

    * bullet point B
    """
    )
    changelog_path.write_text(changelog_content)

    overrides = {
        "current_version": "1.0.3",
        "files": [
            {
                "filename": str(changelog_path),
                "search": "Not-yet-released",
                "replace": "Release v{new_version} ({now:%Y-%m-%d})",
            }
        ],
    }
    conf, version_config, current_version = get_config_data(overrides)
    new_version = current_version.bump("patch", version_config.order)
    configured_files = files.resolve_file_config(conf.files, version_config)
    with pytest.raises(exceptions.VersionNotFoundError, match="Did not find 'Not-yet-released' in file:"):
        files.modify_files(configured_files, current_version, new_version, get_context(conf))

    assert changelog_path.read_text() == changelog_content


def test_simple_replacement_in_utf8_file(tmp_path: Path):
    """Changing a file in UTF-8 should not change the non-ASCII characters."""
    # Arrange
    version_path = tmp_path / "VERSION"
    version_path.write_bytes("Kröt1.3.0".encode("utf-8"))

    overrides = {"current_version": "1.3.0", "files": [{"filename": str(version_path)}]}
    with inside_dir(tmp_path):
        conf, version_config, current_version = get_config_data(overrides)
        new_version = current_version.bump("patch", version_config.order)

    # Act
    for file_cfg in conf.files:
        cfg_file = files.ConfiguredFile(file_cfg, version_config)
        cfg_file.replace_version(current_version, new_version, get_context(conf))

    # Assert
    out = version_path.read_text()
    assert out == "Kröt1.3.1"


def test_multi_line_search_is_found(tmp_path: Path) -> None:
    """A multiline search string is found and replaced."""
    # Arrange
    alphabet_path = tmp_path / "the_alphabet.txt"
    alphabet_path.write_text("A\nB\nC\n")

    overrides = {
        "current_version": "9.8.7",
        "search": "A\nB\nC",
        "replace": "A\nB\nC\n{new_version}",
        "files": [{"filename": str(alphabet_path)}],
    }
    with inside_dir(tmp_path):
        conf, version_config, current_version = get_config_data(overrides)
        new_version = current_version.bump("major", version_config.order)

    # Act
    for file_cfg in conf.files:
        cfg_file = files.ConfiguredFile(file_cfg, version_config)
        cfg_file.replace_version(current_version, new_version, get_context(conf))

    # Assert
    assert alphabet_path.read_text() == "A\nB\nC\n10.0.0\n"
