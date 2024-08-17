"""Implementation of the hook interface."""

import datetime
import os
import subprocess
from typing import Dict, Optional

from bumpversion.config.models import Config
from bumpversion.ui import get_indented_logger

PREFIX = "BVHOOK_"

logger = get_indented_logger(__name__)


def run_command(script: str, environment: Optional[dict] = None) -> subprocess.CompletedProcess:
    """Runs command-line programs using the shell."""
    if not isinstance(script, str):
        raise TypeError(f"`script` must be a string, not {type(script)}")
    if environment and not isinstance(environment, dict):
        raise TypeError(f"`environment` must be a dict, not {type(environment)}")
    return subprocess.run(script, env=environment, encoding="utf-8", shell=True, text=True, capture_output=True)


def base_env(config: Config) -> Dict[str, str]:
    """Provide the base environment variables."""
    return {
        f"{PREFIX}NOW": datetime.datetime.now().isoformat(),
        f"{PREFIX}UTCNOW": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        **os.environ,
        **scm_env(config),
    }


def scm_env(config: Config) -> Dict[str, str]:
    """Provide the scm environment variables."""
    scm = config.scm_info
    return {
        f"{PREFIX}COMMIT_SHA": scm.commit_sha or "",
        f"{PREFIX}DISTANCE_TO_LATEST_TAG": str(scm.distance_to_latest_tag) or "0",
        f"{PREFIX}IS_DIRTY": str(scm.dirty),
        f"{PREFIX}BRANCH_NAME": scm.branch_name or "",
        f"{PREFIX}SHORT_BRANCH_NAME": scm.short_branch_name or "",
        f"{PREFIX}CURRENT_VERSION": scm.current_version or "",
        f"{PREFIX}CURRENT_TAG": scm.current_tag or "",
    }


def current_version_env(config: Config) -> Dict[str, str]:
    """Provide the current version environment variables."""
    version_str = config.current_version
    version = config.version_config.parse(version_str)

    return {f"{PREFIX}CURRENT_{part.upper()}": version[part].value for part in version}


def setup_hook_env(config: Config) -> Dict[str, str]:
    """Provide the environment dictionary for `setup_hook`s."""
    return {**base_env(config), **scm_env(config), **current_version_env(config)}


def run_setup_hooks(config: Config) -> None:
    """Run the setup hooks."""
    env = setup_hook_env(config)
    if config.setup_hooks:
        logger.info("Running setup hooks:")
    else:
        logger.info("No setup hooks defined")
        return

    logger.indent()
    for script in config.setup_hooks:
        logger.debug(f"Running {script!r}")
        logger.indent()
        result = run_command(script, env)
        logger.debug(result.stdout)
        logger.debug(result.stderr)
        logger.debug(f"Exited with {result.returncode}")
        logger.indent()
    logger.dedent()


def run_pre_commit_hooks(config: Config) -> None:
    """Run the pre-commit hooks."""
    pass


def run_post_commit_hooks(config: Config) -> None:
    """Run the post-commit hooks."""
    pass
