"""Tests for the ConfiguredFile class."""

import logging
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent

import pytest

from bumpversion import files
from bumpversion.context import get_context
from bumpversion.files import ConfiguredFile, FileChange
from bumpversion.ui import get_indented_logger, setup_logging
from bumpversion.versioning.models import VersionComponentSpec
from bumpversion.versioning.version_config import VersionConfig
from tests.conftest import get_config_data, inside_dir


def setup_configured_file(filepath):
    """Sets up a configured file for testing."""
    overrides = {
        "current_version": "1.2.3",
        "files": [{"filename": str(filepath)}],
    }
    conf, version_config, _current_version = get_config_data(overrides)
    assert len(conf.files_to_modify) == 1
    assert conf.files_to_modify[0].filename == str(filepath)
    return ConfiguredFile(conf.files_to_modify[0], version_config)


class TestConfiguredFile:
    """Tests for the ConfiguredFile class."""

    class TestClassCreation:
        """Tests for the creation of the ConfiguredFile class."""

        def test_file_change_is_identical_to_input(self):
            """Test that the file change is identical to the input but a different object."""
            # Arrange
            change = FileChange(
                filename="boobar.txt",
                search="dashes: {current_version}",
                replace="dashes: {new_version}",
                parse=r"(?P<major>\d+)-(?P<minor>\d+)-(?P<patch>\d+)",
                serialize=("{major}-{minor}-{patch}",),
                regex=True,
                ignore_missing_version=False,
                ignore_missing_file=False,
            )
            version_config = VersionConfig(
                parse="(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+)(\\-(?P<release>[a-z]+))?",
                serialize=("{major}.{minor}.{patch}",),
                search="{current_version}",
                replace="{new_version}",
                part_configs={
                    "major": VersionComponentSpec(),
                    "minor": VersionComponentSpec(),
                    "patch": VersionComponentSpec(),
                },
            )

            # Act
            cfg_file = ConfiguredFile(change, version_config)

            # Assert
            assert cfg_file.file_change == change
            assert cfg_file.file_change is not change

        def test_version_config_uses_file_change_attrs(self):
            """Test that the version config uses the file change attributes and the original part configs."""
            # Arrange
            change = FileChange(
                filename="boobar.txt",
                search="dashes: {current_version}",
                replace="dashes: {new_version}",
                parse=r"(?P<major>\d+)-(?P<minor>\d+)-(?P<patch>\d+)",
                serialize=("{major}-{minor}-{patch}",),
                regex=True,
                ignore_missing_version=False,
                ignore_missing_file=False,
            )
            version_config = VersionConfig(
                parse="(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+)(\\-(?P<release>[a-z]+))?",
                serialize=("{major}.{minor}.{patch}",),
                search="{current_version}",
                replace="{new_version}",
                part_configs={
                    "major": VersionComponentSpec(),
                    "minor": VersionComponentSpec(),
                    "patch": VersionComponentSpec(),
                },
            )
            expected = VersionConfig(
                parse=change.parse,
                search=change.search,
                replace=change.replace,
                serialize=change.serialize,
                part_configs=version_config.part_configs,
            )

            # Act
            cfg_file = ConfiguredFile(change, version_config)

            # Assert
            assert cfg_file.version_config == expected

    class TestGetFileContents:
        """Tests of the get_file_content method."""

        def test_returns_contents_of_existing_file(self, tmp_path: Path) -> None:
            """The get_file_content method returns the contents of an existing file."""
            # Arrange
            filepath = tmp_path / "file.md"
            expected_data = "My current version is 1.2.3"
            filepath.write_text(expected_data, encoding="utf-8")
            configured_file = setup_configured_file(filepath)

            # Assert
            assert configured_file.get_file_contents() == expected_data

        def test_raises_exception_if_file_not_found(self, tmp_path: Path) -> None:
            """The get_file_content method raises an exception if the file does not exist."""
            filepath = tmp_path / "file.md"
            configured_file = setup_configured_file(filepath)
            # Act
            with pytest.raises(FileNotFoundError):
                configured_file.get_file_contents()

    class TestMakeFileChange:
        """Tests of the make_file_change function."""

        def test_raises_exception_if_file_not_found(self, tmp_path: Path) -> None:
            """The make_file_change method raises an exception if the file does not exist."""
            # Arrange
            filepath = tmp_path / "file.md"
            overrides = {
                "current_version": "1.2.3",
                "files": [{"filename": str(filepath)}],
            }
            with inside_dir(tmp_path):
                conf, version_config, current_version = get_config_data(overrides)
            configured_file = ConfiguredFile(conf.files_to_modify[0], version_config)
            new_version = current_version.bump("patch")
            ctx = get_context(conf)

            # Act
            with pytest.raises(FileNotFoundError):
                configured_file.make_file_change(current_version, new_version, ctx, dry_run=True)

        def test_logs_missing_file_when_ignore_missing_file_set(self, tmp_path: Path, caplog) -> None:
            """The make_file_change method logs missing file when ignore_missing_file set to True."""
            self._setup_logging(caplog)
            filepath = tmp_path / "file.md"
            overrides = {
                "current_version": "1.2.3",
                "files": [{"filename": str(filepath), "ignore_missing_file": True}],
            }
            with inside_dir(tmp_path):
                conf, version_config, current_version = get_config_data(overrides)
                configured_file = ConfiguredFile(conf.files_to_modify[0], version_config)
                new_version = current_version.bump("patch")
                ctx = get_context(conf)

                # Act
                configured_file.make_file_change(current_version, new_version, ctx, dry_run=True)

            # Assert
            logs = caplog.messages
            assert logs[0] == "Reading configuration"
            assert logs[1] == "  Configuration file not found: missing."
            assert logs[2] == f"\nFile {filepath}: replace `{{current_version}}` with `{{new_version}}`"
            assert logs[3] == "  File not found, but ignoring"

        def test_dedents_properly_when_file_does_not_contain_pattern(
            self, fixtures_path: Path, tmp_path, caplog
        ) -> None:
            """The make_file_change method dedents the logging context when it does not contain a pattern."""
            self._setup_logging(caplog)
            overrides = {
                "current_version": "1.2.3",
                "files": [{"glob": "glob/**/*.txt", "ignore_missing_file": True, "ignore_missing_version": True}],
            }
            shutil.copytree(fixtures_path / "glob", tmp_path / "glob")

            with inside_dir(tmp_path):
                conf, version_config, current_version = get_config_data(overrides)
                configured_file1 = ConfiguredFile(conf.files_to_modify[0], version_config)
                configured_file2 = ConfiguredFile(conf.files_to_modify[1], version_config)
                configured_file3 = ConfiguredFile(conf.files_to_modify[2], version_config)
            new_version = current_version.bump("patch")
            ctx = get_context(conf)

            # Act
            configured_file1.make_file_change(current_version, new_version, ctx, dry_run=True)
            configured_file2.make_file_change(current_version, new_version, ctx, dry_run=True)
            configured_file3.make_file_change(current_version, new_version, ctx, dry_run=True)

            # Assert
            logs = caplog.messages
            assert logs[0] == "Reading configuration"
            assert logs[1] == "  Configuration file not found: missing."
            assert logs[2] == (
                f"\nFile {configured_file1.file_change.filename}: replace `{{current_version}}` with `{{new_version}}`"
            )
            assert logs[3] == "  File not found, but ignoring"
            assert logs[4] == (
                f"\nFile {configured_file2.file_change.filename}: replace `{{current_version}}` with `{{new_version}}`"
            )
            assert logs[5] == "  File not found, but ignoring"
            assert logs[6] == (
                f"\nFile {configured_file3.file_change.filename}: replace `{{current_version}}` with `{{new_version}}`"
            )
            assert logs[7] == "  File not found, but ignoring"

        def _setup_logging(self, caplog):
            setup_logging(1)
            caplog.set_level(logging.INFO)
            logger = get_indented_logger(__name__)
            logger.reset()

    def test_can_process_single_file_twice(self, tmp_path: Path):
        """
        Verify that a single file "file2" can be processed twice.

        Use two file_ entries, both with a different suffix after the underscore.
        Employ different parse/serialize and search/replace configs to verify correct interpretation.
        """
        # Arrange
        filepath = tmp_path.joinpath("file2")
        filepath.write_text("dots: 0.10.2\ndashes: 0-10-2", encoding="utf-8")
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

        # Act
        for file_cfg in conf.files:
            cfg_file = files.ConfiguredFile(file_cfg, version_config)
            cfg_file.make_file_change(current_version, new_version, ctx)

        # Assert
        assert len(conf.files) == 2
        assert filepath.read_text() == "dots: 0.10.3\ndashes: 0-10-3"

    def test_can_multi_file_configuration(self, tmp_path: Path):
        full_vers_path = tmp_path / "FULL_VERSION.txt"
        full_vers_path.write_text("1.0.3", encoding="utf-8")
        maj_vers_path = tmp_path / "MAJOR_VERSION.txt"
        maj_vers_path.write_text("1", encoding="utf-8")
        readme_path = tmp_path / "README.txt"
        readme_path.write_text("MyAwesomeSoftware(TM) v1.0", encoding="utf-8")
        build_num_path = tmp_path / "BUILD_NUMBER"
        build_num_path.write_text("1.0.3+joe+38943", encoding="utf-8")

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


def test_make_file_change_search_replace_to_avoid_updating_unconcerned_lines(tmp_path: Path, caplog):
    import logging

    caplog.set_level(logging.DEBUG)
    req_path = tmp_path / "requirements.txt"
    req_path.write_text("Django>=1.5.6,<1.6\nMyProject==1.5.6", encoding="utf-8")

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
        ),
        encoding="utf-8",
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


def test_make_file_change_simple_replacement_in_utf8_file(tmp_path: Path):
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


def test_make_file_change_multi_line_search_is_found(tmp_path: Path) -> None:
    """A multiline search string is found and replaced."""
    # Arrange
    alphabet_path = tmp_path / "the_alphabet.txt"
    alphabet_path.write_text("A\nB\nC\n", encoding="utf-8")

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
