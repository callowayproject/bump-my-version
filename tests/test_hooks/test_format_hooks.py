"""Tests for version placeholder substitution in hook commands."""

from typing import Any, Callable, Dict, List, Optional, Tuple

import pytest

from bumpversion import hooks
from bumpversion.hooks import (
    run_post_commit_hooks,
    run_pre_commit_hooks,
    run_setup_hooks,
)
from tests.conftest import get_config_data


class TestFormatHooks:
    """Tests for the format_hooks helper."""

    @pytest.mark.parametrize(
        ["hooks_list", "context", "expected"],
        [
            pytest.param(
                ["echo {major}.{minor}.{patch}"],
                {"major": "1", "minor": "2", "patch": "3"},
                ["echo 1.2.3"],
                id="known_placeholders",
            ),
            pytest.param(
                ["echo {major} {unknown} {not_a_key}"],
                {"major": "1"},
                ["echo 1 {unknown} {not_a_key}"],
                id="unknown_placeholders",
            ),
            pytest.param(
                ["git log --pretty=format:'%h %s'", "echo {%not_a_key%}"],
                {"major": "1"},
                ["git log --pretty=format:'%h %s'", "echo {%not_a_key%}"],
                id="unrelated_braces",
            ),
            pytest.param(
                ["echo {major}", "script2"],
                {},
                ["echo {major}", "script2"],
                id="empty_context",
            ),
        ],
    )
    def test_format_hooks(self, hooks_list: List[str], context: Dict[str, str], expected: List[str]) -> None:
        """Replace known placeholders and preserve unknown ones."""
        assert hooks.format_hooks(hooks_list, context) == expected


class TestHookContext:
    """Tests for the hook_context helper."""

    @pytest.mark.parametrize(
        ["bump_part", "expect_new_version"],
        [
            pytest.param(None, False, id="current_only"),
            pytest.param("minor", True, id="current_and_new"),
        ],
    )
    def test_hook_context(self, bump_part: Optional[str], expect_new_version: bool) -> None:
        """Build a context with the expected version components."""
        config, _, current_version = get_config_data({"current_version": "1.2.3"})
        new_version = current_version.bump(bump_part) if bump_part else None
        ctx = hooks.hook_context(config, current_version, new_version)

        assert ctx["current_version"] == "1.2.3"
        assert ctx["current_major"] == "1"
        assert ctx["current_minor"] == "2"
        assert ctx["current_patch"] == "3"
        if expect_new_version:
            assert ctx["new_version"] == "1.3.0"
            assert ctx["new_major"] == "1"
            assert ctx["new_minor"] == "3"
            assert ctx["new_patch"] == "0"
        else:
            assert "new_version" not in ctx


SUITE_CASES: List[Tuple[str, Callable, Optional[str], Dict[str, Any], str]] = [
    pytest.param(
        "setup",
        run_setup_hooks,
        None,
        {"setup_hooks": ["echo {current_version} {current_major}"]},
        "echo 1.2.3 1",
        id="setup",
    ),
    pytest.param(
        "pre_commit",
        run_pre_commit_hooks,
        "minor",
        {"pre_commit_hooks": ["echo {new_version} {new_major}.{new_minor}"]},
        "echo 1.3.0 1.3",
        id="pre_commit",
    ),
    pytest.param(
        "post_commit",
        run_post_commit_hooks,
        "patch",
        {"post_commit_hooks": ["git tag release/{new_version}"]},
        "git tag release/1.2.4",
        id="post_commit",
    ),
]


class TestSuiteFormatting:
    """Tests that each hook suite formats commands before running them."""

    @pytest.fixture
    def pre_commit_setup(self, mocker):
        """Return common objects for pre-commit formatting tests."""
        env = {"var": "value"}
        mocker.patch("bumpversion.hooks.get_pre_commit_hook_env", return_value=env)
        config, _, current_version = get_config_data({"current_version": "1.2.3"})
        new_version = current_version.bump("minor")
        return config, current_version, new_version, env

    @pytest.mark.parametrize(["suite_name", "suite_func", "bump_part", "overrides", "expected"], SUITE_CASES)
    def test_suite_formats_version_placeholders(
        self,
        mocker,
        suite_name: str,
        suite_func: Callable,
        bump_part: Optional[str],
        overrides: Dict[str, Any],
        expected: str,
    ) -> None:
        """Each hook suite formats version placeholders before execution."""
        env = {"var": "value"}
        mocker.patch(f"bumpversion.hooks.get_{suite_name}_hook_env", return_value=env)
        mock_run_command = mocker.patch("bumpversion.hooks.run_command")
        mock_run_command.return_value = mocker.MagicMock(stdout="", stderr="", returncode=0)
        config, _, current_version = get_config_data({"current_version": "1.2.3", **overrides})

        args = (
            (config, current_version)
            if bump_part is None
            else (config, current_version, current_version.bump(bump_part))
        )
        suite_func(*args)

        mock_run_command.assert_called_once_with(expected, env)

    def test_formatting_preserves_unknown_braces(self, mocker, pre_commit_setup) -> None:
        """Hooks containing braces that are not version placeholders keep them."""
        config, current_version, new_version, env = pre_commit_setup
        mock_run_command = mocker.patch("bumpversion.hooks.run_command")
        mock_run_command.return_value = mocker.MagicMock(stdout="", stderr="", returncode=0)
        config.pre_commit_hooks = ["git log --pretty=format:'%h'", "echo {not_a_placeholder}"]

        run_pre_commit_hooks(config, current_version, new_version)

        mock_run_command.assert_has_calls(
            [
                mocker.call("git log --pretty=format:'%h'", env),
                mocker.call("echo {not_a_placeholder}", env),
            ]
        )

    def test_formatting_before_shell_syntax_check(self, mocker, pre_commit_setup) -> None:
        """Shell syntax in a formatted hook is still detected and rejected by default."""
        config, current_version, new_version, _env = pre_commit_setup
        config.pre_commit_hooks = ["echo {new_version} | cat"]  # noqa: RUF027

        with pytest.raises(hooks.HookError, match="shell syntax"):
            run_pre_commit_hooks(config, current_version, new_version)

    def test_no_formatting_when_shell_hooks_allowed(self, mocker, pre_commit_setup) -> None:
        """When allow_shell_hooks is True, the original hook command is passed to run_hooks."""
        config, current_version, new_version, env = pre_commit_setup
        config.allow_shell_hooks = True
        config.pre_commit_hooks = ["echo {new_version}"]  # noqa: RUF027
        mock_run_hooks = mocker.patch("bumpversion.hooks.run_hooks")

        run_pre_commit_hooks(config, current_version, new_version)

        mock_run_hooks.assert_called_once_with(
            ["echo {new_version}"],  # noqa: RUF027
            env,
            False,
            allow_shell_hooks=True,
            context=mocker.ANY,
        )


class TestRunHooksFormatting:
    """Tests that run_hooks formats commands according to allow_shell_hooks."""

    @pytest.mark.parametrize(
        ["allow_shell_hooks", "expected_command"],
        [
            pytest.param(False, "echo 1.3.0", id="formats_when_safe"),
            pytest.param(True, "echo {new_version}", id="passes_through_when_shell_allowed"),
        ],
    )
    def test_run_hooks_formatting(self, mocker, allow_shell_hooks: bool, expected_command: str) -> None:
        """run_hooks formats placeholders only when shell hooks are disabled."""
        env = {"var": "value"}
        mock_run_command = mocker.patch("bumpversion.hooks.run_command")
        mock_run_command.return_value = mocker.MagicMock(stdout="", stderr="", returncode=0)
        context = {"new_version": "1.3.0"}

        hooks.run_hooks(["echo {new_version}"], env, allow_shell_hooks=allow_shell_hooks, context=context)

        mock_run_command.assert_called_once_with(expected_command, env)
