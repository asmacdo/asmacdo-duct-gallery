# Research: Optional Execution Skipping

**Feature**: 002-gallery-entries-can
**Date**: 2025-10-03

## Research Questions

### 1. File Existence Patterns in Python

**Decision**: Use `Path.exists()` from pathlib

**Rationale**:
- Standard library pathlib provides `Path.exists()` method
- Already used throughout codebase (discovery.py, executor.py, gallery_render.py)
- Returns boolean, handles both files and directories
- Cross-platform compatible
- More readable than `os.path.exists()`

**Alternatives Considered**:
- `os.path.exists()`: Older style, less readable
- `Path.is_file()`: Too specific, would fail if command.sh is accidentally a directory
- Try/except on file read: Overly complex for simple existence check

**Implementation**:
```python
command_script = entry_path / "command.sh"
if command_script.exists():
    # Execute
else:
    # Skip execution, validate logs
```

### 2. Error Handling Strategy

**Decision**: Follow existing warning pattern with `logger.warning()` and continue processing

**Rationale**:
- Existing code in `gallery_render.py` uses this pattern for non-fatal errors
- Entry failures should not block other entries from processing
- Warnings go to stderr, errors go to log
- Maintains consistency with current error handling approach

**Alternatives Considered**:
- Raise exceptions: Would stop processing of remaining entries
- Silent skip: User wouldn't know why entry was excluded
- Fatal error: Too harsh for missing optional files

**Existing Pattern** (from gallery_render.py:39):
```python
logger.warning(f"Warning: Entry '{entry.name}' skipped - setup.sh failed with exit code 1")
return False
```

**New Pattern** (for missing logs):
```python
logger.warning(f"Warning: Entry '{entry.name}' skipped - command.sh absent but info.json missing")
return False
```

### 3. Backward Compatibility Validation

**Decision**: No breaking changes required - all existing behavior preserved

**Rationale**:
- Entries with command.sh: Processed exactly as before (execute setup.sh → command.sh → plot)
- Entries without command.sh: New code path, doesn't affect existing entries
- No changes to command-line interface (no new flags required)
- No changes to output format
- Test fixtures (example-1, example-2) have command.sh and will continue to execute

**Validation Approach**:
1. Existing integration test (test_full_pipeline.py) should pass without modifications
2. New test (test_skip_execution.py) validates new code path
3. Both execution modes can coexist in same gallery directory

**Backward Compatibility Checklist**:
- [x] No changes to CLI arguments
- [x] No changes to output file format (README.md)
- [x] No changes to required entry files for executable entries
- [x] No changes to discovery.py behavior for entries with command.sh
- [x] Existing test fixtures work without modification

## Implementation Notes

### File Detection Logic
Location: `src/discovery.py` or `src/gallery_render.py` process_entry()

```python
def should_skip_execution(entry: GalleryEntry) -> bool:
    """Determine if entry should skip execution based on command.sh presence."""
    return not (entry.path / "command.sh").exists()
```

### Log Validation Logic
Location: `src/gallery_render.py` process_entry()

When skipping execution:
1. Check for `.duct/*info.json` (glob pattern)
2. Read info.json to get usage_json path
3. Validate usage.json exists
4. If either missing: log warning, return False
5. If both present: proceed to plot generation

### Minimal Changes Required
- **discovery.py**: No changes needed (entry discovery unchanged)
- **gallery_render.py**: Update `process_entry()` to check command.sh before executing
- **models/gallery_entry.py**: Add properties for has_command_script, skip_execution (optional, for clarity)

## Open Questions

None - all technical decisions resolved through clarification session.

## References

- Existing codebase: `src/gallery_render.py` (error handling patterns)
- Python pathlib docs: https://docs.python.org/3/library/pathlib.html
- Feature spec: `specs/002-gallery-entries-can/spec.md`
- Clarifications: Session 2025-10-03 in spec.md
