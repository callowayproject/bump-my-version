"""Tests for the config.__init__ module."""

from typing import Optional
from unittest.mock import Mock

import pytest

from bumpversion.config import Config, check_current_version
from bumpversion.config.models import PEP621Info
from bumpversion.scm.models import SCMConfig, SCMInfo


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
