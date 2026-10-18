"""Tests for config discovery through parent directories and file path resolution."""

import sys
from pathlib import Path

import pytest
from pydantic import ValidationError
from wcmatch import glob

from bumpversion.config import get_configuration
from bumpversion.config.files import find_config_file
from bumpversion.config.files_legacy import update_ini_config_file
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
    """Tests for find_repo_root."""

    @pytest.mark.parametrize("marker", [".git", ".hg"])
    def test_finds_root_from_subdir(self, tmp_path: Path, marker: str) -> None:
        """Finds root from subdir."""
        sub = make_repo(tmp_path, marker)
        assert find_repo_root(sub) == tmp_path

    def test_git_worktree_file_marker(self, tmp_path: Path) -> None:
        """Git worktree file marker."""
        (tmp_path / ".git").write_text("gitdir: elsewhere", encoding="utf-8")
        assert find_repo_root(tmp_path) == tmp_path

    def test_none_outside_repo(self, tmp_path: Path) -> None:
        """None outside repo."""
        assert find_repo_root(tmp_path) is None


class TestFindConfigInParents:
    """Tests for config discovery through parent directories."""

    def test_found_in_repo_root_from_subdir(self, tmp_path: Path) -> None:
        """Found in repo root from subdir."""
        sub = make_repo(tmp_path)
        (tmp_path / ".bumpversion.toml").write_text(CFG, encoding="utf-8")
        with inside_dir(sub):
            assert find_config_file() == tmp_path / ".bumpversion.toml"

    def test_nearest_directory_wins(self, tmp_path: Path) -> None:
        """Nearest directory wins."""
        sub = make_repo(tmp_path)
        (tmp_path / ".bumpversion.toml").write_text(CFG, encoding="utf-8")
        (sub.parent / "pyproject.toml").write_text(CFG, encoding="utf-8")
        with inside_dir(sub):
            assert find_config_file() == sub.parent / "pyproject.toml"

    def test_does_not_search_above_repo_root(self, tmp_path: Path) -> None:
        """Does not search above repo root."""
        repo = tmp_path / "repo"
        sub = make_repo(repo)
        (tmp_path / ".bumpversion.toml").write_text(CFG, encoding="utf-8")
        with inside_dir(sub):
            assert find_config_file() is None

    def test_no_parent_search_outside_repo(self, tmp_path: Path) -> None:
        """No parent search outside repo."""
        child = tmp_path / "child"
        child.mkdir()
        (tmp_path / ".bumpversion.toml").write_text(CFG, encoding="utf-8")
        with inside_dir(child):
            assert find_config_file() is None


class TestFileResolution:
    """Tests for resolving file paths relative to the config directory."""

    def _config(self, root: Path, files_toml: str) -> Path:
        """Write a config file containing the given files TOML."""
        cfg = root / ".bumpversion.toml"
        cfg.write_text(CFG + files_toml, encoding="utf-8")
        return cfg

    def test_relative_filename_resolved_from_config_dir(self, tmp_path: Path) -> None:
        """Relative filename resolved from config dir."""
        sub = make_repo(tmp_path)
        cfg = self._config(tmp_path, '[[tool.bumpversion.files]]\nfilename = "pkg/__init__.py"\n')
        with inside_dir(sub):
            conf = get_configuration(cfg)
        assert Path(conf.files[0].filename) == tmp_path / "pkg" / "__init__.py"

    def test_relative_filename_unchanged_when_cwd_is_config_dir(self, tmp_path: Path) -> None:
        """Relative filename unchanged when cwd is config dir."""
        cfg = self._config(tmp_path, '[[tool.bumpversion.files]]\nfilename = "a.py"\n')
        with inside_dir(tmp_path):
            conf = get_configuration(cfg)
        assert conf.files[0].filename == "a.py"

    def test_absolute_filename_used_as_is(self, tmp_path: Path) -> None:
        """Absolute filename used as is."""
        sub = make_repo(tmp_path)
        absolute = tmp_path / "elsewhere.py"
        cfg = self._config(tmp_path, f'[[tool.bumpversion.files]]\nfilename = "{absolute.as_posix()}"\n')
        with inside_dir(sub):
            conf = get_configuration(cfg)
        assert conf.files[0].filename == absolute.as_posix()

    def test_relative_glob_and_exclude_resolved_from_config_dir(self, tmp_path: Path) -> None:
        """Relative glob and exclude resolved from config dir."""
        sub = make_repo(tmp_path)
        (tmp_path / "pkg" / "a.py").write_text("1.0.0", encoding="utf-8")
        (tmp_path / "pkg" / "skip.py").write_text("1.0.0", encoding="utf-8")
        cfg = self._config(tmp_path, '[[tool.bumpversion.files]]\nglob = "pkg/*.py"\nglob_exclude = ["pkg/skip.py"]\n')
        with inside_dir(sub):
            conf = get_configuration(cfg)
            assert list(conf.resolved_filemap) == [str(tmp_path / "pkg" / "a.py")]

    def test_repo_root_placeholder(self, tmp_path: Path) -> None:
        """Repo root placeholder."""
        sub = make_repo(tmp_path)
        cfg = self._config(tmp_path, '[[tool.bumpversion.files]]\nfilename = "{repo_root}/lib/__init__.py"\n')
        with inside_dir(sub):
            conf = get_configuration(cfg)
        assert Path(conf.files[0].filename) == tmp_path / "lib" / "__init__.py"

    def test_repo_root_placeholder_in_glob(self, tmp_path: Path) -> None:
        """Repo root placeholder in glob."""
        sub = make_repo(tmp_path)
        cfg = self._config(tmp_path, '[[tool.bumpversion.files]]\nglob = "{repo_root}/lib/*.py"\n')
        with inside_dir(sub):
            conf = get_configuration(cfg)
        assert conf.files[0].glob == f"{glob.escape(tmp_path.as_posix())}/lib/*.py"

    def test_repo_root_placeholder_outside_repo_errors(self, tmp_path: Path) -> None:
        """Repo root placeholder outside repo errors."""
        cfg = self._config(tmp_path, '[[tool.bumpversion.files]]\nfilename = "{repo_root}/a.py"\n')
        with inside_dir(tmp_path), pytest.raises(ConfigurationError, match="repo_root"):
            get_configuration(cfg)


class TestCliPathsAndGaps:
    """Tests for CLI path handling and edge cases in path resolution."""

    def _config(self, root: Path, files_toml: str) -> Path:
        """Write a config file containing the given files TOML."""
        cfg = root / ".bumpversion.toml"
        cfg.write_text(CFG + files_toml, encoding="utf-8")
        return cfg

    def test_cli_relative_path_matches_configured_absolute(self, tmp_path: Path) -> None:
        """Cli relative path matches configured absolute."""
        sub = make_repo(tmp_path)
        (tmp_path / "pkg" / "a.py").write_text("1.0.0", encoding="utf-8")
        cfg = self._config(tmp_path, '[[tool.bumpversion.files]]\nfilename = "pkg/a.py"\n')
        with inside_dir(sub):
            conf = get_configuration(cfg)
            conf.excluded_paths = list(conf.resolved_filemap)
            conf.add_files(["../a.py"])
            conf.included_paths = ["../a.py"]
            names = {f.filename for f in conf.files_to_modify}
        # the CLI spelling of an already-configured file is not added again
        assert names == {(tmp_path / "pkg" / "a.py").as_posix()}

    def test_bang_filename_is_not_treated_as_negation(self, tmp_path: Path) -> None:
        """Bang filename is not treated as negation."""
        sub = make_repo(tmp_path)
        cfg = self._config(tmp_path, '[[tool.bumpversion.files]]\nfilename = "!weird.py"\n')
        with inside_dir(sub):
            conf = get_configuration(cfg)
        assert conf.files[0].filename == (tmp_path / "!weird.py").as_posix()

    def test_cli_path_not_matching_stays_excluded(self, tmp_path: Path) -> None:
        """Cli path not matching stays excluded."""
        sub = make_repo(tmp_path)
        cfg = self._config(tmp_path, '[[tool.bumpversion.files]]\nfilename = "pkg/a.py"\n')
        with inside_dir(sub):
            conf = get_configuration(cfg)
            conf.excluded_paths = list(conf.resolved_filemap)
            conf.add_files(["other.py"])
            conf.included_paths = ["other.py"]
            assert [f.filename for f in conf.files_to_modify] == ["other.py"]

    def test_symlinked_cwd(self, tmp_path: Path) -> None:
        """Symlinked cwd."""
        real = tmp_path / "real"
        make_repo(real)
        link = tmp_path / "link"
        link.symlink_to(real)
        cfg = self._config(real, '[[tool.bumpversion.files]]\nfilename = "pkg/a.py"\n')
        with inside_dir(link / "pkg" / "sub"):
            conf = get_configuration(link / ".bumpversion.toml")
            assert find_config_file() == cfg.resolve()
            conf.excluded_paths = list(conf.resolved_filemap)
            conf.add_files(["../a.py"])
            conf.included_paths = ["../a.py"]
            assert [f.filename for f in conf.files_to_modify] == [(real.resolve() / "pkg" / "a.py").as_posix()]

    def test_symlinked_config_file(self, tmp_path: Path) -> None:
        """Symlinked config file."""
        real = tmp_path / "real"
        sub = make_repo(real)
        cfg = self._config(real, '[[tool.bumpversion.files]]\nfilename = "pkg/a.py"\n')
        link = tmp_path / "elsewhere.toml"
        link.symlink_to(cfg)
        with inside_dir(sub):
            conf = get_configuration(link)
        # relative names are anchored at the real config's directory
        assert conf.files[0].filename == (real.resolve() / "pkg" / "a.py").as_posix()

    def test_ini_config_found_in_parent(self, tmp_path: Path) -> None:
        """Ini config found in parent."""
        sub = make_repo(tmp_path)
        cfg = tmp_path / ".bumpversion.cfg"
        cfg.write_text("[bumpversion]\ncurrent_version = 1.0.0\n\n[bumpversion:file:pkg/a.py]\n", encoding="utf-8")
        with inside_dir(sub):
            assert find_config_file() == cfg
            conf = get_configuration(cfg)
            assert conf.files[0].filename == (tmp_path / "pkg" / "a.py").as_posix()
            update_ini_config_file(cfg, "1.0.0", "1.0.1")
        assert "current_version = 1.0.1" in cfg.read_text(encoding="utf-8")

    def test_glob_exclude_negation_keeps_prefix(self, tmp_path: Path) -> None:
        """Glob exclude negation keeps prefix."""
        sub = make_repo(tmp_path)
        cfg = self._config(tmp_path, '[[tool.bumpversion.files]]\nglob = "pkg/*.py"\nglob_exclude = ["!pkg/a.py"]\n')
        with inside_dir(sub):
            conf = get_configuration(cfg)
        assert conf.files[0].glob_exclude == (f"!{glob.escape(tmp_path.as_posix())}/pkg/a.py",)

    @pytest.mark.skipif(sys.platform == "win32", reason="'|' is not a valid Windows path character")
    def test_pipe_in_repo_path_does_not_split_glob(self, tmp_path: Path) -> None:
        """Pipe in repo path does not split glob."""
        root = tmp_path / "a|b"
        sub = make_repo(root)
        (root / "pkg" / "x.py").write_text("1.0.0", encoding="utf-8")
        cfg = self._config(root, '[[tool.bumpversion.files]]\nglob = "pkg/*.py"\n')
        with inside_dir(sub):
            conf = get_configuration(cfg)
            assert list(conf.resolved_filemap) == [str(root / "pkg" / "x.py")]

    @pytest.mark.parametrize("entry", ["files = [1, 'x']", "files = [[]]"])
    def test_non_mapping_files_entries_rejected(self, tmp_path: Path, entry: str) -> None:
        """Non mapping files entries rejected."""
        cfg = tmp_path / ".bumpversion.toml"
        cfg.write_text(CFG.replace("[tool.bumpversion]\n", "[tool.bumpversion]\n" + entry + "\n"), encoding="utf-8")
        with inside_dir(tmp_path), pytest.raises(ConfigurationError, match="files"):
            get_configuration(cfg)

    @pytest.mark.parametrize("line", ["filename = 1", "glob = 1", "glob = ['a']"])
    def test_non_string_filename_or_glob_rejected(self, tmp_path: Path, line: str) -> None:
        """Non string filename or glob rejected."""
        cfg = tmp_path / ".bumpversion.toml"
        cfg.write_text(CFG + f"[[tool.bumpversion.files]]\n{line}\n", encoding="utf-8")
        with inside_dir(tmp_path), pytest.raises(ValidationError):
            get_configuration(cfg)

    def test_windows_and_posix_absolute_paths_not_rebased(self, tmp_path: Path) -> None:
        """Windows and posix absolute paths not rebased."""
        sub = make_repo(tmp_path)
        cfg = self._config(
            tmp_path,
            '[[tool.bumpversion.files]]\nfilename = "/abs/a.py"\n'
            '[[tool.bumpversion.files]]\nfilename = "C:\\\\abs\\\\b.py"\n',
        )
        with inside_dir(sub):
            conf = get_configuration(cfg)
        assert [f.filename for f in conf.files] == ["/abs/a.py", "C:\\abs\\b.py"]
