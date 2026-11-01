"""Tests for the config.__init__ module."""

import logging
from typing import Optional
from unittest.mock import Mock

import pytest

from bumpversion.config import DEFAULTS, Config, check_current_version
from bumpversion.config.models import PEP621Info
from bumpversion.config.utils import get_all_part_configs
from bumpversion.scm.models import SCMConfig, SCMInfo
from bumpversion.versioning.version_config import VersionConfig

SUFFIX_FORMAT = {
    "parse": r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(?P<suffix>[a-z]*)",
    "serialize": ("{major}.{minor}.{patch}{suffix}",),
}
RELEASE_VALUES_FORMAT = {
    "parse": r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(-(?P<release>[a-z]+))?",
    "serialize": ("{major}.{minor}.{patch}-{release}", "{major}.{minor}.{patch}"),
    "parts": {"release": {"values": ["dev", "rc", "final"], "optional_value": "final"}},
}


class TestCheckCurrentVersion:
    """
    Tests for the check_current_version function.

    - tag may not match serialization
    - tag may not match current version in config
    """

    def test_uses_pep621_version_when_missing_current_version(self, scm_config: SCMConfig):
        """When the config does not have a current_version, the PEP 621 project.version is used."""
        # Arrange

        pep621_info = PEP621Info(version="1.2.4")
        scm_info = SCMInfo(scm_config)
        scm_info.current_version = "1.2.3"
        config = Mock(spec=Config, current_version=None, pep621_info=pep621_info, scm_info=scm_info)

        # Act
        result = check_current_version(config)

        # Assert
        assert result == "1.2.4"

    @staticmethod
    def make_config(
        scm_config: SCMConfig, current: str, tagged: Optional[str], overrides: Optional[dict] = None
    ) -> Mock:
        """Create a config with a real VersionConfig, so versions can be parsed and compared."""
        settings = {**DEFAULTS, **(overrides or {})}
        parts = get_all_part_configs(settings)
        version_config = VersionConfig(settings["parse"], settings["serialize"], "", "", parts)
        scm_info = SCMInfo(scm_config)
        scm_info.current_version = tagged
        return Mock(
            spec=Config, current_version=current, pep621_info=None, scm_info=scm_info, version_config=version_config
        )

    @pytest.mark.parametrize(
        ("current", "tagged", "overrides", "warns"),
        [
            pytest.param("1.2.4", "1.2.3", None, False, id="ahead-of-tag"),
            pytest.param("1.2.3", "1.2.3", None, False, id="equal-to-tag"),
            pytest.param("1.2.2", "1.2.3", None, True, id="behind-tag"),
            pytest.param("1.10.0", "1.9.0", None, False, id="numeric-not-lexical"),
            pytest.param("1.2.03", "1.2.3", None, False, id="equal-parsed-components"),
            pytest.param("not-a-version", "1.2.3", None, False, id="unparsable"),
            pytest.param("1.2.3", None, None, False, id="no-tag"),
            pytest.param("1.2.3a", "1.2.3b", SUFFIX_FORMAT, False, id="non-numeric-component"),
            pytest.param("1.0.0-dev", "1.0.0-rc", RELEASE_VALUES_FORMAT, True, id="values-component-behind"),
        ],
    )
    def test_warns_only_when_version_is_behind_tag(
        self, caplog, scm_config: SCMConfig, current: str, tagged: Optional[str], overrides: Optional[dict], warns: bool
    ):
        """Only a version provably behind the last tag logs a warning; otherwise it is at most a debug message."""
        config = self.make_config(scm_config, current, tagged, overrides)

        with caplog.at_level(logging.DEBUG):
            result = check_current_version(config)

        assert result == current
        assert any(r.levelno == logging.WARNING for r in caplog.records) is warns

    @pytest.mark.parametrize("pep621_info", [PEP621Info(version=None), None])
    def test_uses_tag_when_missing_current_version(self, scm_config: SCMConfig, pep621_info: Optional[PEP621Info]):
        """When the config has neither current_version nor PEP 621 project.version, the last tag is used."""
        # Arrange

        scm_info = SCMInfo(scm_config)
        scm_info.current_version = "1.2.3"
        config = Mock(spec=Config, current_version=None, pep621_info=pep621_info, scm_info=scm_info)

        # Act
        result = check_current_version(config)

        # Assert
        assert result == "1.2.3"
