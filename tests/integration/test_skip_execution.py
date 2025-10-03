"""Integration tests for skip execution mode."""
import subprocess
import os
from pathlib import Path
import shutil


def test_skip_execution_mode(tmp_path):
    """Test that entry without command.sh skips execution and uses existing logs."""
    # Create test gallery with skip-execution-example
    test_gallery = tmp_path / "test_gallery"
    test_gallery.mkdir()

    # Copy skip-execution fixture
    fixture_dir = Path(__file__).parent.parent / "fixtures" / "gallery" / "skip-execution-example"
    skip_entry = test_gallery / "skip-execution-example"
    shutil.copytree(fixture_dir, skip_entry)

    # Run from tmp_path so README.md is written there
    result = subprocess.run(
        ["con-duct-gallery", "--gallery-dir", str(test_gallery)],
        capture_output=True,
        text=True,
        cwd=str(tmp_path)
    )

    # Should succeed
    assert result.returncode == 0, f"Command failed: {result.stderr}"

    # Check output
    output_file = tmp_path / "README.md"
    assert output_file.exists(), "README.md was not created"

    content = output_file.read_text()
    assert "skip-execution-example" in content, "Skip execution entry not in output"

    # Verify plot was generated
    plot_file = skip_entry / "plots" / "usage.png"
    assert plot_file.exists(), "Plot was not generated for skip mode entry"

    # Check that skip message appeared in output
    assert "Skipping execution (no command.sh)" in result.stdout, "Skip message not in output"


def test_mixed_mode_gallery(tmp_path):
    """Test gallery with both execute mode and skip mode entries."""
    # Create test gallery
    test_gallery = tmp_path / "test_gallery"
    test_gallery.mkdir()

    # Copy both fixtures
    fixtures_base = Path(__file__).parent.parent / "fixtures" / "gallery"

    # Copy execute mode entry (example-1)
    exec_entry = test_gallery / "example-1"
    shutil.copytree(fixtures_base / "example-1", exec_entry)

    # Copy skip mode entry
    skip_entry = test_gallery / "skip-execution-example"
    shutil.copytree(fixtures_base / "skip-execution-example", skip_entry)

    # Run from tmp_path
    result = subprocess.run(
        ["con-duct-gallery", "--gallery-dir", str(test_gallery)],
        capture_output=True,
        text=True,
        cwd=str(tmp_path)
    )

    # Should succeed
    assert result.returncode == 0, f"Command failed: {result.stderr}"

    # Check output includes both entries
    output_file = tmp_path / "README.md"
    assert output_file.exists(), "README.md was not created"

    content = output_file.read_text()
    assert "example-1" in content, "Execute mode entry not in output"
    assert "skip-execution-example" in content, "Skip mode entry not in output"

    # Verify both plots generated
    assert (exec_entry / "plots" / "usage.png").exists(), "Execute mode plot not generated"
    assert (skip_entry / "plots" / "usage.png").exists(), "Skip mode plot not generated"


def test_skip_mode_error_handling(tmp_path):
    """Test error handling for skip mode entries with missing logs."""
    # Create test gallery
    test_gallery = tmp_path / "test_gallery"
    test_gallery.mkdir()

    # Create entry without command.sh and without logs (should fail)
    broken_entry = test_gallery / "broken-skip"
    broken_entry.mkdir()

    # Create a working entry so the command doesn't fail entirely
    fixtures_base = Path(__file__).parent.parent / "fixtures" / "gallery"
    working_entry = test_gallery / "example-1"
    shutil.copytree(fixtures_base / "example-1", working_entry)

    # Run from tmp_path
    result = subprocess.run(
        ["con-duct-gallery", "--gallery-dir", str(test_gallery)],
        capture_output=True,
        text=True,
        cwd=str(tmp_path)
    )

    # Should succeed overall (one entry works)
    assert result.returncode == 0, f"Command failed: {result.stderr}"

    # Check that warning was issued for broken entry
    assert "broken-skip" in result.stderr and "skipped" in result.stderr, \
        "Warning not issued for broken skip mode entry"

    # Check that working entry still processed
    output_file = tmp_path / "README.md"
    assert output_file.exists(), "README.md was not created"

    content = output_file.read_text()
    assert "example-1" in content, "Working entry not in output"
    assert "broken-skip" not in content, "Broken entry should not be in output"
