"""Unit tests for GalleryEntry model."""
from pathlib import Path
import tempfile
import pytest
from src.models.gallery_entry import GalleryEntry


def test_has_command_script_returns_true_when_exists(tmp_path):
    """Test has_command_script property returns True when command.sh exists."""
    # Create entry with command.sh
    entry_dir = tmp_path / "test-entry"
    entry_dir.mkdir()
    command_script = entry_dir / "command.sh"
    command_script.write_text("#!/bin/bash\necho test")

    entry = GalleryEntry.from_directory(entry_dir)

    assert entry.has_command_script is True, "has_command_script should return True when command.sh exists"


def test_has_command_script_returns_false_when_missing(tmp_path):
    """Test has_command_script property returns False when command.sh is missing."""
    # Create entry without command.sh
    entry_dir = tmp_path / "test-entry"
    entry_dir.mkdir()

    entry = GalleryEntry.from_directory(entry_dir)

    assert entry.has_command_script is False, "has_command_script should return False when command.sh missing"


def test_skip_execution_returns_inverse_of_has_command_script(tmp_path):
    """Test skip_execution property is inverse of has_command_script."""
    # Test with command.sh present
    entry_dir_with = tmp_path / "with-command"
    entry_dir_with.mkdir()
    (entry_dir_with / "command.sh").write_text("#!/bin/bash\n")
    entry_with = GalleryEntry.from_directory(entry_dir_with)

    assert entry_with.skip_execution is False, "skip_execution should be False when command.sh exists"
    assert entry_with.skip_execution == (not entry_with.has_command_script), \
        "skip_execution should be inverse of has_command_script"

    # Test without command.sh
    entry_dir_without = tmp_path / "without-command"
    entry_dir_without.mkdir()
    entry_without = GalleryEntry.from_directory(entry_dir_without)

    assert entry_without.skip_execution is True, "skip_execution should be True when command.sh missing"
    assert entry_without.skip_execution == (not entry_without.has_command_script), \
        "skip_execution should be inverse of has_command_script"
