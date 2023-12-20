"""Tests for the serialization of versioned objects."""
from bumpversion.versioning.serialization import parse_version
from bumpversion.versioning.models import SEMVER_PATTERN
from bumpversion.exceptions import BumpVersionError

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
