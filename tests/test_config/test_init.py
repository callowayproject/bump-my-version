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
        ("current", "tagged", "level"),
        [
            pytest.param("1.2.4", "1.2.3", None, id="ahead-of-tag"),
            pytest.param("1.2.3", "1.2.3", None, id="equal-to-tag"),
            pytest.param("1.2.2", "1.2.3", logging.WARNING, id="behind-tag"),
            pytest.param("1.10.0", "1.9.0", None, id="numeric-not-lexical"),
            pytest.param("not-a-version", "1.2.3", None, id="unparsable"),
        ],
    )
    def test_tag_mismatch_logging(self, caplog, scm_config: SCMConfig, current: str, tagged: str, level: Optional[int]):
        """Only a version behind the last tag logs a warning, otherwise it is at most a debug message."""
        config = self.make_config(scm_config, current, tagged)

        with caplog.at_level(logging.DEBUG):
            result = check_current_version(config)

        assert result == current
        mismatches = [r for r in caplog.records if "does not match last tagged version" in r.getMessage()]
        warnings = [r for r in mismatches if r.levelno == logging.WARNING]
        assert bool(warnings) is (level == logging.WARNING)
        assert len(mismatches) == (1 if current != tagged else 0)

    def test_no_tag_logs_nothing(self, caplog, scm_config: SCMConfig):
        """Without a tag there is nothing to compare against."""
        config = self.make_config(scm_config, "1.2.3", None)

        with caplog.at_level(logging.DEBUG):
            check_current_version(config)

        assert not [r for r in caplog.records if "last tagged version" in r.getMessage()]

    def test_tag_mismatch_with_values_component(self, caplog, scm_config: SCMConfig):
        """Components with a `values` list compare by position in the list."""
        overrides = {
            "parse": r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(-(?P<release>[a-z]+))?",
            "serialize": ("{major}.{minor}.{patch}-{release}", "{major}.{minor}.{patch}"),
            "parts": {"release": {"values": ["dev", "rc", "final"], "optional_value": "final"}},
        }
        config = self.make_config(scm_config, "1.0.0-dev", "1.0.0-rc", overrides)

        with caplog.at_level(logging.DEBUG):
            check_current_version(config)

        assert [r.levelno for r in caplog.records if "last tagged version" in r.getMessage()] == [logging.WARNING]

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
