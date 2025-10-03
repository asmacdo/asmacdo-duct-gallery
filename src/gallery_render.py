"""Main CLI entrypoint for con-duct-gallery."""
import argparse
import logging
import sys
from pathlib import Path

from src.discovery import discover_entries
from src.executor import execute_script, read_command_text
from src.plot_generator import generate_plot
from src.renderers.markdown import render_markdown

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)


def validate_output_path(output_path: Path) -> bool:
    """Validate that output path is writable."""
    parent = output_path.parent
    if not parent.exists():
        logger.error(f"Error: Output path invalid - parent directory does not exist: {parent}")
        return False
    if not parent.is_dir():
        logger.error(f"Error: Parent path is not a directory: {parent}")
        return False
    return True


def process_entry(entry, output_path):
    """Process a single gallery entry: execute scripts, generate plot, prepare for rendering."""
    logger.info(f"Executing entry: {entry.name}")

    # Run setup.sh
    logger.info("  Running setup.sh...")
    success, stdout, stderr = execute_script(entry.setup_script, entry.path)
    if not success:
        logger.warning(f"Warning: Entry '{entry.name}' skipped - setup.sh failed with exit code 1")
        return False

    # Run command.sh
    logger.info("  Running command.sh...")
    success, stdout, stderr = execute_script(entry.command_script, entry.path)
    if not success:
        logger.warning(f"Warning: Entry '{entry.name}' skipped - command.sh failed")
        return False

    # Read command text for display
    entry.command_text = read_command_text(entry.command_script)

    # Find usage.json - duct creates files with prefix, need to find actual file
    # Look for info.json to get the correct path
    import json
    import glob

    info_files = list(entry.path.glob(".duct/*info.json"))
    if not info_files:
        logger.warning(f"Warning: Entry '{entry.name}' skipped - no duct info.json found")
        return False

    try:
        info_data = json.loads(info_files[0].read_text())
        usage_path = info_data.get("output_paths", {}).get("usage")
        if usage_path:
            entry.usage_json = entry.path / usage_path
        else:
            logger.warning(f"Warning: Entry '{entry.name}' skipped - usage path not in info.json")
            return False
    except Exception as e:
        logger.warning(f"Warning: Entry '{entry.name}' skipped - failed to parse info.json: {e}")
        return False

    if not entry.usage_json.exists():
        logger.warning(f"Warning: Entry '{entry.name}' skipped - usage.json not found at {entry.usage_json}")
        return False

    # Generate plot
    logger.info("  Generating plot...")
    plots_dir = entry.path / "plots"
    entry.plot_path = generate_plot(entry.usage_json, plots_dir)
    if not entry.plot_path:
        logger.warning(f"Warning: Entry '{entry.name}' skipped - plot generation failed")
        return False

    return True


def main():
    """Main entry point for con-duct-gallery CLI."""
    parser = argparse.ArgumentParser(description="Generate gallery markdown from duct executions")
    parser.add_argument("-o", "--output", required=True, type=Path, help="Output markdown file path")
    parser.add_argument("--gallery-dir", type=Path, default=Path("./gallery"), help="Gallery directory to scan")

    args = parser.parse_args()

    # Validate output path
    if not validate_output_path(args.output):
        sys.exit(1)

    # Discover entries
    logger.info(f"Scanning gallery directory: {args.gallery_dir}")
    entries = discover_entries(args.gallery_dir)

    if not entries:
        logger.error(f"Error: No valid gallery entries found in {args.gallery_dir}")
        sys.exit(1)

    logger.info(f"Found {len(entries)} entries")

    # Process each entry
    successful_entries = []
    for entry in entries:
        if process_entry(entry, args.output):
            successful_entries.append(entry)

    if not successful_entries:
        logger.error("Error: No entries were successfully processed")
        sys.exit(1)

    # Generate markdown
    markdown_content = render_markdown(successful_entries, args.output)

    # Write output
    args.output.write_text(markdown_content)
    logger.info(f"Generated markdown: {args.output} ({len(successful_entries)} entries)")


if __name__ == "__main__":
    main()
