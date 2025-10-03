"""CLI entry point for con-duct-gallery command."""
import argparse
import sys
from pathlib import Path
from .models.gallery import Gallery
from .renderers.readme_renderer import generate_readme


def main():
    """Main CLI entry point for con-duct-gallery."""
    parser = argparse.ArgumentParser(
        description="Generate gallery README from entries in the entries/ directory"
    )

    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("README.md"),
        help="Path to output README file (default: README.md)"
    )

    parser.add_argument(
        "--gallery-dir",
        type=Path,
        default=Path("entries"),
        help="Path to gallery entries directory (default: entries/)"
    )

    args = parser.parse_args()

    try:
        # Create Gallery instance (validates directory exists)
        gallery = Gallery(args.gallery_dir)

        # Discover entries
        gallery.discover_entries()

        # Print warnings for incomplete entries
        warnings = gallery.get_warnings()
        for warning in warnings:
            print(warning, file=sys.stdout)

        # Generate README
        generate_readme(gallery, args.output)

        # Print success message
        entry_count = len(gallery.get_complete_entries())
        print(f"Generated README with {entry_count} entries")

        sys.exit(0)

    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    except NotADirectoryError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    except (PermissionError, OSError) as e:
        print(f"ERROR: Cannot write to output file: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
