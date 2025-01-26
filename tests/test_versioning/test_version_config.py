from pathlib import Path
from unittest.mock import MagicMock

import pytest
from click import UsageError

from bumpversion import exceptions
from bumpversion.context import get_context
from bumpversion.versioning.version_config import VersionConfig
from tests.conftest import get_config_data


def test_invalid_parse_raises_error():
    """An invalid parse regex value raises an error."""
    with pytest.raises(exceptions.UsageError):
        VersionConfig(r"(.+", ("{major}.{minor}.{patch}",), search="", replace="")


class TestParse:
    """Tests for parsing a version."""

    def test_cant_parse_returns_none(self):
        """The default behavior when unable to parse a string is to return None."""
        # Arrange
        overrides = {
            "current_version": "19.6.0",
            "parse": r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+).*",
            "serialize": ["{major}.{minor}.{patch}"],
        }
        _, version_config, current_version = get_config_data(overrides)

        # Act and Assert
        assert version_config.parse("A.B.C") is None

    def test_cant_parse_raises_error_when_set(self):
        """When `raise_error` is enabled, the inability to parse a string will raise an error."""
        # Arrange
        overrides = {
            "current_version": "19.6.0",
            "parse": r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+).*",
            "serialize": ["{major}.{minor}.{patch}"],
        }
        _, version_config, current_version = get_config_data(overrides)

        # Act and Assert
        with pytest.raises(exceptions.UsageError):
            version_config.parse("A.B.C", raise_error=True)


class TestSerialize:
    """Tests for the VersionConfig.serialize() method."""

    def test_distance_to_latest_tag_in_pattern(self):
        """Using ``distance_to_latest_tag`` in the serialization string outputs correctly."""
        from bumpversion.scm.models import SCMConfig, SCMInfo

        overrides = {
            "current_version": "19.6.0",
            "parse": r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+).*",
            "serialize": ["{major}.{minor}.{patch}-pre{distance_to_latest_tag}"],
        }
        conf, version_config, current_version = get_config_data(overrides)
        scm_config = SCMConfig.from_config(conf)
        scm_info = SCMInfo(scm_config)
        scm_info.current_version = "19.6.0"
        scm_info.distance_to_latest_tag = 3
        scm_info.commit_sha = "1234123412341234"
        conf.scm_info = scm_info
        assert version_config.serialize(current_version, get_context(conf)) == "19.6.0-pre3"

    def test_environment_var_in_serialize_pattern(self):
        """Environment variables are serialized correctly."""
        import os

        os.environ["BUILD_NUMBER"] = "567"
        overrides = {
            "current_version": "2.3.4",
            "parse": r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+).*",
            "serialize": ["{major}.{minor}.{patch}-pre{$BUILD_NUMBER}"],
        }
        conf, version_config, current_version = get_config_data(overrides)
        assert version_config.serialize(current_version, get_context(conf)) == "2.3.4-pre567"
        del os.environ["BUILD_NUMBER"]
