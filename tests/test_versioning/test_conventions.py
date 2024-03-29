"""Test the versioning conventions."""

from bumpversion.versioning.conventions import (
    PEP440_COMPONENT_CONFIGS,
    PEP440_PATTERN,
    PEP440_SERIALIZE_PATTERNS,
)
import re

import pytest
from pytest import param


@pytest.mark.parametrize(
    ["version", "expected"],
    [
        param(
            "1.2.3a123.post123.dev123+local.123",
            {
                "dev": "dev123",
                "local": "local.123",
                "major": "1",
                "minor": "2",
                "patch": "3",
                "post": "post123",
                "pre": "a123",
                "pre_l": "a",
                "pre_n": "123",
            },
            id="alpha-post-dev-local",
        ),
        param(
            "1.2.3b123.post123.dev123+local.123",
            {
                "dev": "dev123",
                "local": "local.123",
                "major": "1",
                "minor": "2",
                "patch": "3",
                "post": "post123",
                "pre": "b123",
                "pre_l": "b",
                "pre_n": "123",
            },
            id="beta-post-dev-local",
        ),
        param(
            "1.2.3rc123.post123.dev123+local.123",
            {
                "dev": "dev123",
                "local": "local.123",
                "major": "1",
                "minor": "2",
                "patch": "3",
                "post": "post123",
                "pre": "rc123",
                "pre_l": "rc",
                "pre_n": "123",
            },
            id="rc-post-dev-local",
        ),
        param(
            "1.2.3a123.post123.dev123",
            {
                "dev": "dev123",
                "local": None,
                "major": "1",
                "minor": "2",
                "patch": "3",
                "post": "post123",
                "pre": "a123",
                "pre_l": "a",
                "pre_n": "123",
            },
            id="alpha-post-dev",
        ),
        param(
            "1.2.3b123.post123.dev123",
            {
                "dev": "dev123",
                "local": None,
                "major": "1",
                "minor": "2",
                "patch": "3",
                "post": "post123",
                "pre": "b123",
                "pre_l": "b",
                "pre_n": "123",
            },
            id="beta-post-dev",
        ),
        param(
            "1.2.3rc123.post123.dev123",
            {
                "dev": "dev123",
                "local": None,
                "major": "1",
                "minor": "2",
                "patch": "3",
                "post": "post123",
                "pre": "rc123",
                "pre_l": "rc",
                "pre_n": "123",
            },
            id="rc-post-dev",
        ),
        param(
            "1.2.3a123.post123+local.123",
            {
                "dev": None,
                "local": "local.123",
                "major": "1",
                "minor": "2",
                "patch": "3",
                "post": "post123",
                "pre": "a123",
                "pre_l": "a",
                "pre_n": "123",
            },
            id="alpha-post-local",
        ),
        param(
            "1.2.3b123.post123+local.123",
            {
                "dev": None,
                "local": "local.123",
                "major": "1",
                "minor": "2",
                "patch": "3",
                "post": "post123",
                "pre": "b123",
                "pre_l": "b",
                "pre_n": "123",
            },
            id="beta-post-local",
        ),
        param(
            "1.2.3rc123.post123+local.123",
            {
                "dev": None,
                "local": "local.123",
                "major": "1",
                "minor": "2",
                "patch": "3",
                "post": "post123",
                "pre": "rc123",
                "pre_l": "rc",
                "pre_n": "123",
            },
            id="rc-post-local",
        ),
        param(
            "1.2.3a123.dev123+local.123",
            {
                "dev": "dev123",
                "local": "local.123",
                "major": "1",
                "minor": "2",
                "patch": "3",
                "post": None,
                "pre": "a123",
                "pre_l": "a",
                "pre_n": "123",
            },
            id="alpha-dev-local",
        ),
        param(
            "1.2.3b123.dev123+local.123",
            {
                "dev": "dev123",
                "local": "local.123",
                "major": "1",
                "minor": "2",
                "patch": "3",
                "post": None,
                "pre": "b123",
                "pre_l": "b",
                "pre_n": "123",
            },
            id="beta-dev-local",
        ),
        param(
            "1.2.3rc123.dev123+local.123",
            {
                "dev": "dev123",
                "local": "local.123",
                "major": "1",
                "minor": "2",
                "patch": "3",
                "post": None,
                "pre": "rc123",
                "pre_l": "rc",
                "pre_n": "123",
            },
            id="rc-dev-local",
        ),
        param(
            "1.2.3.post123.dev123+local.123",
            {
                "dev": "dev123",
                "local": "local.123",
                "major": "1",
                "minor": "2",
                "patch": "3",
                "post": "post123",
                "pre": None,
                "pre_l": None,
                "pre_n": None,
            },
            id="post-dev-local",
        ),
        param(
            "1.2.3a123.post123",
            {
                "dev": None,
                "local": None,
                "major": "1",
                "minor": "2",
                "patch": "3",
                "post": "post123",
                "pre": "a123",
                "pre_l": "a",
                "pre_n": "123",
            },
            id="alpha-post",
        ),
        param(
            "1.2.3b123.post123",
            {
                "dev": None,
                "local": None,
                "major": "1",
                "minor": "2",
                "patch": "3",
                "post": "post123",
                "pre": "b123",
                "pre_l": "b",
                "pre_n": "123",
            },
            id="beta-post",
        ),
        param(
            "1.2.3rc123.post123",
            {
                "dev": None,
                "local": None,
                "major": "1",
                "minor": "2",
                "patch": "3",
                "post": "post123",
                "pre": "rc123",
                "pre_l": "rc",
                "pre_n": "123",
            },
            id="rc-post",
        ),
        param(
            "1.2.3a123.dev123",
            {
                "dev": "dev123",
                "local": None,
                "major": "1",
                "minor": "2",
                "patch": "3",
                "post": None,
                "pre": "a123",
                "pre_l": "a",
                "pre_n": "123",
            },
            id="alpha-dev",
        ),
        param(
            "1.2.3b123.dev123",
            {
                "dev": "dev123",
                "local": None,
                "major": "1",
                "minor": "2",
                "patch": "3",
                "post": None,
                "pre": "b123",
                "pre_l": "b",
                "pre_n": "123",
            },
            id="beta-dev",
        ),
        param(
            "1.2.3rc123.dev123",
            {
                "dev": "dev123",
                "local": None,
                "major": "1",
                "minor": "2",
                "patch": "3",
                "post": None,
                "pre": "rc123",
                "pre_l": "rc",
                "pre_n": "123",
            },
            id="rc-dev",
        ),
        param(
            "1.2.3a123+local.123",
            {
                "dev": None,
                "local": "local.123",
                "major": "1",
                "minor": "2",
                "patch": "3",
                "post": None,
                "pre": "a123",
                "pre_l": "a",
                "pre_n": "123",
            },
            id="alpha-local",
        ),
        param(
            "1.2.3b123+local.123",
            {
                "dev": None,
                "local": "local.123",
                "major": "1",
                "minor": "2",
                "patch": "3",
                "post": None,
                "pre": "b123",
                "pre_l": "b",
                "pre_n": "123",
            },
            id="beta-local",
        ),
        param(
            "1.2.3rc123+local.123",
            {
                "dev": None,
                "local": "local.123",
                "major": "1",
                "minor": "2",
                "patch": "3",
                "post": None,
                "pre": "rc123",
                "pre_l": "rc",
                "pre_n": "123",
            },
            id="rc-local",
        ),
        param(
            "1.2.3.post123.dev123",
            {
                "dev": "dev123",
                "local": None,
                "major": "1",
                "minor": "2",
                "patch": "3",
                "post": "post123",
                "pre": None,
                "pre_l": None,
                "pre_n": None,
            },
            id="post-dev",
        ),
        param(
            "1.2.3.post123+local.123",
            {
                "dev": None,
                "local": "local.123",
                "major": "1",
                "minor": "2",
                "patch": "3",
                "post": "post123",
                "pre": None,
                "pre_l": None,
                "pre_n": None,
            },
            id="post-local",
        ),
        param(
            "1.2.3.dev123+local.123",
            {
                "dev": "dev123",
                "local": "local.123",
                "major": "1",
                "minor": "2",
                "patch": "3",
                "post": None,
                "pre": None,
                "pre_l": None,
                "pre_n": None,
            },
            id="dev-local",
        ),
        param(
            "1.2.3a123",
            {
                "dev": None,
                "local": None,
                "major": "1",
                "minor": "2",
                "patch": "3",
                "post": None,
                "pre": "a123",
                "pre_l": "a",
                "pre_n": "123",
            },
            id="alpha",
        ),
        param(
            "1.2.3b123",
            {
                "dev": None,
                "local": None,
                "major": "1",
                "minor": "2",
                "patch": "3",
                "post": None,
                "pre": "b123",
                "pre_l": "b",
                "pre_n": "123",
            },
            id="beta",
        ),
        param(
            "1.2.3rc123",
            {
                "dev": None,
                "local": None,
                "major": "1",
                "minor": "2",
                "patch": "3",
                "post": None,
                "pre": "rc123",
                "pre_l": "rc",
                "pre_n": "123",
            },
            id="rc",
        ),
        param(
            "1.2.3.post123",
            {
                "dev": None,
                "local": None,
                "major": "1",
                "minor": "2",
                "patch": "3",
                "post": "post123",
                "pre": None,
                "pre_l": None,
                "pre_n": None,
            },
            id="post",
        ),
        param(
            "1.2.3.dev123",
            {
                "dev": "dev123",
                "local": None,
                "major": "1",
                "minor": "2",
                "patch": "3",
                "post": None,
                "pre": None,
                "pre_l": None,
                "pre_n": None,
            },
            id="dev",
        ),
        param(
            "1.2.3+local.123",
            {
                "dev": None,
                "local": "local.123",
                "major": "1",
                "minor": "2",
                "patch": "3",
                "post": None,
                "pre": None,
                "pre_l": None,
                "pre_n": None,
            },
            id="local",
        ),
        param(
            "1.2.3",
            {
                "dev": None,
                "local": None,
                "major": "1",
                "minor": "2",
                "patch": "3",
                "post": None,
                "pre": None,
                "pre_l": None,
                "pre_n": None,
            },
            id="release",
        ),
    ],
)
def test_pep440_pattern(version: str, expected: dict):
    """The PEP440 pattern should match the version string and return the expected dictionary."""
    match = re.search(PEP440_PATTERN, version, re.VERBOSE)
    assert match.groupdict() == expected
