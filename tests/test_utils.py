"""Tests for the utils module."""

from itertools import combinations

import pytest
from bumpversion import utils


class TestGetNestedValue:
    """Test the get_nested_value function."""

    def test_returns_value(self):
        """It should return the value of the nested key."""
        # Arrange
        d = {"a": {"b": {"c": 1}}}
        path = "a.b.c"
        expected_value = 1

        # Act
        actual_value = utils.get_nested_value(d, path)

        # Assert
        assert actual_value == expected_value

    def test_invalid_path_raises_keyerror(self):
        """It should raise a KeyError if the path is invalid."""
        # Arrange
        d = {"a": {"b": {"c": 1}}}
        path = "a.b.d"

        # Act/Assert
        with pytest.raises(KeyError):
            utils.get_nested_value(d, path)

    def test_non_dict_element_raises_valueerror(self):
        """It should raise a ValueError if an element in the path is not a dict."""
        # Arrange
        d = {"a": {"b": {"c": 1}}}
        path = "a.b.c.d"

        # Act/Assert
        with pytest.raises(ValueError):
            utils.get_nested_value(d, path)


class TestSetNestedValue:
    """Test the set_nested_value function."""

    def test_sets_value(self):
        """It should set the value of the nested key."""
        # Arrange
        d = {"a": {"b": {"c": 1}}}
        path = "a.b.c"
        value = 2
        expected_d = {"a": {"b": {"c": 2}}}

        # Act
        utils.set_nested_value(d, value, path)

        # Assert
        assert d == expected_d

    def test_invalid_path_raises_keyerror(self):
        """It should raise a KeyError if the path is invalid."""
        # Arrange
        d = {"a": {"b": {"c": 1}}}
        path = "a.b.d.e"
        value = 2

        # Act/Assert
        with pytest.raises(KeyError):
            utils.set_nested_value(d, value, path)

    def test_non_dict_element_raises_valueerror(self):
        """It should raise a ValueError if an element in the path is not a dict."""
        # Arrange
        d = {"a": {"b": {"c": 1}}}
        path = "a.b.c.d"
        value = 2

        # Act/Assert
        with pytest.raises(ValueError):
            utils.set_nested_value(d, value, path)


def pytest_generate_tests(metafunc):
    if "flag_permutation" in metafunc.fixturenames:
        flags = [
            "a",
            "i",
            "L",
            "m",
            "s",
            "u",
            "x",
        ]
        permutes = flags[:]
        permutes.extend(["".join(p) for p in combinations(flags, 2)])
        permutes.extend(["".join(p) for p in combinations(flags, 3)])
        permutes.extend(["".join(p) for p in combinations(flags, 4)])
        permutes.extend(["".join(p) for p in combinations(flags, 5)])
        permutes.extend(["".join(p) for p in combinations(flags, 6)])
        permutes.extend(["".join(p) for p in combinations(flags, 7)])
        metafunc.parametrize(
            "flag_permutation",
            permutes,
        )


class TestExtractRegexFlags:
    def test_returns_flags_when_available(self, flag_permutation):
        """It should return the flags when available."""
        # Arrange
        regex = f"(?{flag_permutation})abc"
        expected = ("abc", f"(?{flag_permutation})")

        # Act
        actual_flags = utils.extract_regex_flags(regex)

        # Assert
        assert actual_flags == expected

    def test_returns_empty_string_when_no_flags(self):
        """It should return an empty string when no flags are present."""
        # Arrange
        regex = "abc"
        expected = ("abc", "")

        # Act
        actual_flags = utils.extract_regex_flags(regex)

        # Assert
        assert actual_flags == expected
