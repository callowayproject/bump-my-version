"""Tests for config discovery through parent directories and file path resolution."""

from pathlib import Path

import pytest
from wcmatch import glob

from bumpversion.config import get_configuration
from bumpversion.config.files import find_config_file
from bumpversion.exceptions import ConfigurationError
from bumpversion.utils import find_repo_root
from tests.conftest import inside_dir

CFG = '[tool.bumpversion]\ncurrent_version = "1.0.0"\n'


def make_repo(root: Path, marker: str = ".git") -> Path:
    """Create a fake repo with a nested working directory."""
    (root / marker).mkdir(parents=True)
    sub = root / "pkg" / "sub"
    sub.mkdir(parents=True)
    return sub


class TestFindRepoRoot:
    @pytest.mark.parametrize("marker", [".git", ".hg"])
    def test_finds_root_from_subdir(self, tmp_path: Path, marker: str) -> None:
        sub = make_repo(tmp_path, marker)
        assert find_repo_root(sub) == tmp_path

    def test_git_worktree_file_marker(self, tmp_path: Path) -> None:
        (tmp_path / ".git").write_text("gitdir: elsewhere", encoding="utf-8")
        assert find_repo_root(tmp_path) == tmp_path

    def test_none_outside_repo(self, tmp_path: Path) -> None:
        assert find_repo_root(tmp_path) is None


class TestFindConfigInParents:
    def test_found_in_repo_root_from_subdir(self, tmp_path: Path) -> None:
        sub = make_repo(tmp_path)
        (tmp_path / ".bumpversion.toml").write_text(CFG, encoding="utf-8")
        with inside_dir(sub):
            assert find_config_file() == tmp_path / ".bumpversion.toml"

    def test_nearest_directory_wins(self, tmp_path: Path) -> None:
        sub = make_repo(tmp_path)
        (tmp_path / ".bumpversion.toml").write_text(CFG, encoding="utf-8")
        (sub.parent / "pyproject.toml").write_text(CFG, encoding="utf-8")
        with inside_dir(sub):
            assert find_config_file() == sub.parent / "pyproject.toml"

    def test_does_not_search_above_repo_root(self, tmp_path: Path) -> None:
        repo = tmp_path / "repo"
        sub = make_repo(repo)
        (tmp_path / ".bumpversion.toml").write_text(CFG, encoding="utf-8")
        with inside_dir(sub):
            assert find_config_file() is None

    def test_no_parent_search_outside_repo(self, tmp_path: Path) -> None:
        child = tmp_path / "child"
        child.mkdir()
        (tmp_path / ".bumpversion.toml").write_text(CFG, encoding="utf-8")
        with inside_dir(child):
            assert find_config_file() is None


class TestFileResolution:
    def _config(self, root: Path, files_toml: str) -> Path:
        cfg = root / ".bumpversion.toml"
        cfg.write_text(CFG + files_toml, encoding="utf-8")
        return cfg

    def test_relative_filename_resolved_from_config_dir(self, tmp_path: Path) -> None:
        sub = make_repo(tmp_path)
        cfg = self._config(tmp_path, '[[tool.bumpversion.files]]\nfilename = "pkg/__init__.py"\n')
        with inside_dir(sub):
            conf = get_configuration(cfg)
        assert conf.files[0].filename == str(tmp_path / "pkg" / "__init__.py")

    def test_relative_filename_unchanged_when_cwd_is_config_dir(self, tmp_path: Path) -> None:
        cfg = self._config(tmp_path, '[[tool.bumpversion.files]]\nfilename = "a.py"\n')
        with inside_dir(tmp_path):
            conf = get_configuration(cfg)
        assert conf.files[0].filename == "a.py"

    def test_absolute_filename_used_as_is(self, tmp_path: Path) -> None:
        sub = make_repo(tmp_path)
        absolute = tmp_path / "elsewhere.py"
        cfg = self._config(tmp_path, f'[[tool.bumpversion.files]]\nfilename = "{absolute.as_posix()}"\n')
        with inside_dir(sub):
            conf = get_configuration(cfg)
        assert conf.files[0].filename == absolute.as_posix()

    def test_relative_glob_and_exclude_resolved_from_config_dir(self, tmp_path: Path) -> None:
        sub = make_repo(tmp_path)
        (tmp_path / "pkg" / "a.py").write_text("1.0.0", encoding="utf-8")
        (tmp_path / "pkg" / "skip.py").write_text("1.0.0", encoding="utf-8")
        cfg = self._config(tmp_path, '[[tool.bumpversion.files]]\nglob = "pkg/*.py"\nglob_exclude = ["pkg/skip.py"]\n')
        with inside_dir(sub):
            conf = get_configuration(cfg)
            assert list(conf.resolved_filemap) == [str(tmp_path / "pkg" / "a.py")]

    def test_repo_root_placeholder(self, tmp_path: Path) -> None:
        sub = make_repo(tmp_path)
        cfg = self._config(tmp_path, '[[tool.bumpversion.files]]\nfilename = "{repo_root}/lib/__init__.py"\n')
        with inside_dir(sub):
            conf = get_configuration(cfg)
        assert Path(conf.files[0].filename) == tmp_path / "lib" / "__init__.py"

    def test_repo_root_placeholder_in_glob(self, tmp_path: Path) -> None:
        sub = make_repo(tmp_path)
        cfg = self._config(tmp_path, '[[tool.bumpversion.files]]\nglob = "{repo_root}/lib/*.py"\n')
        with inside_dir(sub):
            conf = get_configuration(cfg)
        assert conf.files[0].glob == f"{glob.escape(tmp_path.as_posix())}/lib/*.py"

    def test_repo_root_placeholder_outside_repo_errors(self, tmp_path: Path) -> None:
        cfg = self._config(tmp_path, '[[tool.bumpversion.files]]\nfilename = "{repo_root}/a.py"\n')
        with inside_dir(tmp_path), pytest.raises(ConfigurationError, match="repo_root"):
            get_configuration(cfg)
