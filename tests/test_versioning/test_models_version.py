"""Tests for the Version class."""

from freezegun import freeze_time

from bumpversion import exceptions
from bumpversion.versioning.models import VersionComponentSpec
from bumpversion.versioning.models import VersionSpec
import pytest
from pytest import param


@pytest.fixture
def semver_version_spec():
    """Return a version spec."""
    config = {
        "major": VersionComponentSpec(),
        "minor": VersionComponentSpec(),
        "patch": VersionComponentSpec(),
        "build": VersionComponentSpec(optional_value="0", independent=True),
        "auto": VersionComponentSpec(optional_value="0", independent=True, always_increment=True),
    }

    return VersionSpec(config)


@pytest.fixture
def calver_version_spec():
    """Return a calver version spec."""
    config = {
        "release": VersionComponentSpec(calver_format="{YYYY}.{MM}.{DD}"),
        "patch": VersionComponentSpec(),
        "build": VersionComponentSpec(optional_value="0", independent=True),
    }

    return VersionSpec(config)


class TestSemVerVersion:
    """Test how a SemVer-style Version model should behave."""

    def test_acts_like_a_dict(self, semver_version_spec: VersionSpec):
        """You can get version components by name."""
        # Arrange
        version = semver_version_spec.create_version({"major": "1", "minor": "2", "patch": "3"})

        # Assert
        assert version["major"].value == "1"
        assert version["minor"].value == "2"
        assert version["patch"].value == "3"
        assert version["build"].value == "0"
        assert version["auto"].value == "0"

        with pytest.raises(KeyError):
            version["invalid"]

    def test_length_is_number_of_parts(self, semver_version_spec: VersionSpec):
        # Arrange
        version = semver_version_spec.create_version({"major": "1"})

        # Assert
        assert len(version) == 5

    def test_is_iterable(self, semver_version_spec: VersionSpec):
        # Arrange
        version = semver_version_spec.create_version({"major": "1"})

        # Assert
        assert list(version) == ["major", "minor", "patch", "build", "auto"]

    def test_has_a_string_representation(self, semver_version_spec: VersionSpec):
        # Arrange
        version = semver_version_spec.create_version({"major": "1", "minor": "2", "patch": "3"})

        # Assert
        assert repr(version) == "<bumpversion.Version:auto=0, build=0, major=1, minor=2, patch=3>"

    def test_has_an_equality_comparison(self, semver_version_spec: VersionSpec):
        # Arrange
        version1 = semver_version_spec.create_version({"major": "1", "minor": "2", "patch": "3"})
        version2 = semver_version_spec.create_version({"major": "1", "minor": "2", "patch": "3"})
        version3 = semver_version_spec.create_version({"major": "1", "minor": "2", "patch": "4"})

        # Assert
        assert version1 == version2
        assert version1 != version3

    class TestBump:
        """Tests of the bump method."""

        def test_does_not_change_original_version(self, semver_version_spec: VersionSpec):
            """Bumping a version does not change the original version."""
            # Arrange
            version1 = semver_version_spec.create_version({"major": "1", "minor": "2", "patch": "3"})

            # Act
            version2 = version1.bump("patch")

            # Assert
            assert version1["patch"].value == "3"
            assert version2["patch"].value == "4"

        def test_returns_a_new_version(self, semver_version_spec: VersionSpec):
            """Bumping a version returns a new version."""
            # Arrange
            version1 = semver_version_spec.create_version({"major": "1", "minor": "2", "patch": "3"})

            # Act
            version2 = version1.bump("patch")

            # Assert
            assert version1 is not version2

        def test_changes_component_and_dependents(self, semver_version_spec: VersionSpec):
            """Bumping a version bumps the specified component and changes its dependents."""
            # Arrange
            version1 = semver_version_spec.create_version(
                {"major": "1", "minor": "2", "patch": "3", "build": "4", "auto": "5"}
            )

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
            assert patch_version_str == "1.2.4.4.6"
            assert minor_version_str == "1.3.0.4.6"
            assert major_version_str == "2.0.0.4.6"
            assert build_version_str == "1.2.3.5.6"

        def test_invalid_component_raises_error(self, semver_version_spec: VersionSpec):
            """If you bump a version with an invalid component name raises an error."""
            version1 = semver_version_spec.create_version(
                {"major": "1", "minor": "2", "patch": "3", "build": "4", "auto": "5"}
            )
            with pytest.raises(exceptions.InvalidVersionPartError, match="No part named 'bugfix'"):
                version1.bump("bugfix")

        def test_independent_component_is_independent(self, semver_version_spec: VersionSpec):
            """An independent component can only get bumped independently."""
            # Arrange
            version1 = semver_version_spec.create_version(
                {"major": "1", "minor": "2", "patch": "3", "build": "4", "auto": "5"}
            )

            # Act & Assert
            build_version_bump = version1.bump("build")
            assert build_version_bump["build"].value == "5"
            assert build_version_bump["major"].value == "1"

            major_version_bump = build_version_bump.bump("major")
            assert major_version_bump["build"].value == "5"
            assert major_version_bump["major"].value == "2"

            build_version_bump2 = major_version_bump.bump("build")
            assert build_version_bump2["build"].value == "6"
            assert build_version_bump2["major"].value == "2"

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
        def test_returns_required_component_names(
            self, semver_version_spec: VersionSpec, values: dict, expected: list
        ):
            """The required_keys function returns all required keys."""
            # Arrange
            version = semver_version_spec.create_version(values)

            # Act
            required_components = version.required_components()

            # Assert
            assert required_components == expected


class TestCalVerVersion:
    """Test how a CalVer-style Version model should behave."""

    @freeze_time("2020-05-01")
    def test_acts_like_a_dict(self, calver_version_spec: VersionSpec):
        """You can get version components by name."""
        # Arrange
        version = calver_version_spec.create_version({"release": "2020.4.1", "patch": "3", "build": "10"})

        # Assert
        assert version["release"].value == "2020.4.1"
        assert version["patch"].value == "3"
        assert version["build"].value == "10"

        with pytest.raises(KeyError):
            version["invalid"]

    def test_length_is_number_of_parts(self, calver_version_spec: VersionSpec):
        # Arrange
        version = calver_version_spec.create_version({"release": "2020.4.1"})

        # Assert
        assert len(version) == 3

    def test_version_is_iterable(self, calver_version_spec: VersionSpec):
        # Arrange
        version = calver_version_spec.create_version({"release": "2020.4.1"})

        # Assert
        assert list(version) == ["release", "patch", "build"]

    def test_has_a_string_representation(self, calver_version_spec: VersionSpec):
        # Arrange
        version = calver_version_spec.create_version({"release": "2020.4.1", "patch": "3"})

        # Assert
        assert repr(version) == "<bumpversion.Version:build=0, patch=3, release=2020.4.1>"

    def test_version_has_an_equality_comparison(self, calver_version_spec: VersionSpec):
        # Arrange
        version1 = calver_version_spec.create_version({"release": "2020.4.1", "patch": "3"})
        version2 = calver_version_spec.create_version({"release": "2020.4.1", "patch": "3"})
        version3 = calver_version_spec.create_version({"release": "2020.5.1"})

        # Assert
        assert version1 == version2
        assert version1 != version3

    class TestBump:
        """Tests of the bump method."""

        @freeze_time("2020-05-01")
        def test_bump_does_not_change_original_version(self, calver_version_spec: VersionSpec):
            """Bumping a version does not change the original version."""
            # Arrange
            version1 = calver_version_spec.create_version({"release": "2020.4.1", "patch": "3", "build": "10"})

            # Act
            version2 = version1.bump("patch")

            # Assert
            assert version1["patch"].value == "3"
            assert version1["release"].value == "2020.4.1"
            assert version2["patch"].value == "0"
            assert version2["release"].value == "2020.5.1"

        @freeze_time("2020-05-01")
        def test_bump_returns_a_new_version(self, calver_version_spec: VersionSpec):
            """Bumping a version returns a new version."""
            # Arrange
            version1 = calver_version_spec.create_version({"release": "2020.4.1", "patch": "3"})

            # Act
            version2 = version1.bump("patch")

            assert version2["release"].value == "2020.5.1"
            assert version2["patch"].value == "0"

            # Assert
            assert version1 is not version2

        @freeze_time("2020-05-01")
        def test_bump_always_increments_calver(self, calver_version_spec: VersionSpec):
            """Bumping a version always increments the calver."""
            # Arrange
            version1 = calver_version_spec.create_version({"release": "2020.4.1", "patch": "3", "build": "10"})

            # Act
            version2 = version1.bump("patch")

            # Assert
            assert version2["release"].value == "2020.5.1"
            assert version2["patch"].value == "0"

        @freeze_time("2020-05-01")
        def test_bump_changes_component_and_dependents(self, calver_version_spec: VersionSpec):
            """Bumping a version bumps the specified component and changes its dependents."""
            # Arrange
            version1 = calver_version_spec.create_version({"release": "2020.5.1", "patch": "3", "build": "4"})

            # Act
            patch_version = version1.bump("patch")
            release_version = version1.bump("release")
            build_version = version1.bump("build")

            # Assert
            patch_version_str = ".".join([item.value for item in patch_version.components.values()])
            release_version_str = ".".join([item.value for item in release_version.components.values()])
            build_version_str = ".".join([item.value for item in build_version.components.values()])
            assert patch_version_str == "2020.5.1.4.4"
            assert release_version_str == "2020.5.1.0.4"
            assert build_version_str == "2020.5.1.3.5"

    class TestRequiredComponents:
        """Tests of the required_keys function."""

        @pytest.mark.parametrize(
            ["values", "expected"],
            [
                param({"release": "2020.4.1", "patch": "3"}, ["release", "patch"], id="release-patch"),
                param({"release": "2020.4.1", "build": "4"}, ["release", "build"], id="release-build"),
                param({"release": "2020.4.1"}, ["release"], id="release"),
            ],
        )
        @freeze_time("2020-05-01")
        def test_returns_required_component_names(
            self, calver_version_spec: VersionSpec, values: dict, expected: list
        ):
            """The required_keys function returns all required keys."""
            # Arrange
            version = calver_version_spec.create_version(values)

            # Act
            required_components = version.required_components()

            # Assert
            assert required_components == expected
