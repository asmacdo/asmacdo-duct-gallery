"""Plot generation from duct usage.json files."""
import subprocess
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def generate_plot(usage_json: Path, output_dir: Path) -> Optional[Path]:
    """
    Generate plot from usage.json using con-duct.

    Args:
        usage_json: Path to usage.json file from duct execution
        output_dir: Directory to save plot

    Returns:
        Path to generated plot, or None if generation failed
    """
    if not usage_json.exists():
        logger.error(f"usage.json not found: {usage_json}")
        return None

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    plot_path = output_dir / "usage.png"

    try:
        # Use con-duct plot command to generate visualization
        result = subprocess.run(
            ["con-duct", "plot", str(usage_json), "-o", str(plot_path)],
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode == 0 and plot_path.exists():
            logger.info(f"Generated plot: {plot_path}")
            return plot_path
        else:
            logger.error(f"con-duct plot failed: {result.stderr}")
            return None

    except subprocess.TimeoutExpired:
        logger.error("Plot generation timed out")
        return None
    except Exception as e:
        logger.error(f"Plot generation failed: {e}")
        return None
