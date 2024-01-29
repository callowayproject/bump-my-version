"""Tests of the VersionPart model."""

from bumpversion.versioning.models import VersionComponentSpec
from bumpversion.versioning.functions import ValuesFunction, NumericFunction
import pytest


@pytest.fixture(
    params=[
        {"optional_value": "0", "first_value": "0"},
        {"first_value": "1"},
        {"values": ["alpha", "beta", "gamma"]},
        {"values": ["alpha", "gamma"]},
    ]
)
def version_component_config(request):
    """Return a three-part and a two-part version part configuration."""
    return VersionComponentSpec(**request.param)


class TestVersionComponent:
    class TestCreation:
        def test_none_value_uses_optional_value(self, version_component_config):
            vp = version_component_config.create_component()
            assert vp.value == vp.func.optional_value
            assert vp._value is None

        def test_config_with_values_selects_values_function(self):
            values = ["0", "1", "2"]
            vp = VersionComponentSpec(values=values).create_component()
            assert isinstance(vp.func, ValuesFunction)

        def test_config_without_values_selects_numeric_function(self):
            vp = VersionComponentSpec().create_component()
            assert isinstance(vp.func, NumericFunction)

    def test_copy_returns_new_version_part(self, version_component_config):
        vp = version_component_config.create_component(version_component_config.first_value)
        vc = vp.copy()
        assert vp.value == vc.value
        assert id(vp) != id(vc)

    def test_bump_increments_value(self, version_component_config):
        vp = version_component_config.create_component(version_component_config.first_value)
        vc = vp.bump()
        if version_component_config.values:
            assert vc.value == str(version_component_config.values[1])
        else:
            assert vc.value == str(int(version_component_config.first_value) + 1)

    def test_non_first_value_is_not_optional(self, version_component_config):
        assert not version_component_config.create_component(version_component_config.first_value).bump().is_optional

    def test_first_value_is_optional(self, version_component_config):
        assert version_component_config.create_component(version_component_config.first_value).is_optional

    def test_versionparts_with_same_settings_are_equal(self, version_component_config):
        version1 = version_component_config.create_component(version_component_config.first_value)
        version2 = version_component_config.create_component(version_component_config.first_value)
        assert version1 == version2

    def test_null_resets_value_to_first_value(self, version_component_config):
        version1 = version_component_config.create_component(version_component_config.first_value)
        version2 = version1.bump().null()
        assert version2 == version1
