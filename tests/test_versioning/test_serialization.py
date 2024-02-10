"""Tests for the serialization of versioned objects."""

from bumpversion.versioning.serialization import parse_version, serialize
from bumpversion.versioning.conventions import semver_spec, SEMVER_PATTERN
from bumpversion.versioning.models import Version, VersionSpec, VersionComponentSpec
from bumpversion.exceptions import BumpVersionError, FormattingError

import pytest
from pytest import param


class TestParseVersion:
    """Test the parse_version function."""

    def test_empty_version_returns_empty_dict(self):
        assert parse_version("", "") == {}
        assert parse_version(None, "") == {}

    def test_empty_parse_pattern_returns_empty_dict(self):
        assert parse_version("1.2.3", "") == {}
        assert parse_version("1.2.3", None) == {}

    @pytest.mark.parametrize(
        ["version_string", "parse_pattern", "expected"],
        [
            param(
                "1.2.3",
                SEMVER_PATTERN,
                {"buildmetadata": "", "major": "1", "minor": "2", "patch": "3", "pre_l": "", "pre_n": ""},
                id="parse-version",
            ),
            param(
                "1.2.3-alpha1",
                SEMVER_PATTERN,
                {"buildmetadata": "", "major": "1", "minor": "2", "patch": "3", "pre_l": "alpha", "pre_n": "1"},
                id="parse-prerelease",
            ),
            param(
                "1.2.3+build.1",
                SEMVER_PATTERN,
                {"buildmetadata": "build.1", "major": "1", "minor": "2", "patch": "3", "pre_l": "", "pre_n": ""},
                id="parse-buildmetadata",
            ),
            param(
                "1.2.3-alpha1+build.1",
                SEMVER_PATTERN,
                {"buildmetadata": "build.1", "major": "1", "minor": "2", "patch": "3", "pre_l": "alpha", "pre_n": "1"},
                id="parse-prerelease-buildmetadata",
            ),
        ],
    )
    def test_parses_version_and_returns_full_dict(self, version_string: str, parse_pattern: str, expected: dict):
        """The version string should be parsed into a dictionary of the parts and values, including missing parts."""
        results = parse_version(version_string, parse_pattern)
        assert results == expected

    def test_unmatched_pattern_returns_empty_dict(self):
        """If the version string doesn't match the parse pattern, an empty dictionary should be returned."""
        assert parse_version("1.2.3", r"v(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)") == {}

    def test_invalid_parse_pattern_raises_error(self):
        """If the parse pattern is not a valid regular expression, a ValueError should be raised."""
        with pytest.raises(BumpVersionError):
            parse_version("1.2.3", r"v(?P<major>\d+\.(?P<minor>\d+)\.(?P<patch>\d+)")

    def test_parse_pattern_with_newlines(self):
        """A parse pattern with newlines should be parsed correctly."""
        pattern = r"MAJOR=(?P<major>\d+)\nMINOR=(?P<minor>\d+)\nPATCH=(?P<patch>\d+)\n"
        assert parse_version("MAJOR=31\nMINOR=0\nPATCH=3\n", pattern) == {"major": "31", "minor": "0", "patch": "3"}


class TestSerialize:
    """Test the serialize function."""

    class TestFormatSelection:
        @pytest.mark.parametrize(
            ["version", "expected"],
            [
                param(
                    semver_spec().create_version({"major": "1", "minor": "2", "patch": "3"}),
                    "1.2.3",
                    id="major-minor-patch",
                ),
                param(
                    semver_spec().create_version({"major": "1", "minor": "2", "patch": "0"}),
                    "1.2",
                    id="major-minor-patch-zero",
                ),
                param(
                    semver_spec().create_version({"major": "1", "minor": "0", "patch": "0"}),
                    "1",
                    id="major-minor-zero-patch-zero",
                ),
            ],
        )
        def test_is_string_with_fewest_required_labels(self, version: Version, expected: str):
            """The smallest pattern with all the required values should be picked."""
            patterns = ["{major}.{minor}.{patch}", "{major}.{minor}", "{major}"]
            assert serialize(version, serialize_patterns=patterns, context={}) == expected

        def test_is_renderable_pattern_with_fewest_labels(self):
            """The smallest renderable pattern should be picked if no pattern has all the required values."""
            version = semver_spec().create_version(
                {"major": "1", "minor": "2", "patch": "3", "pre_l": "a", "buildmetadata": "build.1"}
            )
            # None of the patterns have all the required values, so the smallest renderable pattern should be picked
            assert (
                serialize(
                    version,
                    serialize_patterns=["{major}.{minor}.{patch}+{buildmetadata}", "{major}.{minor}.{patch}"],
                    context={},
                )
                == "1.2.3"
            )

        def test_is_first_pattern_with_fewest_labels(self):
            """The first pattern with the fewest labels should be picked if multiple have the same number of labels."""
            version = semver_spec().create_version(
                {"major": "1", "minor": "2", "patch": "3", "buildmetadata": "build.1"}
            )
            assert (
                serialize(
                    version,
                    serialize_patterns=["{major}.{minor}.{buildmetadata}", "{major}.{minor}.{patch}"],
                    context={},
                )
                == "1.2.build.1"
            )

        def test_includes_optional_component_when_dependent_is_not_optional(self):
            """A format with an optional component should render when the dependent component is not optional."""
            version_spec = VersionSpec(
                components={
                    "major": VersionComponentSpec(),
                    "minor": VersionComponentSpec(),
                    "patch": VersionComponentSpec(),
                    "release": VersionComponentSpec(
                        optional_value="g",
                        first_value="g",
                        values=[
                            "dev",
                            "a",
                            "b",
                            "g",
                        ],
                    ),
                    "build": VersionComponentSpec(),
                },
            )
            serialize_patterns = [
                "{major}.{minor}.{patch}{release}{build}",
                "{major}.{minor}.{patch}{release}",
                "{major}.{minor}.{patch}",
            ]

            version = version_spec.create_version({"major": "0", "minor": "3", "patch": "1", "build": "1"})
            assert (
                serialize(
                    version,
                    serialize_patterns=serialize_patterns,
                    context={},
                )
                == "0.3.1g1"
            )

        def test_selects_first_pattern_when_all_are_invalid(self):
            """If all patterns are invalid, the first pattern should be selected."""
            version = semver_spec().create_version({"major": "1", "minor": "2", "patch": "3"})
            assert (
                serialize(
                    version,
                    serialize_patterns=["{major}", "{major}.{minor}"],
                    context={},
                )
                == "1"
            )

    class TestRendersFormat:
        def test_with_newlines(self):
            """A serialization format with newlines should be rendered correctly."""
            version = semver_spec().create_version({"major": "31", "minor": "0", "patch": "3"})
            assert (
                serialize(version, serialize_patterns=["MAJOR={major}\nMINOR={minor}\nPATCH={patch}\n"], context={})
                == "MAJOR=31\nMINOR=0\nPATCH=3\n"
            )

        def test_with_additional_context(self):
            """A serialization format with additional context should be rendered correctly."""
            version = semver_spec().create_version({"major": "1", "minor": "2", "patch": "3"})
            assert (
                serialize(
                    version,
                    serialize_patterns=["{major}.{minor}.{patch}+{$BUILDMETADATA}"],
                    context={"$BUILDMETADATA": "build.1"},
                )
                == "1.2.3+build.1"
            )

    class TestRaisesError:
        def test_if_context_is_missing_values(self):
            """An error is raised if not all parts required in the format have values."""
            version = semver_spec().create_version({"major": "1", "minor": "2"})
            with pytest.raises(FormattingError):
                serialize(
                    version,
                    serialize_patterns=["{major}.{minor}.{patch}+{$BUILDMETADATA}"],
                    context={},
                )
