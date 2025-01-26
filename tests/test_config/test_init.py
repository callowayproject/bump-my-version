"""Tests for the config.__init__ module."""

from unittest.mock import Mock

from bumpversion.config import Config, check_current_version
from bumpversion.scm.models import SCMConfig, SCMInfo


class TestCheckCurrentVersion:
    """
    Tests for the check_current_version function.

    - tag may not match serialization
    - tag may not match current version in config
    """

    def test_uses_tag_when_missing_current_version(self, scm_config: SCMConfig):
        """When the config does not have a current_version, the last tag is used."""
        # Arrange

        scm_info = SCMInfo(scm_config)
        scm_info.current_version = "1.2.3"
        config = Mock(spec=Config, current_version=None, scm_info=scm_info)

        # Act
        result = check_current_version(config)

        # Assert
        assert result == "1.2.3"
