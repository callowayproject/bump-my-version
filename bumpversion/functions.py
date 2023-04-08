"""Generators for version parts."""
import re
from typing import List, Optional, Union


class PartFunction:
    """Base class for a version part function."""

    first_value: str
    optional_value: str
    independent: bool

    def bump(self, value: str) -> str:
        """Increase the value."""
        raise NotImplementedError


class NumericFunction(PartFunction):
    """
    This is a class that provides a numeric function for version parts.

    It simply starts with the provided first_value (0 by default) and
    increases it following the sequence of integer numbers.

    The optional value of this function is equal to the first value.

    This function also supports alphanumeric parts, altering just the numeric
    part (e.g. 'r3' --> 'r4'). Only the first numeric group found in the part is
    considered (e.g. 'r3-001' --> 'r4-001').
    """

    FIRST_NUMERIC = re.compile(r"(\D*)(\d+)(.*)")

    def __init__(self, optional_value: Optional[str] = None, first_value: Optional[str] = None):
        if first_value is not None and not self.FIRST_NUMERIC.search(str(first_value)):
            raise ValueError(f"The given first value {first_value} does not contain any digit")

        self.first_value = str(first_value or 0)
        self.optional_value = optional_value or self.first_value

    def bump(self, value: Union[str, int]) -> str:
        """Increase the first numerical value by one."""
        match = self.FIRST_NUMERIC.search(str(value))
        if not match:
            raise ValueError(f"The given value {value} does not contain any digit")
        part_prefix, part_numeric, part_suffix = match.groups()
        bumped_numeric = int(part_numeric) + 1

        return "".join([part_prefix, str(bumped_numeric), part_suffix])


class ValuesFunction(PartFunction):
    """
    This is a class that provides a values list based function for version parts.

    It is initialized with a list of values and iterates through them when
    bumping the part.

    The default optional value of this function is equal to the first value,
    but may be otherwise specified.

    When trying to bump a part which has already the maximum value in the list
    you get a ValueError exception.
    """

    def __init__(
        self,
        values: List[str],
        optional_value: Optional[str] = None,
        first_value: Optional[str] = None,
    ):
        if not values:
            raise ValueError("Version part values cannot be empty")

        self._values = values

        if optional_value is None:
            optional_value = values[0]

        if optional_value not in values:
            raise ValueError(f"Optional value {optional_value} must be included in values {values}")

        self.optional_value = optional_value

        if not first_value:
            first_value = values[0]

        if first_value not in values:
            raise ValueError(f"First value {first_value} must be included in values {values}")

        self.first_value = first_value

    def bump(self, value: str) -> str:
        """Return the item after ``value`` in the list."""
        try:
            return self._values[self._values.index(value) + 1]
        except IndexError as e:
            raise ValueError(
                f"The part has already the maximum value among {self._values} and cannot be bumped."
            ) from e
