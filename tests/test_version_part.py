from pathlib import Path

import pytest
from click import UsageError

from bumpversion import exceptions
from bumpversion.utils import get_context
from tests.conftest import get_config_data, inside_dir


def test_bump_version_missing_part():
    overrides = {
        "current_version": "1.0.0",
    }
    conf, version_config, current_version = get_config_data(overrides)
    with pytest.raises(exceptions.InvalidVersionPartError, match="No part named 'bugfix'"):
        current_version.bump("bugfix")


def test_build_number_configuration():
    overrides = {
        "current_version": "2.1.6-5123",
        "parse": r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)\-(?P<build>\d+)",
        "serialize": ["{major}.{minor}.{patch}-{build}"],
        "parts": {
            "build": {
                "independent": True,
            }
        },
    }
    conf, version_config, current_version = get_config_data(overrides)

    build_version_bump = current_version.bump("build")
    assert build_version_bump["build"].value == "5124"
    assert build_version_bump["build"].is_independent

    major_version_bump = build_version_bump.bump("major")
    assert major_version_bump["build"].value == "5124"
    assert build_version_bump["build"].is_independent
    assert major_version_bump["major"].value == "3"

    build_version_bump = major_version_bump.bump("build")
    assert build_version_bump["build"].value == "5125"
    assert build_version_bump["build"].is_independent


def test_serialize_with_distance_to_latest_tag():
    """Using ``distance_to_latest_tag`` in the serialization string outputs correctly."""
    from bumpversion.scm import Git, SCMInfo

    overrides = {
        "current_version": "19.6.0",
        "parse": r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+).*",
        "serialize": ["{major}.{minor}.{patch}-pre{distance_to_latest_tag}"],
    }
    conf, version_config, current_version = get_config_data(overrides)
    conf.scm_info = SCMInfo(
        tool=Git, commit_sha="1234123412341234", distance_to_latest_tag=3, current_version="19.6.0", dirty=False
    )
    assert version_config.serialize(current_version, get_context(conf)) == "19.6.0-pre3"


def test_serialize_with_environment_var():
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


def test_version_part_invalid_regex_exit(tmp_path: Path) -> None:
    """A version part with an invalid regex should raise an exception."""
    # Arrange
    overrides = {
        "current_version": "12",
        "parse": "*kittens*",
    }
    with inside_dir(tmp_path):
        with pytest.raises(UsageError):
            get_config_data(overrides)
