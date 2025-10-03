"""Path resolution utilities."""
from pathlib import Path
import os


def get_relative_path(from_path: Path, to_path: Path) -> str:
    """
    Calculate relative path from one file to another.

    Args:
        from_path: Source file path (treated as file even if it doesn't exist yet)
        to_path: Target file path

    Returns:
        Relative path as string suitable for markdown links
    """
    try:
        # Get absolute paths - always use parent of from_path since it's a file
        from_abs = from_path.resolve().parent
        to_abs = to_path.resolve()

        # Calculate relative path
        rel_path = os.path.relpath(to_abs, from_abs)
        return rel_path
    except ValueError:
        # Paths on different drives on Windows, return absolute
        return str(to_path.resolve())
