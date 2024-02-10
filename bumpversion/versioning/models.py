"""Models for managing versioning of software projects."""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel

from bumpversion.exceptions import InvalidVersionPartError
from bumpversion.utils import key_val_string
from bumpversion.versioning.functions import NumericFunction, PartFunction, ValuesFunction


class VersionComponent:
    """
    Represent part of a version number.

    Determines the PartFunction that rules how the part behaves when increased or reset
    based on the configuration given.
    """

    def __init__(
        self,
        values: Optional[list] = None,
        optional_value: Optional[str] = None,
        first_value: Union[str, int, None] = None,
        independent: bool = False,
        source: Optional[str] = None,
        value: Union[str, int, None] = None,
    ):
        self._value = str(value) if value is not None else None
        self.func: Optional[PartFunction] = None
        self.independent = independent
        self.source = source
        if values:
            str_values = [str(v) for v in values]
            str_optional_value = str(optional_value) if optional_value is not None else None
            str_first_value = str(first_value) if first_value is not None else None
            self.func = ValuesFunction(str_values, str_optional_value, str_first_value)
        else:
            self.func = NumericFunction(optional_value, first_value or "0")

    @property
    def value(self) -> str:
        """Return the value of the part."""
        return self._value or self.func.optional_value

    def copy(self) -> "VersionComponent":
        """Return a copy of the part."""
        return VersionComponent(
            values=getattr(self.func, "_values", None),
            optional_value=self.func.optional_value,
            first_value=self.func.first_value,
            independent=self.independent,
            source=self.source,
            value=self._value,
        )

    def bump(self) -> "VersionComponent":
        """Return a part with bumped value."""
        new_component = self.copy()
        new_component._value = self.func.bump(self.value)
        return new_component

    def null(self) -> "VersionComponent":
        """Return a part with first value."""
        new_component = self.copy()
        new_component._value = self.func.first_value
        return new_component

    @property
    def is_optional(self) -> bool:
        """Is the part optional?"""
        return self.value == self.func.optional_value

    @property
    def is_independent(self) -> bool:
        """Is the part independent of the other parts?"""
        return self.independent

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
        return self.value == other.value if isinstance(other, VersionComponent) else False


class VersionComponentSpec(BaseModel):
    """
    Configuration of a version component.

    This is used to read in the configuration from the bumpversion config file.
    """

    values: Optional[list] = None  # Optional. Numeric is used if missing or no items in list
    optional_value: Optional[str] = None  # Optional.
    # Defaults to first value. 0 in the case of numeric. Empty string means nothing is optional.
    first_value: Union[str, int, None] = None  # Optional. Defaults to first value in values
    independent: bool = False
    # source: Optional[str] = None  # Name of environment variable or context variable to use as the source for value
    depends_on: Optional[str] = None  # The name of the component this component depends on

    def create_component(self, value: Union[str, int, None] = None) -> VersionComponent:
        """Generate a version component from the configuration."""
        return VersionComponent(
            values=self.values,
            optional_value=self.optional_value,
            first_value=self.first_value,
            independent=self.independent,
            # source=self.source,
            value=value,
        )


class VersionSpec:
    """The specification of a version's components and their relationships."""

    def __init__(self, components: Dict[str, VersionComponentSpec], order: Optional[List[str]] = None):
        if not components:
            raise ValueError("A VersionSpec must have at least one component.")
        if not order:
            order = list(components.keys())
        if len(set(order) - set(components.keys())) > 0:
            raise ValueError("The order of components refers to items that are not in your components.")

        self.component_configs = components
        self.order = order
        self.dependency_map = defaultdict(list)
        previous_component = self.order[0]
        for component in self.order[1:]:
            if self.component_configs[component].independent:
                continue
            elif self.component_configs[component].depends_on:
                self.dependency_map[self.component_configs[component].depends_on].append(component)
            else:
                self.dependency_map[previous_component].append(component)
            previous_component = component

    def create_version(self, values: Dict[str, str]) -> "Version":
        """Generate a version from the given values."""
        components = {
            key: comp_config.create_component(value=values.get(key))
            for key, comp_config in self.component_configs.items()
        }
        return Version(version_spec=self, components=components)

    def get_dependents(self, component_name: str) -> List[str]:
        """Return the parts that depend on the given part."""
        stack = deque(self.dependency_map.get(component_name, []), maxlen=len(self.order))
        visited = []

        while stack:
            e = stack.pop()
            if e not in visited:
                visited.append(e)
                stack.extendleft(self.dependency_map[e])

        return visited


class Version:
    """The specification of a version and its parts."""

    def __init__(
        self, version_spec: VersionSpec, components: Dict[str, VersionComponent], original: Optional[str] = None
    ):
        self.version_spec = version_spec
        self.components = components
        self.original = original

    def values(self) -> Dict[str, str]:
        """Return the values of the parts."""
        return {key: value.value for key, value in self.components.items()}

    def __getitem__(self, key: str) -> VersionComponent:
        return self.components[key]

    def __len__(self) -> int:
        return len(self.components)

    def __iter__(self):
        return iter(self.components)

    def __repr__(self):
        return f"<bumpversion.Version:{key_val_string(self.components)}>"

    def __eq__(self, other: Any) -> bool:
        return (
            all(value == other.components[key] for key, value in self.components.items())
            if isinstance(other, Version)
            else False
        )

    def required_components(self) -> List[str]:
        """Return the names of the parts that are required."""
        return [key for key, value in self.components.items() if value.value != value.func.optional_value]

    def bump(self, component_name: str) -> "Version":
        """Increase the value of the specified component, reset its dependents, and return a new Version."""
        if component_name not in self.components:
            raise InvalidVersionPartError(f"No part named {component_name!r}")

        components_to_reset = self.version_spec.get_dependents(component_name)

        new_values = dict(self.components.items())
        new_values[component_name] = self.components[component_name].bump()
        for component in components_to_reset:
            if not self.components[component].is_independent:
                new_values[component] = self.components[component].null()

        return Version(self.version_spec, new_values, self.original)
