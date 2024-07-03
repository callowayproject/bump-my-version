"""Tests for the config.__init__ module."""

from dataclasses import dataclass
from typing import Optional

from bumpversion.scm import SCMInfo
from bumpversion.config import check_current_version


@dataclass
class MockConfig:
    """Just includes the current_version and scm_info attributes."""

    current_version: Optional[str]
    scm_info: SCMInfo


class TestCheckCurrentVersion:
    """
    Tests for the check_current_version function.

    - tag may not match serialization
    - tag may not match current version in config
    """

    def test_uses_tag_when_missing_current_version(self):
        """When the config does not have a current_version, the last tag is used."""
        # Assemble
        scm_info = SCMInfo()
        scm_info.current_version = "1.2.3"
        config = MockConfig(current_version=None, scm_info=scm_info)

        # Act
        result = check_current_version(config)

        # Assert
        assert result == "1.2.3"
