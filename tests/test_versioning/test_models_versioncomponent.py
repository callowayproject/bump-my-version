"""Tests of the VersionPart model."""

from freezegun import freeze_time

from bumpversion.versioning.models import VersionComponentSpec
from bumpversion.versioning.functions import ValuesFunction, NumericFunction, CalVerFunction
import pytest

params = {
    "numeric": [{"optional_value": "0", "first_value": "0"}],
    "values": [{"values": ["alpha", "beta", "gamma"]}],
    "calver": [{"calver_format": "{YYYY}.{MM}.{DD}"}],
}


@pytest.fixture
def version_component_config(request):
    """Return a three-part and a two-part version part configuration."""
    return VersionComponentSpec(**request.param)


class TestVersionComponent:
    class TestCreation:
        @pytest.mark.parametrize(
            ["version_component_config"],
            [
                params["numeric"],
                params["values"],
            ],
            ids=["numeric", "values"],
            indirect=True,
        )
        def test_none_value_uses_optional_value(self, version_component_config: VersionComponentSpec):
            """When passing in no value, the optional value is used."""
            vp = version_component_config.create_component()
            assert vp.value == vp.func.optional_value
            assert vp._value is None

        @pytest.mark.parametrize(
            ["version_component_config"],
            [params["calver"]],
            ids=["calver"],
            indirect=True,
        )
        @freeze_time("2020-05-01")
        def test_none_value_uses_current_date(self, version_component_config: VersionComponentSpec):
            """When passing in no value, the current date is used for CalVer components."""
            vp = version_component_config.create_component()
            assert vp.value == "2020.5.1"
            assert vp._value == "2020.5.1"

        def test_config_with_values_selects_values_function(self):
            values = ["0", "1", "2"]
            vp = VersionComponentSpec(values=values).create_component()
            assert isinstance(vp.func, ValuesFunction)

        def test_config_with_calver_selects_calver_function(self):
            vp = VersionComponentSpec(calver_format="{YYYY}.{MM}").create_component()
            assert isinstance(vp.func, CalVerFunction)

        def test_config_defaults_to_numeric_function(self):
            vp = VersionComponentSpec().create_component()
            assert isinstance(vp.func, NumericFunction)

    @pytest.mark.parametrize(
        ["version_component_config"],
        [
            params["numeric"],
            params["values"],
            params["calver"],
        ],
        ids=["numeric", "values", "calver"],
        indirect=True,
    )
    def test_copy_returns_new_version_part(self, version_component_config):
        vp = version_component_config.create_component(version_component_config.first_value)
        vc = vp.copy()
        assert vp.value == vc.value
        assert id(vp) != id(vc)

    @pytest.mark.parametrize(
        ["version_component_config"],
        [params["numeric"]],
        ids=["numeric"],
        indirect=True,
    )
    def test_bump_increments_numeric_value(self, version_component_config):
        vp = version_component_config.create_component(version_component_config.first_value)
        vc = vp.bump()
        assert vc.value == str(int(version_component_config.first_value) + 1)

    @pytest.mark.parametrize(
        ["version_component_config"],
        [params["values"]],
        ids=["values"],
        indirect=True,
    )
    def test_bump_selects_next_value(self, version_component_config):
        vp = version_component_config.create_component(version_component_config.first_value)
        vc = vp.bump()
        assert vc.value == str(version_component_config.values[1])

    @pytest.mark.parametrize(
        ["version_component_config"],
        [
            params["numeric"],
            params["values"],
            params["calver"],
        ],
        ids=["numeric", "values", "calver"],
        indirect=True,
    )
    def test_non_first_value_is_not_optional(self, version_component_config):
        assert not version_component_config.create_component(version_component_config.first_value).bump().is_optional

    @pytest.mark.parametrize(
        ["version_component_config"],
        [params["calver"]],
        ids=["calver"],
        indirect=True,
    )
    def test_calver_is_not_optional(self, version_component_config):
        vc = version_component_config.create_component(version_component_config.first_value)
        assert not vc.is_optional

    @pytest.mark.parametrize(
        ["version_component_config"],
        [params["numeric"], params["values"]],
        ids=["numeric", "values"],
        indirect=True,
    )
    def test_first_value_is_optional(self, version_component_config):
        vc = version_component_config.create_component(version_component_config.first_value)
        assert vc.is_optional

    @pytest.mark.parametrize(
        ["version_component_config"],
        [
            params["numeric"],
            params["values"],
            params["calver"],
        ],
        ids=["numeric", "values", "calver"],
        indirect=True,
    )
    def test_versionparts_with_same_settings_are_equal(self, version_component_config):
        version1 = version_component_config.create_component(version_component_config.first_value)
        version2 = version_component_config.create_component(version_component_config.first_value)
        assert version1 == version2

    @pytest.mark.parametrize(
        ["version_component_config"],
        [
            params["numeric"],
            params["values"],
            params["calver"],
        ],
        ids=["numeric", "values", "calver"],
        indirect=True,
    )
    def test_null_resets_value_to_first_value(self, version_component_config):
        version1 = version_component_config.create_component(version_component_config.first_value)
        version2 = version1.bump().null()
        assert version2 == version1
