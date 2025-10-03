"""GalleryEntry model - represents a single gallery entry directory."""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple


@dataclass(frozen=True)
class GalleryEntry:
    """Immutable value object representing a gallery entry.

    Represents a single gallery entry directory with its associated files.
    """
    name: str
    path: Path
    command_script: Path
    plots_dir: Path
    readme_file: Optional[Path] = None
    setup_script: Optional[Path] = None

    def validate(self) -> Tuple[bool, Optional[str]]:
        """Validate that the entry has all required files.

        Returns:
            Tuple of (is_valid, error_message)
            - is_valid: True if entry passes validation
            - error_message: None if valid, error description if invalid
        """
        # Check command script exists and is readable
        if not self.command_script.exists():
            return False, "Missing required file command.sh"

        if not self.command_script.is_file():
            return False, "command.sh is not a file"

        try:
            self.command_script.read_text()
        except (PermissionError, OSError) as e:
            return False, f"Cannot read command.sh: {e}"

        # Check plots directory exists
        if not self.plots_dir.exists():
            return False, "plots/ directory does not exist"

        if not self.plots_dir.is_dir():
            return False, "plots/ is not a directory"

        # Check plots directory contains at least one .png file
        png_files = list(self.plots_dir.glob("*.png"))
        if not png_files:
            return False, "plots/ directory empty (no .png files)"

        return True, None
