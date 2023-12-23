"""Module for managing Versions and their internal parts."""
import re
import string
from copy import copy
from typing import Any, Dict, List, MutableMapping, Optional, Tuple

from click import UsageError
from versioning.models import VersionComponentConfig

from bumpversion.exceptions import FormattingError, MissingValueError
from bumpversion.ui import get_indented_logger
from bumpversion.utils import labels_for_format
from bumpversion.versioning.models import Version, VersionComponent, VersionSpec
from bumpversion.versioning.serialization import parse_version

logger = get_indented_logger(__name__)


class VersionConfig:
    """
    Hold a complete representation of a version string.
    """

    def __init__(
        self,
        parse: str,
        serialize: Tuple[str],
        search: str,
        replace: str,
        part_configs: Optional[Dict[str, VersionComponentConfig]] = None,
    ):
        try:
            self.parse_regex = re.compile(parse, re.VERBOSE)
        except re.error as e:
            raise UsageError(f"--parse '{parse}' is not a valid regex.") from e

        self.serialize_formats = serialize
        self.part_configs = part_configs or {}
        self.version_spec = VersionSpec(self.part_configs)
        # TODO: I think these two should be removed from the config object
        self.search = search
        self.replace = replace

    def __repr__(self) -> str:
        return f"<bumpversion.VersionConfig:{self.parse_regex.pattern}:{self.serialize_formats}>"

    def __eq__(self, other: Any) -> bool:
        return (
            self.parse_regex.pattern == other.parse_regex.pattern
            and self.serialize_formats == other.serialize_formats
            and self.part_configs == other.part_configs
            and self.search == other.search
            and self.replace == other.replace
        )

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
        parsed = parse_version(version_string, self.parse_regex.pattern)

        if not parsed:
            return None

        version = self.version_spec.create_version(parsed)
        version.original = version_string
        return version

        # _parsed = {
        #     key: VersionComponent(self.part_configs[key], value)
        #     for key, value in parsed.items()
        #     if key in self.part_configs
        # }
        # return Version(_parsed, version_string)

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

            if not isinstance(v, VersionComponent):
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
        """
        Choose a serialization format for the given version and context.

        Args:
            version: The version to serialize
            context: The context to use when serializing the version

        Returns:
            The serialized version as a string

        Raises:
            MissingValueError: if not all parts required in the format have values
        """
        chosen = None

        logger.debug("Evaluating serialization formats")
        logger.indent()
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
        logger.dedent()
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
        logger.debug("Serializing version '%s'", version)
        logger.indent()
        serialized = self._serialize(version, self._choose_serialize_format(version, context), context)
        logger.debug("Serialized to '%s'", serialized)
        logger.dedent()
        return serialized
