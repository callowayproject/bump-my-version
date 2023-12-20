"""Models for managing versioning of software projects."""
from typing import Any, Dict, List, Optional, Union

from bumpversion.config.models import VersionPartConfig
from bumpversion.exceptions import InvalidVersionPartError
from bumpversion.utils import key_val_string
from bumpversion.versioning.functions import NumericFunction, PartFunction, ValuesFunction

# Adapted from https://regex101.com/r/Ly7O1x/3/
SEMVER_PATTERN = r"""
    (?P<major>0|[1-9]\d*)\.
    (?P<minor>0|[1-9]\d*)\.
    (?P<patch>0|[1-9]\d*)
    (?:
        -                             # dash seperator for pre-release section
        (?P<pre_l>[a-zA-Z-]+)         # pre-release label
        (?P<pre_n>0|[1-9]\d*)         # pre-release version number
    )?                                # pre-release section is optional
    (?:
        \+                            # plus seperator for build metadata section
        (?P<buildmetadata>
            [0-9a-zA-Z-]+
            (?:\.[0-9a-zA-Z-]+)*
        )
    )?                                # build metadata section is optional
"""

# Adapted from https://packaging.python.org/en/latest/specifications/version-specifiers/
PEP440_PATTERN = r"""
    v?
    (?:
        (?:(?P<epoch>[0-9]+)!)?                           # Optional epoch
        (?P<release>
            (?P<major>0|[1-9]\d*)\.
            (?P<minor>0|[1-9]\d*)\.
            (?P<patch>0|[1-9]\d*)
        )
        (?P<pre>                                          # pre-release
            [-_\.]?
            (?P<pre_l>(a|b|c|rc|alpha|beta|pre|preview))
            [-_\.]?
            (?P<pre_n>[0-9]+)?
        )?
        (?P<post>                                         # post release
            (?:-(?P<post_n1>[0-9]+))
            |
            (?:
                [-_\.]?
                (?P<post_l>post|rev|r)
                [-_\.]?
                (?P<post_n2>[0-9]+)?
            )
        )?
        (?P<dev>                                          # dev release
            [-_\.]?
            (?P<dev_l>dev)
            [-_\.]?
            (?P<dev_n>[0-9]+)?
        )?
    )
    (?:\+(?P<local>[a-z0-9]+(?:[-_\.][a-z0-9]+)*))?       # local version
"""


class VersionPart:
    """
    Represent part of a version number.

    Determines the PartFunction that rules how the part behaves when increased or reset
    based on the configuration given.
    """

    def __init__(self, config: VersionPartConfig, value: Union[str, int, None] = None):
        self._value = str(value) if value is not None else None
        self.config = config
        self.func: Optional[PartFunction] = None
        if config.values:
            str_values = [str(v) for v in config.values]
            str_optional_value = str(config.optional_value) if config.optional_value is not None else None
            str_first_value = str(config.first_value) if config.first_value is not None else None
            self.func = ValuesFunction(str_values, str_optional_value, str_first_value)
        else:
            self.func = NumericFunction(config.optional_value, config.first_value or "0")

    @property
    def value(self) -> str:
        """Return the value of the part."""
        return self._value or self.func.optional_value

    def copy(self) -> "VersionPart":
        """Return a copy of the part."""
        return VersionPart(self.config, self._value)

    def bump(self) -> "VersionPart":
        """Return a part with bumped value."""
        return VersionPart(self.config, self.func.bump(self.value))

    def null(self) -> "VersionPart":
        """Return a part with first value."""
        return VersionPart(self.config, self.func.first_value)

    @property
    def is_optional(self) -> bool:
        """Is the part optional?"""
        return self.value == self.func.optional_value

    @property
    def is_independent(self) -> bool:
        """Is the part independent of the other parts?"""
        return self.config.independent

    def __format__(self, format_spec: str) -> str:
        try:
            val = int(self.value)
        except ValueError:
            return self.value
        else:
            return int.__format__(val, format_spec)

    def __repr__(self) -> str:
        return f"<bumpversion.VersionPart:{self.func.__class__.__name__}:{self.value}>"

    def __eq__(self, other: Any) -> bool:
        return self.value == other.value if isinstance(other, VersionPart) else False


class Version:
    """The specification of a version and its parts."""

    def __init__(self, values: Dict[str, VersionPart], original: Optional[str] = None):
        self.values = values
        self.original = original

    def __getitem__(self, key: str) -> VersionPart:
        return self.values[key]

    def __len__(self) -> int:
        return len(self.values)

    def __iter__(self):
        return iter(self.values)

    def __repr__(self):
        return f"<bumpversion.Version:{key_val_string(self.values)}>"

    def __eq__(self, other: Any) -> bool:
        return (
            all(value == other.values[key] for key, value in self.values.items())
            if isinstance(other, Version)
            else False
        )

    def bump(self, part_name: str, order: List[str]) -> "Version":
        """Increase the value of the given part."""
        bumped = False

        new_values = {}

        for label in order:
            if label not in self.values:
                continue
            if label == part_name:
                new_values[label] = self.values[label].bump()
                bumped = True
            elif bumped and not self.values[label].is_independent:
                new_values[label] = self.values[label].null()
            else:
                new_values[label] = self.values[label].copy()

        if not bumped:
            raise InvalidVersionPartError(f"No part named {part_name!r}")

        return Version(new_values)
