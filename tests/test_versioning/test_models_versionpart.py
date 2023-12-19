"""Tests of the VersionPart model."""

from bumpversion.versioning.models import VersionPart
from bumpversion.config.models import VersionPartConfig
from bumpversion.versioning.functions import ValuesFunction, NumericFunction
import pytest


@pytest.fixture(
    params=[
        None,
        ("0", "1", "2"),
        ("0", "3"),
    ]
)
def version_part_config(request):
    """Return a three-part and a two-part version part configuration."""
    if request.param is None:
        return VersionPartConfig(optional_value="0", first_value="0")
    else:
        return VersionPartConfig(values=request.param)


class TestVersionPartConfig:
    class TestCreation:
        def test_none_value_uses_optional_value(self, version_part_config):
            vp = VersionPart(version_part_config)
            assert vp.value == vp.func.optional_value
            assert vp._value is None

        def test_config_with_values_selects_values_function(self):
            values = ["0", "1", "2"]
            vp = VersionPart(VersionPartConfig(values=values))
            assert isinstance(vp.func, ValuesFunction)

        def test_config_without_values_selects_numeric_function(self):
            vp = VersionPart(VersionPartConfig())
            assert isinstance(vp.func, NumericFunction)

    def test_copy_returns_new_version_part(self, version_part_config):
        vp = VersionPart(version_part_config, version_part_config.first_value)
        vc = vp.copy()
        assert vp.value == vc.value
        assert id(vp) != id(vc)

    def test_bump_increments_value(self, version_part_config):
        vp = VersionPart(version_part_config, version_part_config.first_value)
        vc = vp.bump()
        if version_part_config.values:
            assert vc.value == str(version_part_config.values[1])
        else:
            assert vc.value == "1"

    def test_non_first_value_is_not_optional(self, version_part_config):
        assert not VersionPart(version_part_config, version_part_config.first_value).bump().is_optional

    def test_first_value_is_optional(self, version_part_config):
        assert VersionPart(version_part_config, version_part_config.first_value).is_optional

    def test_versionparts_with_same_settings_are_equal(self, version_part_config):
        assert VersionPart(version_part_config, version_part_config.first_value) == VersionPart(
            version_part_config, version_part_config.first_value
        )

    def test_null_resets_value_to_first_value(self, version_part_config):
        assert VersionPart(version_part_config, version_part_config.first_value).null() == VersionPart(
            version_part_config, version_part_config.first_value
        )
