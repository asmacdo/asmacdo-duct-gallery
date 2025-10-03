"""Integration test for full pipeline execution."""
import subprocess
import os
from pathlib import Path


def test_execute_entries_and_generate_markdown(tmp_path):
    """Test executing gallery entries and generating markdown output."""
    # Setup test gallery directory
    gallery_dir = Path(__file__).parent.parent / "fixtures" / "gallery"
    output_file = tmp_path / "test-output.md"

    # Run con-duct-gallery (will fail until implemented)
    result = subprocess.run(
        ["con-duct-gallery", "-o", str(output_file), "--gallery-dir", str(gallery_dir)],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Command failed: {result.stderr}"
    assert output_file.exists(), "Output file was not created"

    # Verify markdown structure
    content = output_file.read_text()
    assert "## Entry: example-1" in content
    assert "## Entry: example-2" in content
    assert "```bash" in content
    assert "![Plot]" in content
