"""Module for managing Versions and their internal parts."""
import logging
import re
import string
from copy import copy
from typing import Any, Dict, List, MutableMapping, Optional

from click import UsageError

from bumpversion.config import VersionPartConfig
from bumpversion.exceptions import FormattingError, InvalidVersionPartError, MissingValueError
from bumpversion.functions import NumericFunction, PartFunction, ValuesFunction
from bumpversion.utils import key_val_string, labels_for_format

logger = logging.getLogger(__name__)


class VersionPart:
    """
    Represent part of a version number.

    Determines the PartFunction that rules how the part behaves when increased or reset
    based on the configuration given.
    """

    def __init__(self, config: VersionPartConfig, value: Optional[str] = None):
        self._value = value
        self.config = config
        self.func: Optional[PartFunction] = None
        if config.values:
            self.func = ValuesFunction(config.values, config.optional_value, config.first_value)
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


class VersionConfig:
    """
    Hold a complete representation of a version string.
    """

    def __init__(
        self,
        parse: str,
        serialize: List[str],
        search: str,
        replace: str,
        part_configs: Optional[Dict[str, VersionPartConfig]] = None,
    ):
        try:
            self.parse_regex = re.compile(parse, re.VERBOSE)
        except re.error as e:
            raise UsageError(f"--parse '{parse}' is not a valid regex.") from e

        self.serialize_formats = serialize
        self.part_configs = part_configs or {}
        self.search = search
        self.replace = replace

    @property
    def order(self) -> List[str]:
        """
        Return the order of the labels in a serialization format.

        Currently, order depends on the first given serialization format.
        This seems like a good idea because this should be the most complete format.

        Returns:
            A list of version part labels in the order they should be rendered.
        """
        return labels_for_format(self.serialize_formats[0])

    def parse(self, version_string: Optional[str] = None) -> Optional[Version]:
        """
        Parse a version string into a Version object.

        Args:
            version_string: Version string to parse

        Returns:
            A Version object representing the string.
        """
        if not version_string:
            return None

        regexp_one_line = "".join([line.split("#")[0].strip() for line in self.parse_regex.pattern.splitlines()])

        logger.info(
            "Parsing version '%s' using regexp '%s'",
            version_string,
            regexp_one_line,
        )

        match = self.parse_regex.search(version_string)

        if not match:
            logger.warning(
                "Evaluating 'parse' option: '%s' does not parse current version '%s'",
                self.parse_regex.pattern,
                version_string,
            )
            return None

        _parsed = {
            key: VersionPart(self.part_configs[key], value)
            for key, value in match.groupdict().items()
            if key in self.part_configs
        }
        v = Version(_parsed, version_string)

        logger.info("Parsed the following values: %s", key_val_string(v.values))

        return v

    def _serialize(
        self, version: Version, serialize_format: str, context: MutableMapping, raise_if_incomplete: bool = False
    ) -> str:
        """
        Attempts to serialize a version with the given serialization format.

        Args:
            version: The version to serialize
            serialize_format: The serialization format to use, using Python's format string syntax
            context: The context to use when serializing the version
            raise_if_incomplete: Whether to raise an error if the version is incomplete

        Raises:
            FormattingError: if not serializable
            MissingValueError: if not all parts required in the format have values

        Returns:
            The serialized version as a string
        """
        values = copy(context)
        for k in version:
            values[k] = version[k]

        # TODO dump complete context on debug level

        try:
            # test whether all parts required in the format have values
            serialized = serialize_format.format(**values)

        except KeyError as e:
            missing_key = getattr(e, "message", e.args[0])
            raise MissingValueError(
                f"Did not find key {missing_key!r} in {version!r} when serializing version number"
            ) from e

        keys_needing_representation = set()

        keys = list(self.order)
        for i, k in enumerate(keys):
            v = values[k]

            if not isinstance(v, VersionPart):
                # values coming from environment variables don't need
                # representation
                continue

            if not v.is_optional:
                keys_needing_representation = set(keys[: i + 1])

        required_by_format = set(labels_for_format(serialize_format))

        # try whether all parsed keys are represented
        if raise_if_incomplete and not keys_needing_representation <= required_by_format:
            missing_keys = keys_needing_representation ^ required_by_format
            raise FormattingError(
                f"""Could not represent '{"', '".join(missing_keys)}' in format '{serialize_format}'"""
            )

        return serialized

    def _choose_serialize_format(self, version: Version, context: MutableMapping) -> str:
        chosen = None

        logger.debug("Available serialization formats: '%s'", "', '".join(self.serialize_formats))

        for serialize_format in self.serialize_formats:
            try:
                self._serialize(version, serialize_format, context, raise_if_incomplete=True)
                # Prefer shorter or first search expression.
                chosen_part_count = len(list(string.Formatter().parse(chosen))) if chosen else None
                serialize_part_count = len(list(string.Formatter().parse(serialize_format)))
                if not chosen or chosen_part_count > serialize_part_count:
                    chosen = serialize_format
                    logger.debug("Found '%s' to be a usable serialization format", chosen)
                else:
                    logger.debug("Found '%s' usable serialization format, but it's longer", serialize_format)
            except FormattingError:
                # If chosen, prefer shorter
                if not chosen:
                    chosen = serialize_format
            except MissingValueError as e:
                logger.info(e.message)
                raise e

        if not chosen:
            raise KeyError("Did not find suitable serialization format")

        logger.debug("Selected serialization format '%s'", chosen)

        return chosen

    def serialize(self, version: Version, context: MutableMapping) -> str:
        """
        Serialize a version to a string.

        Args:
            version: The version to serialize
            context: The context to use when serializing the version

        Returns:
            The serialized version as a string
        """
        serialized = self._serialize(version, self._choose_serialize_format(version, context), context)
        logger.debug("Serialized to '%s'", serialized)
        return serialized
