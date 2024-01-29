"""Tests of the VersionSpec model."""

import pytest
from bumpversion.versioning.models import VersionSpec
from bumpversion.versioning.models import VersionComponentSpec


class TestVersionSpec:
    """Tests for the version spec."""

    class TestCreation:
        """Tests for creating a version spec."""

        def test_empty_components_raises_error(self):
            """An empty components dict raises an error."""
            with pytest.raises(ValueError):
                VersionSpec({}, [])

        class TestComponentOrder:
            def test_empty_order_uses_order_of_components(self):
                """If the order is empty, it uses the component order."""
                # Arrange
                config = {
                    "major": VersionComponentSpec(),
                    "minor": VersionComponentSpec(),
                    "patch": VersionComponentSpec(),
                }

                # Act
                version_spec = VersionSpec(config, [])

                # Assert
                assert version_spec.order == ["major", "minor", "patch"]

            def test_extra_items_raises_error(self):
                """If the order contains component names that do not exist, it raises and error."""
                # Arrange
                config = {
                    "major": VersionComponentSpec(),
                    "minor": VersionComponentSpec(),
                    "patch": VersionComponentSpec(),
                }

                # Act
                with pytest.raises(ValueError):
                    VersionSpec(config, ["major", "minor", "patch", "build"])

            def test_subset_of_items_works_fine(self):
                """An order containing a subset of component names works fine."""
                # Arrange
                config = {
                    "major": VersionComponentSpec(),
                    "minor": VersionComponentSpec(),
                    "patch": VersionComponentSpec(),
                }

                # Act
                version_spec = VersionSpec(config, ["major", "patch"])

                # Assert
                assert dict(version_spec.dependency_map) == {"major": ["patch"]}

        def test_dependency_map_follows_order(self):
            """The order of components correctly creates the dependency map."""
            # Arrange
            config = {
                "major": VersionComponentSpec(),
                "minor": VersionComponentSpec(),
                "patch": VersionComponentSpec(),
            }

            # Act
            version_spec = VersionSpec(config, ["major", "minor", "patch"])
            version_spec2 = VersionSpec(config, ["patch", "minor", "major"])

            # Assert
            assert dict(version_spec.dependency_map) == {"major": ["minor"], "minor": ["patch"]}
            assert dict(version_spec2.dependency_map) == {"patch": ["minor"], "minor": ["major"]}

        def test_dependency_map_skips_independent_components(self):
            """Independent components are not in the dependency map."""
            # Arrange
            config = {
                "major": VersionComponentSpec(),
                "minor": VersionComponentSpec(independent=True),
                "patch": VersionComponentSpec(),
            }

            # Act
            version_spec = VersionSpec(config, ["major", "minor", "patch"])

            # Assert
            assert dict(version_spec.dependency_map) == {"major": ["patch"]}

    class TestGenerateVersion:
        """Tests of the generate_version method."""

        def test_empty_values_creates_default_version(self):
            """An empty values dict raises an error."""
            # Arrange
            config = {
                "major": VersionComponentSpec(),
                "minor": VersionComponentSpec(),
                "patch": VersionComponentSpec(),
                "build": VersionComponentSpec(independent=True),
            }
            version_spec = VersionSpec(config)

            # Act
            version = version_spec.create_version({})

            # Assert
            assert version["major"].value == "0"
            assert version["minor"].value == "0"
            assert version["patch"].value == "0"
            assert version["build"].value == "0"

        def test_missing_values_uses_component_first_value(self):
            """A missing value raises an error."""
            # Arrange
            config = {
                "major": VersionComponentSpec(),
                "minor": VersionComponentSpec(),
                "patch": VersionComponentSpec(),
                "build": VersionComponentSpec(independent=True),
            }
            version_spec = VersionSpec(config)

            # Act
            version = version_spec.create_version({"major": "1", "minor": "2"})

            # Assert
            assert version["major"].value == "1"
            assert version["minor"].value == "2"
            assert version["patch"].value == "0"
            assert version["build"].value == "0"

        def test_extra_values_ignored(self):
            """Extra values are ignored."""
            # Arrange
            config = {
                "major": VersionComponentSpec(),
                "minor": VersionComponentSpec(),
                "patch": VersionComponentSpec(),
            }
            version_spec = VersionSpec(config)

            # Act
            version = version_spec.create_version({"major": "1", "minor": "2", "patch": "3", "build": "4"})

            # Assert
            assert version["major"].value == "1"
            assert version["minor"].value == "2"
            assert version["patch"].value == "3"
            assert "build" not in version

    class TestGetDependents:
        """Tests of the get_dependents method."""

        def test_bad_component_name_returns_empty_list(self):
            """Getting the dependents of a non-existing component returns an empty list."""
            # Arrange
            config = {
                "major": VersionComponentSpec(),
                "minor": VersionComponentSpec(),
                "patch": VersionComponentSpec(),
            }
            version_spec = VersionSpec(config)

            # Act
            dependents = version_spec.get_dependents("invalid")

            # Assert
            assert dependents == []

        def test_extra_values_ignored(self):
            """Extra values are ignored."""
            # Arrange
            config = {
                "major": VersionComponentSpec(),
                "minor": VersionComponentSpec(),
                "patch": VersionComponentSpec(),
            }
            version_spec = VersionSpec(config)

            # Act
            patch_dependents = version_spec.get_dependents("patch")
            minor_dependents = version_spec.get_dependents("minor")
            major_dependents = version_spec.get_dependents("major")

            # Assert
            assert patch_dependents == []
            assert minor_dependents == ["patch"]
            assert major_dependents == ["minor", "patch"]
