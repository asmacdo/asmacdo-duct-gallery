"""Path resolution utilities."""
from pathlib import Path
import os


def get_relative_path(from_path: Path, to_path: Path) -> str:
    """
    Calculate relative path from one file to another.

    Args:
        from_path: Source file path
        to_path: Target file path

    Returns:
        Relative path as string suitable for markdown links
    """
    try:
        # Get absolute paths
        from_abs = from_path.resolve().parent if from_path.is_file() else from_path.resolve()
        to_abs = to_path.resolve()

        # Calculate relative path
        rel_path = os.path.relpath(to_abs, from_abs)
        return rel_path
    except ValueError:
        # Paths on different drives on Windows, return absolute
        return str(to_path.resolve())
