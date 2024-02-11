"""Tests for the ConfiguredFile class."""

from bumpversion.files import ConfiguredFile, FileChange
from bumpversion.version_part import VersionConfig
from bumpversion.versioning.models import VersionComponentSpec


class TestConfiguredFile:
    """Tests for the ConfiguredFile class."""

    class TestClassCreation:
        """Tests for the creation of the ConfiguredFile class."""

        def test_file_change_is_identical_to_input(self):
            """Test that the file change is identical to the input, but not the same object."""
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
            cfg_file = ConfiguredFile(change, version_config)
            assert cfg_file.file_change == change
            assert cfg_file.file_change is not change

        def test_version_config_uses_file_change_attrs(self):
            """Test that the version config uses the file change attributes, and the original part configs."""
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
            cfg_file = ConfiguredFile(change, version_config)
            assert cfg_file.version_config == expected
