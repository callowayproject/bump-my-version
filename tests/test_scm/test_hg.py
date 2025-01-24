import shutil
from pathlib import Path

import pytest

from bumpversion.scm.hg import Mercurial
from bumpversion.scm.models import SCMConfig
from tests.conftest import inside_dir


def test_hg_is_not_available(tmp_path: Path, scm_config: SCMConfig) -> None:
    """Should return false if it is not a mercurial repo."""
    with inside_dir(tmp_path):
        assert not Mercurial(scm_config).is_available()


@pytest.mark.skipif(not shutil.which("hg"), reason="Mercurial is not available.")
def test_hg_is_available(hg_repo: Path, scm_config: SCMConfig) -> None:
    """Should return false if it is not a mercurial repo."""
    with inside_dir(hg_repo):
        assert Mercurial(scm_config).is_available()
