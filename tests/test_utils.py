"""Tests for the utils module."""
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
