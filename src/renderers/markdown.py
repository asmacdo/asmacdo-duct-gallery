"""Markdown rendering for gallery output."""
from pathlib import Path
from typing import List

from src.models.gallery_entry import GalleryEntry
from src.path_utils import get_relative_path


def render_entry(entry: GalleryEntry, output_path: Path) -> str:
    """
    Render a single gallery entry as markdown.

    Args:
        entry: GalleryEntry to render
        output_path: Output markdown file path (for relative path calculation)

    Returns:
        Markdown string for the entry
    """
    sections = []

    # Entry heading
    sections.append(f"## Entry: {entry.name}\n")

    # Command code block
    if entry.command_text:
        sections.append(f"```bash\n{entry.command_text}\n```\n")

    # Plot image (if available)
    if entry.plot_path and entry.plot_path.exists():
        rel_path = get_relative_path(output_path, entry.plot_path)
        sections.append(f"![Plot]({rel_path})\n")

    sections.append("---\n")

    return "\n".join(sections)


def render_markdown(entries: List[GalleryEntry], output_path: Path) -> str:
    """
    Render complete markdown document from gallery entries.

    Args:
        entries: List of GalleryEntry instances
        output_path: Output markdown file path

    Returns:
        Complete markdown document as string
    """
    content = ["# Gallery\n"]

    for entry in entries:
        content.append(render_entry(entry, output_path))

    return "\n".join(content)
