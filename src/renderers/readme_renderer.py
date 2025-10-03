"""README renderer - generates gallery README from entries."""
from pathlib import Path
from typing import List
from ..models.gallery import Gallery
from ..models.readme_section import READMESection


def generate_readme(gallery: Gallery, output_path: Path) -> None:
    """Generate README.md from gallery entries.

    Args:
        gallery: Gallery instance with discovered entries
        output_path: Path where README.md should be written

    Raises:
        PermissionError: If output_path is not writable
        OSError: If write operation fails
    """
    sections: List[READMESection] = []

    # Process each complete entry
    for entry in gallery.get_complete_entries():
        # Read command.sh content
        command_content = entry.command_script.read_text()

        # Find first .png file in plots/ directory
        png_files = sorted(entry.plots_dir.glob("*.png"))
        if not png_files:
            # This shouldn't happen since validation checks for png files
            # but handle defensively
            continue

        first_plot = png_files[0]

        # Calculate relative path from output_path to plot file
        try:
            plot_relative_path = first_plot.relative_to(output_path.parent)
        except ValueError:
            # If relative path fails, use absolute path
            # (shouldn't happen in normal usage)
            plot_relative_path = first_plot

        # Create README section
        section = READMESection(
            entry_name=entry.name,
            command_content=command_content,
            plot_path=str(plot_relative_path),
        )
        sections.append(section)

    # Render template
    readme_content = "# Gallery\n\n"

    for section in sections:
        readme_content += section.render()
        readme_content += "\n"

    # Write to output file
    output_path.write_text(readme_content)
