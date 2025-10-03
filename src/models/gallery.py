"""Gallery model - collection of gallery entries."""
from pathlib import Path
from typing import List
from .gallery_entry import GalleryEntry


class Gallery:
    """Collection of all gallery entries in the entries/ directory."""

    def __init__(self, entries_dir: Path):
        """Initialize Gallery with entries directory.

        Args:
            entries_dir: Path to entries/ directory

        Raises:
            FileNotFoundError: If entries_dir does not exist
            NotADirectoryError: If entries_dir is not a directory
        """
        if not entries_dir.exists():
            raise FileNotFoundError(
                f"Gallery directory does not exist: {entries_dir}"
            )

        if not entries_dir.is_dir():
            raise NotADirectoryError(
                f"Gallery path is not a directory: {entries_dir}"
            )

        self.entries_dir = entries_dir
        self.entries: List[GalleryEntry] = []
        self.incomplete_entries: List[str] = []

    def discover_entries(self) -> List[GalleryEntry]:
        """Scan entries_dir for subdirectories and validate each.

        Returns:
            List of valid GalleryEntry objects (sorted alphabetically by name)
        """
        self.entries = []
        self.incomplete_entries = []

        # Scan for subdirectories
        for entry_path in sorted(self.entries_dir.iterdir()):
            if not entry_path.is_dir():
                continue

            # Skip hidden directories
            if entry_path.name.startswith('.'):
                continue

            # Create GalleryEntry instance
            entry = GalleryEntry(
                name=entry_path.name,
                path=entry_path,
                command_script=entry_path / "command.sh",
                plots_dir=entry_path / "plots",
                readme_file=entry_path / "README.md" if (entry_path / "README.md").exists() else None,
                setup_script=entry_path / "setup.sh" if (entry_path / "setup.sh").exists() else None,
            )

            # Validate entry
            is_valid, error_msg = entry.validate()

            if is_valid:
                self.entries.append(entry)
            else:
                self.incomplete_entries.append(f"{entry.name}: {error_msg}")

        return self.entries

    def get_complete_entries(self) -> List[GalleryEntry]:
        """Return only entries that passed validation.

        Returns:
            List of valid GalleryEntry objects
        """
        return self.entries

    def get_warnings(self) -> List[str]:
        """Return warning messages for incomplete entries.

        Returns:
            List of formatted warning strings
        """
        return [
            f"WARNING: Skipping entry '{reason}'"
            for reason in self.incomplete_entries
        ]
