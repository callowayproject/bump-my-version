"""Tests for bumpversion.scm.models."""

import pytest
from pytest import param

from bumpversion.scm.models import SCMConfig

simple_pattern = r"(?P<major>\\d+)\\.(?P<minor>\\d+)\.(?P<patch>\\d+)"
complex_pattern = (
    r"(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+)"
    r"(-(?P<release>[0-9A-Za-z]+))?(\\+build\\.(?P<build>.[0-9A-Za-z]+))?"
)


@pytest.mark.parametrize(
    ["tag", "tag_name", "parse_pattern", "expected"],
    [
        param("1.2.3", "{new_version}", simple_pattern, "1.2.3", id="no-prefix, no-suffix"),
        param("v/1.2.3", "v/{new_version}", simple_pattern, "1.2.3", id="prefix, no-suffix"),
        param("v/1.2.3/12345", "v/{new_version}/{something}", simple_pattern, "1.2.3", id="prefix, suffix"),
        param("1.2.3/2024-01-01", "{new_version}/{today}", simple_pattern, "1.2.3", id="no-prefix, suffix"),
        param(
            "app/4.0.3-beta+build.1047",
            "app/{new_version}",
            complex_pattern,
            "4.0.3-beta+build.1047",
            id="complex",
        ),
    ],
)
def test_get_version_from_tag_returns_version_from_pattern(
    scm_config: SCMConfig, tag: str, tag_name: str, parse_pattern: str, expected: str
) -> None:
    """SCMConfig.get_version_from_tag properly returns the version from the tag."""
    # Arrange
    scm_config.parse_pattern = parse_pattern
    scm_config.tag_name = tag_name

    # Act
    version = scm_config.get_version_from_tag(tag)

    # Assert
    assert version == expected
