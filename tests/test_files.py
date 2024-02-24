"""File processing tests."""

import os
import shutil
from datetime import datetime, timezone
from difflib import context_diff
from pathlib import Path
from textwrap import dedent
import tomlkit

import pytest
from pytest import param

from bumpversion import exceptions, files, config, bump
from bumpversion.config.models import FileChange
from bumpversion.utils import get_context
from bumpversion.exceptions import VersionNotFoundError
from bumpversion.version_part import VersionConfig
from tests.conftest import get_config_data, inside_dir


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
    new_version = current_version.bump("patch")
    ctx = get_context(conf)

    assert len(conf.files) == 2
    for file_cfg in conf.files:
        cfg_file = files.ConfiguredFile(file_cfg, version_config)
        cfg_file.make_file_change(current_version, new_version, ctx)

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
    major_version = current_version.bump("major")

    os.environ["BUILD_NUMBER"] = "38944"
    os.environ["USER"] = "bob"
    ctx = get_context(conf)
    del os.environ["BUILD_NUMBER"]
    del os.environ["USER"]

    for file_cfg in conf.files:
        cfg_file = files.ConfiguredFile(file_cfg, version_config)
        cfg_file.make_file_change(current_version, major_version, ctx)

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
    major_patch_version = major_version.bump("patch")
    for file_cfg in conf.files:
        cfg_file = files.ConfiguredFile(file_cfg, version_config)
        cfg_file.make_file_change(major_version, major_patch_version, ctx)

    assert full_vers_path.read_text() == "2.0.1"
    assert maj_vers_path.read_text() == "2"
    assert readme_path.read_text() == "MyAwesomeSoftware(TM) v2.0"
    assert build_num_path.read_text() == "2.0.1+jane+38945"


def test_raises_correct_missing_version_string(tmp_path: Path, fixtures_path: Path):
    """When a file is missing the version string, the error should indicate the correct serialization missing."""
    csharp_path = fixtures_path / "csharp"
    dst_path: Path = shutil.copytree(csharp_path, tmp_path / "csharp")

    with inside_dir(dst_path):
        conf = config.get_configuration(config_file=dst_path.joinpath(".bumpversion.toml"))
        version_config = VersionConfig(conf.parse, conf.serialize, conf.search, conf.replace, conf.parts)
        current_version = version_config.parse(conf.current_version)
        dst_path.joinpath("Version.csv").write_text("1;3-1;0;rc;build.1031")

        major_version = current_version.bump("patch")
        ctx = get_context(conf)

        configured_files = [files.ConfiguredFile(file_cfg, version_config) for file_cfg in conf.files]

        with pytest.raises(VersionNotFoundError) as e:
            files.modify_files(configured_files, current_version, major_version, ctx)
            assert e.message.startswith("Did not find '1;3;1;0;rc;build.1031'")


def test_uses_correct_serialization_for_tag_and_commit_messages(git_repo: Path, fixtures_path: Path, caplog):
    """The tag and commit messages should use the root configured serialization."""
    import subprocess
    import logging

    caplog.set_level(logging.INFO)

    csharp_path = fixtures_path / "csharp"
    dst_path: Path = shutil.copytree(csharp_path, git_repo / "csharp")
    subprocess.check_call(["git", "add", "."], cwd=git_repo)
    subprocess.check_call(["git", "commit", "-m", "Initial commit"], cwd=git_repo)
    subprocess.check_call(["git", "tag", "3.1.0-rc+build.1031"], cwd=git_repo)

    with inside_dir(dst_path):
        config_file = dst_path.joinpath(".bumpversion.toml")
        conf = config.get_configuration(config_file=config_file)
        bump.do_bump("patch", None, conf, config_file, dry_run=True)

    assert "Bump version: 3.1.0-rc+build.1031 -> 3.1.1" in caplog.text


def test_search_replace_to_avoid_updating_unconcerned_lines(tmp_path: Path, caplog):
    import logging

    caplog.set_level(logging.DEBUG)
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
                "no_regex": True,
            },
        ],
    }

    conf, version_config, current_version = get_config_data(overrides)
    new_version = current_version.bump("minor")

    for file_cfg in conf.files:
        cfg_file = files.ConfiguredFile(file_cfg, version_config)
        cfg_file.make_file_change(current_version, new_version, get_context(conf))

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
    new_version = current_version.bump("patch")
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
        new_version = current_version.bump("patch")

    # Act
    for file_cfg in conf.files:
        cfg_file = files.ConfiguredFile(file_cfg, version_config)
        cfg_file.make_file_change(current_version, new_version, get_context(conf))

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
        new_version = current_version.bump("major")

    # Act
    for file_cfg in conf.files:
        cfg_file = files.ConfiguredFile(file_cfg, version_config)
        cfg_file.make_file_change(current_version, new_version, get_context(conf))

    # Assert
    assert alphabet_path.read_text() == "A\nB\nC\n10.0.0\n"


@pytest.mark.parametrize(
    ["global_value", "file_value", "should_raise"],
    [
        param(True, True, False, id="ignore global and file"),
        param(True, False, True, id="ignore global only"),
        param(False, True, False, id="ignore file only"),
        param(False, False, True, id="ignore none"),
    ],
)
def test_ignore_missing_version(global_value: bool, file_value: bool, should_raise: bool, tmp_path: Path) -> None:
    """If the version is not found in the file, do nothing."""
    # Arrange
    version_path = tmp_path / Path("VERSION")
    version_path.write_text("1.2.3")

    overrides = {
        "current_version": "1.2.5",
        "ignore_missing_version": global_value,
        "files": [{"filename": str(version_path), "ignore_missing_version": file_value}],
    }
    with inside_dir(tmp_path):
        conf, version_config, current_version = get_config_data(overrides)
        new_version = current_version.bump("patch")
        cfg_files = [files.ConfiguredFile(file_cfg, version_config) for file_cfg in conf.files]

        # Act
        if should_raise:
            with pytest.raises(VersionNotFoundError):
                files.modify_files(cfg_files, current_version, new_version, get_context(conf))
        else:
            files.modify_files(cfg_files, current_version, new_version, get_context(conf))

    # Assert
    assert version_path.read_text() == "1.2.3"


def test_regex_search(tmp_path: Path) -> None:
    """A regex search string is found and replaced."""
    # Arrange
    version_path = tmp_path / "VERSION"
    version_path.write_text("Release: 1234-56-78 '1.2.3'")

    overrides = {
        "regex": True,
        "current_version": "1.2.3",
        "search": r"Release: \d{{4}}-\d{{2}}-\d{{2}} '{current_version}'",
        "replace": r"Release {now:%Y-%m-%d} '{new_version}'",
        "files": [{"filename": str(version_path)}],
    }
    conf, version_config, current_version = get_config_data(overrides)
    new_version = current_version.bump("patch")
    cfg_files = [files.ConfiguredFile(file_cfg, version_config) for file_cfg in conf.files]

    # Act
    files.modify_files(cfg_files, current_version, new_version, get_context(conf))

    # Assert
    now = datetime.now().isoformat()[:10]
    assert version_path.read_text() == f"Release {now} '1.2.4'"


def test_regex_search_with_escaped_chars(tmp_path: Path) -> None:
    """A search that uses special characters is not treated as a regex."""
    # Arrange
    version_path = tmp_path / "VERSION"
    version_path.write_text("## [Release] 1.2.3 1234-56-78")

    overrides = {
        "regex": True,
        "current_version": "1.2.3",
        "search": r"## \[Release\] {current_version} \d{{4}}-\d{{2}}-\d{{2}}",
        "replace": r"## [Release] {new_version} {now:%Y-%m-%d}",
        "files": [{"filename": str(version_path)}],
    }
    conf, version_config, current_version = get_config_data(overrides)
    new_version = current_version.bump("patch")
    cfg_files = [files.ConfiguredFile(file_cfg, version_config) for file_cfg in conf.files]

    # Act
    files.modify_files(cfg_files, current_version, new_version, get_context(conf))

    # Assert
    now = datetime.now().isoformat()[:10]
    assert version_path.read_text() == f"## [Release] 1.2.4 {now}"


def test_regex_search_in_toml(tmp_path: Path, fixtures_path: Path) -> None:
    """Tests how-to doc 'update-a-date.md'."""
    # Arrange
    version_path = tmp_path / "VERSION"
    version_path.write_text("__date__ = '1234-56-78'\n__version__ = '1.2.3'")
    config_path = tmp_path / ".bumpversion.toml"
    shutil.copyfile(fixtures_path / "replace-date-config.toml", config_path)
    with inside_dir(tmp_path):
        conf = config.get_configuration(config_file=config_path)
        version_config = VersionConfig(conf.parse, conf.serialize, conf.search, conf.replace, conf.parts)
        current_version = version_config.parse(conf.current_version)

        new_version = current_version.bump("patch")
        cfg_files = [files.ConfiguredFile(file_cfg, version_config) for file_cfg in conf.files]

        # Act
        files.modify_files(cfg_files, current_version, new_version, get_context(conf))

    # Assert
    now = datetime.now().isoformat()[:10]
    assert version_path.read_text() == f"__date__ = '{now}'\n__version__ = '1.2.4'"


def test_regex_search_with_caret(tmp_path: Path, fixtures_path: Path) -> None:
    """A search that uses a caret to indicate the beginning of the line works correctly."""
    # Arrange
    config_path = tmp_path / ".bumpversion.toml"
    thingy_path = tmp_path / "thingy.yaml"
    shutil.copyfile(fixtures_path / "regex_with_caret.yaml", thingy_path)
    shutil.copyfile(fixtures_path / "regex_with_caret_config.toml", config_path)

    conf = config.get_configuration(config_file=config_path)
    version_config = VersionConfig(conf.parse, conf.serialize, conf.search, conf.replace, conf.parts)
    current_version = version_config.parse(conf.current_version)
    new_version = current_version.bump("patch")

    with inside_dir(tmp_path):
        cfg_files = [files.ConfiguredFile(file_cfg, version_config) for file_cfg in conf.files]

        # Act
        files.modify_files(cfg_files, current_version, new_version, get_context(conf))

    # Assert
    assert (
        thingy_path.read_text() == "version: 1.0.1\ndependencies:\n- name: kube-prometheus-stack\n  version: 1.0.0\n"
    )


def test_bad_regex_search(tmp_path: Path, caplog) -> None:
    """A search string not meant to be a regex is still found and replaced."""
    # Arrange
    version_path = tmp_path / "VERSION"
    version_path.write_text("Score: A+ ( '1.2.3'")

    overrides = {
        "regex": True,
        "current_version": "1.2.3",
        "search": r"Score: A+ ( '{current_version}'",
        "replace": r"Score: A+ ( '{new_version}'",
        "files": [{"filename": str(version_path)}],
    }
    conf, version_config, current_version = get_config_data(overrides)
    new_version = current_version.bump("patch")
    cfg_files = [files.ConfiguredFile(file_cfg, version_config) for file_cfg in conf.files]

    # Act
    files.modify_files(cfg_files, current_version, new_version, get_context(conf))

    # Assert
    assert version_path.read_text() == "Score: A+ ( '1.2.4'"
    assert "Invalid regex" in caplog.text


class TestDataFileUpdater:
    """Tests for the DataFileUpdater class."""

    def test_update_file_does_not_modify_non_toml_files(self, tmp_path: Path) -> None:
        """A non-TOML file is not modified."""
        # Arrange
        version_path = tmp_path / "VERSION"
        version_path.write_text("1.2.3")

        overrides = {"current_version": "1.2.3", "files": [{"filename": str(version_path)}]}
        conf, version_config, current_version = get_config_data(overrides)
        new_version = current_version.bump("patch")
        datafile_config = FileChange(
            filename=str(version_path),
            key_path="",
            search=conf.search,
            replace=conf.replace,
            regex=conf.regex,
            ignore_missing_version=conf.ignore_missing_version,
            ignore_missing_file=conf.ignore_missing_files,
            serialize=conf.serialize,
            parse=conf.parse,
        )

        # Act
        files.DataFileUpdater(datafile_config, version_config.part_configs).update_file(
            current_version, new_version, get_context(conf)
        )

        # Assert
        assert version_path.read_text() == "1.2.3"

    def test_update_replaces_key(self, tmp_path: Path, fixtures_path: Path) -> None:
        """A key specific key is replaced and nothing else is touched."""
        # Arrange
        config_path = tmp_path / "pyproject.toml"
        fixture_path = fixtures_path / "partial_version_strings.toml"
        shutil.copy(fixture_path, config_path)

        contents_before = config_path.read_text()
        conf = config.get_configuration(config_file=config_path, files=[{"filename": str(config_path)}])
        version_config = VersionConfig(conf.parse, conf.serialize, conf.search, conf.replace, conf.parts)
        current_version = version_config.parse(conf.current_version)
        new_version = current_version.bump("minor")
        datafile_config = FileChange(
            filename=str(config_path),
            key_path="tool.bumpversion.current_version",
            search=conf.search,
            replace=conf.replace,
            regex=conf.regex,
            ignore_missing_version=conf.ignore_missing_version,
            ignore_missing_file=conf.ignore_missing_files,
            serialize=conf.serialize,
            parse=conf.parse,
        )

        # Act
        files.DataFileUpdater(datafile_config, version_config.part_configs).update_file(
            current_version, new_version, get_context(conf)
        )

        # Assert
        contents_after = config_path.read_text()
        toml_data = tomlkit.parse(config_path.read_text()).unwrap()
        actual_difference = list(
            context_diff(
                contents_before.splitlines(),
                contents_after.splitlines(),
                fromfile="before",
                tofile="after",
                n=0,
                lineterm="",
            )
        )
        expected_difference = [
            "*** before",
            "--- after",
            "***************",
            "*** 28 ****",
            '! current_version = "0.0.2"',
            "--- 28 ----",
            '! current_version = "0.1.0"',
        ]
        assert actual_difference == expected_difference
        assert toml_data["tool"]["pdm"]["dev-dependencies"]["lint"] == ["ruff==0.0.292"]
        assert toml_data["tool"]["bumpversion"]["current_version"] == "0.1.0"
