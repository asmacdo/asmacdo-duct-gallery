"""Script execution utilities."""
import subprocess
import logging
from pathlib import Path
from typing import Tuple

logger = logging.getLogger(__name__)


def execute_script(script_path: Path, cwd: Path) -> Tuple[bool, str, str]:
    """
    Execute a shell script and capture output.

    Args:
        script_path: Path to script to execute
        cwd: Working directory for execution

    Returns:
        Tuple of (success: bool, stdout: str, stderr: str)
    """
    try:
        result = subprocess.run(
            [str(script_path.resolve())],
            cwd=str(cwd.resolve()),
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
        )
        success = result.returncode == 0
        return success, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        logger.error(f"Script timed out: {script_path}")
        return False, "", "Script execution timed out"
    except Exception as e:
        logger.error(f"Script execution failed: {e}")
        return False, "", str(e)


def read_command_text(command_script: Path) -> str:
    """Read the command text from command.sh for display in markdown."""
    try:
        return command_script.read_text().strip()
    except Exception as e:
        logger.error(f"Failed to read command text: {e}")
        return ""
