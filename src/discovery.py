"""Gallery entry discovery logic."""
from pathlib import Path
from typing import List
import logging

from src.models.gallery_entry import GalleryEntry

logger = logging.getLogger(__name__)


def discover_entries(gallery_dir: Path) -> List[GalleryEntry]:
    """
    Scan gallery directory and discover valid entries.

    Args:
        gallery_dir: Path to gallery directory

    Returns:
        List of validated GalleryEntry instances
    """
    if not gallery_dir.exists() or not gallery_dir.is_dir():
        logger.error(f"Gallery directory not found: {gallery_dir}")
        return []

    entries = []
    for entry_dir in sorted(gallery_dir.iterdir()):
        if not entry_dir.is_dir():
            continue

        entry = GalleryEntry.from_directory(entry_dir)
        if entry.validate():
            entries.append(entry)
            logger.info(f"Discovered entry: {entry.name}")
        else:
            logger.warning(f"Skipping invalid entry: {entry.name}")

    return entries
