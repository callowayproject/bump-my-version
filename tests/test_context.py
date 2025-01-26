"""Tests for bumpversion.context."""

import os
from unittest.mock import patch

import pytest
from pytest import param

from bumpversion.context import calver_string_to_regex, prefixed_environ


@pytest.mark.parametrize(
    ["calver_format", "expected_regex"],
    [
        param("{YYYY}.{MM}", r"(?:[1-9][0-9]{3}).(?:1[0-2]|[1-9])", id="year-month"),
        param(
            "{YYYY}.{MM}.{DD}", r"(?:[1-9][0-9]{3}).(?:1[0-2]|[1-9]).(?:3[0-1]|[1-2][0-9]|[1-9])", id="year-month-day"
        ),
        param("{YYYY}.{WW}", r"(?:[1-9][0-9]{3}).(?:5[0-3]|[1-4][0-9]|[0-9])", id="year-week"),
        param("", "", id="empty"),
        param("version-2.0", "version-2.0", id="no-placeholders"),
        param(
            "v{YYYY}-release-{MM}", r"v(?:[1-9][0-9]{3})-release-(?:1[0-2]|[1-9])", id="mixed-text-and-placeholders"
        ),
        param("{invalid}", "{invalid}", id="invalid-placeholder"),
    ],
)
def test_calver_string_to_regex_replacements(calver_format: str, expected_regex: str) -> None:
    """The function should return the expected regex for the given CalVer format string."""
    # Act
    result = calver_string_to_regex(calver_format)
    # Assert
    assert result == expected_regex


class TestPrefixedEnviron:
    """Tests for the prefixed_environ function."""

    def test_prefixed_environ_with_mocked_environment(self):
        """Test that prefixed_environ returns a dictionary with prefixed keys."""
        # Arrange
        mocked_environ = {"KEY1": "value1", "KEY2": "value2"}
        expected_result = {"$KEY1": "value1", "$KEY2": "value2"}

        with patch.dict(os.environ, mocked_environ, clear=True):
            # Act
            result = prefixed_environ()

            # Assert
            assert result == expected_result

    def test_prefixed_environ_with_empty_environment(self):
        """Test that prefixed_environ works with an empty environment."""
        # Arrange
        mocked_environ = {}

        with patch.dict(os.environ, mocked_environ, clear=True):
            # Act
            result = prefixed_environ()

            # Assert
            assert result == {}

    def test_prefixed_environ_with_special_characters_in_keys(self):
        """Test that prefixed_environ handles special characters in keys."""
        # Arrange
        mocked_environ = {"KEY_WITH_$": "value1", "ANOTHER-KEY": "value2"}
        expected_result = {"$KEY_WITH_$": "value1", "$ANOTHER-KEY": "value2"}

        with patch.dict(os.environ, mocked_environ, clear=True):
            # Act
            result = prefixed_environ()

            # Assert
            assert result == expected_result
