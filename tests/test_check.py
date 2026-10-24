"""Tests for the bumpversion.check module."""

from pathlib import Path
from textwrap import dedent

from bumpversion.check import do_check, references_current_version
from bumpversion.config import get_configuration
from tests.conftest import inside_dir


def write_config(path: Path, body: str = "", current_version: str = "1.2.3", name: str = ".bumpversion.toml") -> Path:
    """Write a minimal configuration file with the given extra TOML."""
    config_file = path / name
    config_file.write_text(
        dedent(f"""
        [tool.bumpversion]
        current_version = "{current_version}"
        """)
        + dedent(body),
        encoding="utf-8",
    )
    return config_file


class TestDoCheck:
    """Tests for the do_check function."""

    def test_consistent_files_report_no_problems(self, tmp_path: Path):
        """Every configured file containing the current version is consistent."""
        # Arrange
        (tmp_path / "VERSION").write_text("1.2.3\n")
        (tmp_path / "setup.py").write_text("version = '1.2.3'\n")
        config_file = write_config(
            tmp_path,
            '[[tool.bumpversion.files]]\nfilename = "VERSION"\n[[tool.bumpversion.files]]\nfilename = "setup.py"\n',
        )

        # Act
        with inside_dir(tmp_path):
            problems = do_check(get_configuration(config_file))

        # Assert
        assert problems == []

    def test_does_not_modify_files(self, tmp_path: Path):
        """Checking leaves the files untouched."""
        # Arrange
        (tmp_path / "VERSION").write_text("1.2.3\n")
        config_file = write_config(tmp_path, '[[tool.bumpversion.files]]\nfilename = "VERSION"\n')
        before = config_file.read_text()

        # Act
        with inside_dir(tmp_path):
            do_check(get_configuration(config_file))

        # Assert
        assert (tmp_path / "VERSION").read_text() == "1.2.3\n"
        assert config_file.read_text() == before

    def test_reports_every_file_without_the_version(self, tmp_path: Path):
        """All the files with a stale version are reported, not just the first one."""
        # Arrange
        (tmp_path / "VERSION").write_text("1.2.2\n")
        (tmp_path / "setup.py").write_text("version = '1.2.1'\n")
        (tmp_path / "README.md").write_text("Version 1.2.3\n")
        config_file = write_config(
            tmp_path,
            '[[tool.bumpversion.files]]\nfilename = "VERSION"\n'
            '[[tool.bumpversion.files]]\nfilename = "setup.py"\n'
            '[[tool.bumpversion.files]]\nfilename = "README.md"\n',
        )

        # Act
        with inside_dir(tmp_path):
            problems = do_check(get_configuration(config_file))

        # Assert
        assert len(problems) == 2
        assert "VERSION" in problems[0]
        assert "setup.py" in problems[1]

    def test_uses_the_configured_search_pattern(self, tmp_path: Path):
        """A file is searched with its own `search`, so ex. a dated changelog heading can be required."""
        # Arrange
        (tmp_path / "CHANGELOG.md").write_text("## 1.2.3 (unreleased)\n")
        config_file = write_config(
            tmp_path,
            """
            [[tool.bumpversion.files]]
            filename = "CHANGELOG.md"
            search = "^## {current_version} \\\\(\\\\d{{4}}-\\\\d{{2}}-\\\\d{{2}}\\\\)"
            regex = true
            """,
        )

        # Act
        with inside_dir(tmp_path):
            problems_unreleased = do_check(get_configuration(config_file))
            (tmp_path / "CHANGELOG.md").write_text("## 1.2.3 (2026-10-05)\n")
            problems_dated = do_check(get_configuration(config_file))

        # Assert
        assert len(problems_unreleased) == 1
        assert "CHANGELOG.md" in problems_unreleased[0]
        assert problems_dated == []

    def test_respects_ignore_missing_version(self, tmp_path: Path):
        """A file allowed to miss the version is not a problem."""
        # Arrange
        (tmp_path / "VERSION").write_text("nothing here\n")
        config_file = write_config(
            tmp_path, '[[tool.bumpversion.files]]\nfilename = "VERSION"\nignore_missing_version = true\n'
        )

        # Act
        with inside_dir(tmp_path):
            problems = do_check(get_configuration(config_file))

        # Assert
        assert problems == []

    def test_reports_missing_file(self, tmp_path: Path):
        """A configured file that does not exist is a problem, unless it is allowed to be missing."""
        # Arrange
        config_file = write_config(tmp_path, '[[tool.bumpversion.files]]\nfilename = "VERSION"\n')
        ignoring_config_file = write_config(
            tmp_path,
            '[[tool.bumpversion.files]]\nfilename = "VERSION"\nignore_missing_file = true\n',
            name="ignoring.toml",
        )

        # Act
        with inside_dir(tmp_path):
            problems = do_check(get_configuration(config_file))
            ignored_problems = do_check(get_configuration(ignoring_config_file))

        # Assert
        assert len(problems) == 1
        assert "VERSION" in problems[0]
        assert ignored_problems == []

    def test_reports_stale_pep621_version(self, tmp_path: Path):
        """The PEP 621 `project.version`, which bump keeps in sync, must match too."""
        # Arrange
        config_file = write_config(tmp_path, name="pyproject.toml")
        config_file.write_text('[project]\nname = "x"\nversion = "1.2.2"\n' + config_file.read_text())

        # Act
        with inside_dir(tmp_path):
            problems = do_check(get_configuration(config_file))

        # Assert
        assert len(problems) == 1
        assert "1.2.2" in problems[0]

    def test_release_tag_must_match_tag_name(self, tmp_path: Path):
        """The release tag is compared with `tag_name` rendered with the current version."""
        # Arrange
        config_file = write_config(tmp_path)

        # Act
        with inside_dir(tmp_path):
            config = get_configuration(config_file)
            matching = do_check(config, "v1.2.3")
            mismatching = do_check(config, "v1.2.4")

        # Assert
        assert matching == []
        assert len(mismatching) == 1
        assert "'v1.2.4'" in mismatching[0]
        assert "'v1.2.3'" in mismatching[0]

    def test_release_tag_uses_custom_tag_name(self, tmp_path: Path):
        """A custom `tag_name` is honored."""
        # Arrange
        config_file = write_config(tmp_path, 'tag_name = "release-{new_version}"\n')

        # Act
        with inside_dir(tmp_path):
            problems = do_check(get_configuration(config_file), "release-1.2.3")

        # Assert
        assert problems == []


class TestReferencesCurrentVersion:
    """Tests for the references_current_version function."""

    def test_detects_the_version_and_its_components(self):
        """The current version, or any of its components, counts."""
        assert references_current_version("{current_version}")
        assert references_current_version("version = {current_major}.{current_minor}")
        assert references_current_version("^## {current_version} \\(\\d{{4}}\\)")

    def test_version_less_patterns(self):
        """New version fields, escaped braces and plain text do not count."""
        assert not references_current_version("## Unreleased")
        assert not references_current_version("**unreleased**")
        assert not references_current_version("{new_version} {{current_version}}")
