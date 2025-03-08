"""Draw.io export script."""

import os.path
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


def get_executable_paths() -> List[str]:
    """Get the Draw.io executable paths for the platform.

    Declared as a function to allow us to use API/environment information
    available only when running under the specified platform.

    Returns:
        All known paths.
    """
    if sys.platform.startswith("darwin"):
        applications = [os.path.expanduser("~/Applications"), "/Applications"]
        drawio_path = os.path.join("draw.io.app", "Contents", "MacOS", "draw.io")
        return [os.path.join(d, drawio_path) for d in applications]
    elif sys.platform.startswith("linux"):
        return ["/opt/draw.io/drawio"]
    elif sys.platform.startswith("win32"):
        program_files = [os.environ["ProgramFiles"]]
        if "ProgramFiles(x86)" in os.environ:
            program_files.append(os.environ["ProgramFiles(x86)"])
        return [os.path.join(d, "draw.io", "draw.io.exe") for d in program_files]
    else:
        return []


def get_drawio_executable(executable_names: Optional[List[str]] = None) -> Optional[str]:
    """Ensure the Draw.io executable path is configured, or guess it.

    Args:
        executable_names: List of executable names to check.

    Returns:
        Final Draw.io executable.
    """
    executable_names = executable_names or ["draw.io", "drawio"]

    for executable_name in executable_names:
        executable = shutil.which(executable_name)
        if executable:
            return executable

    executable_paths = get_executable_paths()

    return next(
        (executable_path for executable_path in executable_paths if os.path.isfile(executable_path)),
        None,
    )


def use_cached_file(source: Path, cache_filename: Path) -> bool:
    """Is the cached copy up to date?

    Args:
        source: Source path.
        cache_filename: Export cache filename.

    Returns:
        True if cache is up to date else False.
    """
    return cache_filename.exists() and cache_filename.stat().st_mtime >= source.stat().st_mtime


def export_file(
    source: Path,
    page_index: int,
    dest: Path,
    export_format: str,
) -> int:
    """Export an individual file.

    Args:
        source: Source path, absolute.
        page_index: Page index, numbered from zero.
        dest: Destination path, within cache.
        export_format: Export format.

    Returns:
        The Draw.io exit status.
    """
    drawio_executable = get_drawio_executable()
    cmd = [
        str(drawio_executable),
        "--export",
        str(source),
        "--page-index",
        str(page_index),
        "--output",
        str(dest),
        "--format",
        export_format,
        "--embed-svg-images",
        "--scale",
        "2",
    ]
    result = subprocess.run(cmd, check=False)  # noqa: S603
    return result.returncode


def export_file_if_needed(source: Path, page_index: int, dest_path: Path) -> None:
    """Export an individual file if needed.

    Args:
        source: Source path, absolute.
        page_index: Page index, numbered from zero.
        dest_path: Destination path.
    """
    if not use_cached_file(source, dest_path):
        export_file(source, page_index, dest_path, "svg")
    else:
        print(f"Using cached file {dest_path}")


if __name__ == "__main__":
    output_files = [
        "creating-a-version-spec.svg",
        "creating-a-version.svg",
        "serializing-a-version-1.svg",
        "serializing-a-version-1-0-0.svg",
        "serializing-a-version-1-2-0.svg",
        "serializing-a-version-1-2-3.svg",
    ]
    source_path = Path(__file__).parent.parent.joinpath("docs/assets/bump-my-version-model.drawio")
    dest_path = Path(__file__).parent.parent.joinpath("docs/assets/")
    for index, filename in enumerate(output_files):
        filepath = dest_path.joinpath(filename)
        export_file_if_needed(source_path, index, filepath)
