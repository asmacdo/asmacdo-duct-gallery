"""Gallery entry model."""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class GalleryEntry:
    """Represents a single gallery entry to be executed and rendered."""

    name: str
    path: Path
    setup_script: Path
    command_script: Path
    command_text: str = ""
    usage_json: Optional[Path] = None
    plot_path: Optional[Path] = None
    metadata: dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

    @classmethod
    def from_directory(cls, entry_dir: Path) -> "GalleryEntry":
        """Create a GalleryEntry from a directory path."""
        return cls(
            name=entry_dir.name,
            path=entry_dir,
            setup_script=entry_dir / "setup.sh",
            command_script=entry_dir / "command.sh",
        )

    @property
    def has_command_script(self) -> bool:
        """Returns True if command.sh exists in entry directory."""
        return self.command_script.exists()

    @property
    def skip_execution(self) -> bool:
        """Returns True if execution should be skipped (no command.sh)."""
        return not self.has_command_script

    def validate(self) -> bool:
        """Validate that required files exist and are executable."""
        if not self.path.is_dir():
            return False
        if not self.setup_script.exists() or not self.setup_script.is_file():
            return False
        if not self.command_script.exists() or not self.command_script.is_file():
            return False
        return True
