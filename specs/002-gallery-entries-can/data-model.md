# Data Model: Optional Execution Skipping

**Feature**: 002-gallery-entries-can
**Date**: 2025-10-03

## Entities

### GalleryEntry (Modified)

**Description**: Represents a single gallery entry that can either execute duct commands or use existing logs for plot generation.

**Location**: `src/models/gallery_entry.py`

**Fields** (existing fields unchanged, new properties added):
- `name: str` - Entry directory name
- `path: Path` - Absolute path to entry directory
- `setup_script: Path` - Path to setup.sh (may not exist)
- `command_script: Path` - Path to command.sh (may not exist)
- `command_text: str` - Content of command.sh for display
- `usage_json: Optional[Path]` - Path to usage.json (from info.json or None)
- `plot_path: Optional[Path]` - Path to generated plot

**New Properties** (computed, not stored):
```python
@property
def has_command_script(self) -> bool:
    """Returns True if command.sh exists in entry directory."""
    return self.command_script.exists()

@property
def skip_execution(self) -> bool:
    """Returns True if execution should be skipped (no command.sh)."""
    return not self.has_command_script
```

**Validation Rules**:
- When `skip_execution == True`:
  - MUST have at least one `.duct/*info.json` file
  - MUST have usage.json at path specified in info.json
  - setup.sh is NOT required
  - command.sh MUST NOT exist (by definition)

- When `skip_execution == False`:
  - command.sh MUST exist
  - setup.sh MAY exist (validated at execution time)
  - .duct/ logs will be generated during execution

**State Transitions**:
```
[Entry Discovered]
      ↓
[Check command.sh existence]
      ↓
  ┌───────┴────────┐
  ↓                ↓
[Has Command]   [No Command]
  ↓                ↓
[Execute Mode]  [Skip Mode]
  ↓                ↓
[Generate Logs] [Validate Logs]
  ↓                ↓
[Generate Plot] [Generate Plot]
  ↓                ↓
[Render Entry]  [Render Entry]
```

## Processing Flow

### Entry Discovery (Unchanged)

**Input**: Gallery directory path
**Process**: Scan for subdirectories, validate basic structure
**Output**: List of GalleryEntry objects

```python
def discover_entries(gallery_dir: Path) -> List[GalleryEntry]:
    """Discover all gallery entries in directory."""
    # Existing implementation - no changes
    # Sets entry.command_script = entry.path / "command.sh"
    # Does NOT validate command.sh existence
```

### Execution Decision (New)

**Input**: GalleryEntry object
**Process**: Check command.sh file existence
**Output**: Boolean (execute or skip)

```python
def should_execute(entry: GalleryEntry) -> bool:
    """Determine if entry requires execution."""
    return entry.has_command_script  # Simple file existence check
```

### Execution Mode Processing (Modified)

**When**: `entry.has_command_script == True`

**Flow**:
1. Execute setup.sh (if exists)
2. Execute command.sh (required)
3. Find info.json in .duct/
4. Read usage.json path from info.json
5. Generate plot from usage.json
6. Render entry to markdown

**Validation**:
- setup.sh execution failure → skip entry, log warning
- command.sh execution failure → skip entry, log warning
- Missing info.json after execution → skip entry, log warning
- Plot generation failure → skip entry, log warning

### Skip Mode Processing (New)

**When**: `entry.has_command_script == False`

**Flow**:
1. Skip setup.sh (not executed)
2. Skip command.sh (does not exist)
3. Find info.json in .duct/ (MUST exist)
4. Read usage.json path from info.json
5. Validate usage.json exists (MUST exist)
6. Generate plot from usage.json
7. Render entry to markdown

**Validation**:
- Missing info.json → skip entry, log warning: "Entry '{name}' skipped - command.sh absent but info.json missing"
- Missing usage.json → skip entry, log warning: "Entry '{name}' skipped - command.sh absent but usage.json missing at {path}"
- Plot generation failure → skip entry, log warning: "Entry '{name}' skipped - plot generation failed"

## Error Handling

### Error Categories

**Fatal Errors** (exit code 1, stop gallery generation):
- No entries found in gallery directory
- Output path not writable

**Non-Fatal Errors** (log warning, skip entry, continue):
- setup.sh execution failure (execute mode)
- command.sh execution failure (execute mode)
- Missing info.json (skip mode)
- Missing usage.json (skip mode)
- Plot generation failure (both modes)

### Error Messages

**Skip Mode Errors**:
```
Warning: Entry 'example-3' skipped - command.sh absent but info.json missing
Warning: Entry 'example-4' skipped - command.sh absent but usage.json missing at .duct/runusage.json
Warning: Entry 'example-5' skipped - plot generation failed from existing logs
```

**Execute Mode Errors** (unchanged):
```
Warning: Entry 'example-1' skipped - setup.sh failed with exit code 1
Warning: Entry 'example-2' skipped - command.sh failed
Warning: Entry 'example-6' skipped - no duct info.json found
```

## Data Flow Diagram

```
Gallery Directory
    ↓
[discover_entries]
    ↓
List[GalleryEntry]
    ↓
For each entry:
    ↓
[Check entry.has_command_script]
    ↓
┌───────────────┴──────────────┐
↓ True                         ↓ False
[Execute Mode]                 [Skip Mode]
↓                              ↓
[Run setup.sh + command.sh]    [Validate logs exist]
↓                              ↓
[Find info.json in .duct/]     [Find info.json in .duct/]
↓                              ↓
[Read usage path]              [Read usage path]
↓                              ↓
[Generate plot]                [Generate plot]
↓                              ↓
[Add to successful_entries]    [Add to successful_entries]
    ↓
    └──────────────┬─────────────┘
                   ↓
         [render_markdown]
                   ↓
              [Write README.md]
```

## Relationships

### GalleryEntry → Duct Log Files

**Type**: Dependency (skip mode) / Generation (execute mode)

**Execute Mode**: GalleryEntry execution PRODUCES duct log files
- command.sh creates .duct/runinfo.json, .duct/runusage.json

**Skip Mode**: GalleryEntry REQUIRES existing duct log files
- Must have .duct/*info.json (from previous execution)
- Must have .duct/*usage.json (path from info.json)

### GalleryEntry → Plot Files

**Type**: Generation (both modes)

Both modes PRODUCE plot files:
- con-duct plot generates plots/usage.png
- Plot generation occurs after logs are available (either from execution or existing)

## Implementation Notes

### Minimal Code Changes

**GalleryEntry model** (`src/models/gallery_entry.py`):
- Add two @property methods (has_command_script, skip_execution)
- No changes to __init__ or existing fields

**gallery_render.py** (`process_entry` function):
- Add file existence check at start of function
- Branch into two code paths based on result
- Skip mode reuses existing log validation and plot generation code

**No changes required**:
- discovery.py (entry discovery unchanged)
- executor.py (execution logic unchanged)
- plot_generator.py (plot generation unchanged)
- renderers/markdown.py (rendering unchanged)

### Backward Compatibility

All existing entries have command.sh → always take execute mode path → behavior identical to current implementation.
