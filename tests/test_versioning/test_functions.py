import pytest
from pytest import param

from bumpversion.versioning.functions import NumericFunction, ValuesFunction, IndependentFunction


# NumericFunction
class TestNumericFunction:
    """The numeric function manages incrementing and resetting numeric version parts."""

    class TestCreation:
        """The numeric function can be created."""

        def test_without_first_value_is_zero(self):
            func = NumericFunction()
            assert func.first_value == "0"

        def test_with_first_value_is_value(self):
            func = NumericFunction(first_value="5")
            assert func.first_value == "5"

        def test_non_numeric_first_value_raises_value_error(self):
            with pytest.raises(ValueError):
                NumericFunction(first_value="a")

        def test_alphanumeric_value_is_accepted(self):
            func = NumericFunction(first_value="v10b")
            assert func.first_value == "v10b"

        def test_without_optional_value_is_first_value(self):
            func = NumericFunction()
            assert func.optional_value == func.first_value == "0"
            func = NumericFunction(first_value="5")
            assert func.optional_value == func.first_value == "5"

    class TestBump:
        """Tests for incrementing a value."""

        def test_number_increments(self):
            func = NumericFunction()
            assert func.bump("0") == "1"

        @pytest.mark.parametrize(
            ("value", "expected"),
            [
                param("v10", "v11", id="alphanumeric-prefix"),
                param("10b", "11b", id="alphanumeric-suffix"),
                param("v10b", "v11b", id="alphanumeric-prefix-suffix"),
                param("r3-001", "r4-001", id="alphanumeric-prefix-suffix-with-numeric-suffix"),
            ],
        )
        def test_alphanumeric_increments(self, value: str, expected: str):
            func = NumericFunction()
            assert func.bump(value) == expected

        def test_bump_before_first_value_raises_value_error(self):
            func = NumericFunction()
            with pytest.raises(ValueError):
                func.bump("-1")

            func = NumericFunction(first_value="5")
            with pytest.raises(ValueError):
                func.bump("3")

        def test_bump_non_numeric_value_raises_value_error(self):
            func = NumericFunction()
            with pytest.raises(ValueError):
                func.bump("a")


# ValuesFunction
class TestValuesFunction:
    """The values function manages incrementing and resetting non-numeric version parts."""

    class TestCreation:
        """The values function can be created."""

        def test_values_set_first_value_and_optional_value(self):
            func = ValuesFunction(["0", "1", "2"])
            assert func.optional_value == "0"
            assert func.first_value == "0"

        def test_optional_value_can_be_different_from_first_value(self):
            func = ValuesFunction(["0", "1", "2"], optional_value="1")
            assert func.optional_value == "1"
            assert func.first_value == "0"

            func = ValuesFunction(["0", "1", "2"], optional_value="0", first_value="1")
            assert func.optional_value == "0"
            assert func.first_value == "1"

        def test_optional_value_must_be_in_values(self):
            with pytest.raises(ValueError):
                ValuesFunction(["0", "1", "2"], optional_value="3")

        def test_first_value_doesnt_need_to_be_first_in_values(self):
            func = ValuesFunction(["0", "1", "2"], first_value="1")
            assert func.optional_value == "0"
            assert func.first_value == "1"

        def test_values_are_required(self):
            with pytest.raises(ValueError):
                ValuesFunction([])

        def test_first_value_must_be_in_values(self):
            with pytest.raises(ValueError):
                ValuesFunction(["0", "1", "2"], first_value="3")

    class TestBump:
        def test_bump_returns_next_item(self):
            func = ValuesFunction(["0", "5", "10"])
            assert func.bump("0") == "5"

        def test_cannot_bump_beyond_max_value(self):
            func = ValuesFunction(["0", "5", "10"])
            with pytest.raises(ValueError):
                func.bump("10")

        def test_bump_non_value_raises_value_error(self):
            func = ValuesFunction(["0", "5", "10"])
            with pytest.raises(ValueError):
                func.bump("3")


class TestIndependentFunction:
    """The independent function manages incrementing and resetting version parts."""

    class TestCreation:
        """The independent function can be created."""

        def test_value_sets_first_value_and_optional_value(self):
            func = IndependentFunction("value")
            assert func.optional_value == "value"
            assert func.first_value == "value"

        def test_value_is_not_required(self):
            assert IndependentFunction().optional_value == ""
            assert IndependentFunction("").optional_value == ""

    class TestBump:
        def test_bump_with_value_returns_value(self):
            func = IndependentFunction("1")
            assert func.bump("5") == "5"

        def test_bump_with_no_value_returns_initial_value(self):
            func = IndependentFunction("1")
            assert func.bump() == "1"
