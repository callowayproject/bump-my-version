"""Tests for the Version class."""

from bumpversion.versioning.models import VersionComponentSpec
from bumpversion.versioning.models import VersionSpec
import pytest
from pytest import param


@pytest.fixture
def version_spec():
    """Return a version spec."""
    config = {
        "major": VersionComponentSpec(),
        "minor": VersionComponentSpec(),
        "patch": VersionComponentSpec(),
        "build": VersionComponentSpec(optional_value="0", independent=True),
    }

    return VersionSpec(config)


class TestVersion:
    """Test how the Version model should behave."""

    def test_version_acts_like_a_dict(self, version_spec: VersionSpec):
        """You can get version components by name."""
        # Arrange
        version = version_spec.create_version({"major": "1", "minor": "2", "patch": "3"})

        # Assert
        assert version["major"].value == "1"
        assert version["minor"].value == "2"
        assert version["patch"].value == "3"
        assert version["build"].value == "0"

        with pytest.raises(KeyError):
            version["invalid"]

    def test_version_has_a_length(self, version_spec: VersionSpec):
        # Arrange
        version = version_spec.create_version({"major": "1"})

        # Assert
        assert len(version) == 4

    def test_version_is_iterable(self, version_spec: VersionSpec):
        # Arrange
        version = version_spec.create_version({"major": "1"})

        # Assert
        assert list(version) == ["major", "minor", "patch", "build"]

    def test_version_has_a_string_representation(self, version_spec: VersionSpec):
        # Arrange
        version = version_spec.create_version({"major": "1", "minor": "2", "patch": "3"})

        # Assert
        assert repr(version) == "<bumpversion.Version:build=0, major=1, minor=2, patch=3>"

    def test_version_has_an_equality_comparison(self, version_spec: VersionSpec):
        # Arrange
        version1 = version_spec.create_version({"major": "1", "minor": "2", "patch": "3"})
        version2 = version_spec.create_version({"major": "1", "minor": "2", "patch": "3"})
        version3 = version_spec.create_version({"major": "1", "minor": "2", "patch": "4"})

        # Assert
        assert version1 == version2
        assert version1 != version3

    class TestBump:
        """Tests of the bump method."""

        def test_bump_does_not_change_original_version(self, version_spec: VersionSpec):
            """Bumping a version does not change the original version."""
            # Arrange
            version1 = version_spec.create_version({"major": "1", "minor": "2", "patch": "3"})

            # Act
            version2 = version1.bump("patch")

            # Assert
            assert version1["patch"].value == "3"
            assert version2["patch"].value == "4"

        def test_bump_returns_a_new_version(self, version_spec: VersionSpec):
            """Bumping a version returns a new version."""
            # Arrange
            version1 = version_spec.create_version({"major": "1", "minor": "2", "patch": "3"})

            # Act
            version2 = version1.bump("patch")

            # Assert
            assert version1 is not version2

        def test_bump_changes_component_and_dependents(self, version_spec: VersionSpec):
            """Bumping a version bumps the specified component and changes its dependents."""
            # Arrange
            version1 = version_spec.create_version({"major": "1", "minor": "2", "patch": "3", "build": "4"})

            # Act
            patch_version = version1.bump("patch")
            minor_version = version1.bump("minor")
            major_version = version1.bump("major")
            build_version = version1.bump("build")

            # Assert
            patch_version_str = ".".join([item.value for item in patch_version.components.values()])
            minor_version_str = ".".join([item.value for item in minor_version.components.values()])
            major_version_str = ".".join([item.value for item in major_version.components.values()])
            build_version_str = ".".join([item.value for item in build_version.components.values()])
            assert patch_version_str == "1.2.4.4"
            assert minor_version_str == "1.3.0.4"
            assert major_version_str == "2.0.0.4"
            assert build_version_str == "1.2.3.5"

    class TestRequiredComponents:
        """Tests of the required_keys function."""

        @pytest.mark.parametrize(
            ["values", "expected"],
            [
                param({"major": "1", "minor": "2", "patch": "3"}, ["major", "minor", "patch"], id="major-minor-patch"),
                param(
                    {"major": "0", "minor": "2", "patch": "3", "build": "4"},
                    ["minor", "patch", "build"],
                    id="minor-patch-build",
                ),
                param({"major": "1", "minor": "0", "patch": "3", "build": ""}, ["major", "patch"], id="major-patch"),
                param({"major": "0", "minor": "0", "patch": "3", "build": ""}, ["patch"], id="patch"),
            ],
        )
        def test_returns_required_component_names(self, version_spec: VersionSpec, values: dict, expected: list):
            """The required_keys function returns all required keys."""
            # Arrange
            version = version_spec.create_version(values)

            # Act
            required_components = version.required_components()

            # Assert
            assert required_components == expected
