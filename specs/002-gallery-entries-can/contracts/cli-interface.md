# CLI Interface Contract: con-duct-gallery (Updated for Optional Execution)

## Command
```bash
con-duct-gallery [OPTIONS]
```

## Optional Arguments
- `--gallery-dir PATH` - Gallery directory to scan (default: `./gallery`)

## Output Location
- Always writes to `README.md` in repository root (current working directory)

## Exit Codes
- `0` - Success, markdown generated (may have skipped some entries with warnings)
- `1` - Error (invalid arguments, no entries found, execution failures, write failures)

## Execution Modes

### Mode Detection
The system automatically detects execution mode for each entry based on file presence:
- **Execute Mode**: Entry has `command.sh` file → runs setup.sh (if exists) and command.sh
- **Skip Mode**: Entry has NO `command.sh` file → validates existing logs, generates plot only

### Execute Mode Behavior (Existing)
**When**: Entry directory contains `command.sh`

**Process**:
1. Execute `setup.sh` (if exists)
2. Execute `command.sh` (required)
3. Generate plot from resulting usage.json
4. Include entry in output

**Failures** (non-fatal, skip entry):
- setup.sh exits non-zero
- command.sh exits non-zero
- No info.json found after execution
- Plot generation fails

### Skip Mode Behavior (New)
**When**: Entry directory does NOT contain `command.sh`

**Process**:
1. Skip setup.sh execution (not run)
2. Skip command.sh execution (file does not exist)
3. Validate `.duct/*info.json` exists
4. Validate usage.json exists (path from info.json)
5. Generate plot from existing usage.json
6. Include entry in output

**Failures** (non-fatal, skip entry):
- No info.json found in .duct/
- usage.json path in info.json does not exist
- usage.json is not readable
- Plot generation fails

## Standard Output

### Basic Usage
```bash
con-duct-gallery
```

**Output**:
```
Scanning gallery directory: ./gallery
Discovered entry: example-1
Discovered entry: example-2
Discovered entry: example-3-skip
Found 3 entries
Executing entry: example-1
  Running setup.sh...
  Running command.sh...
  Generating plot...
Generated plot: gallery/example-1/plots/usage.png
Executing entry: example-2
  Running setup.sh...
  Running command.sh...
  Generating plot...
Generated plot: gallery/example-2/plots/usage.png
Executing entry: example-3-skip
  Skipping execution (no command.sh)
  Validating existing logs...
  Generating plot...
Generated plot: gallery/example-3-skip/plots/usage.png
Generated markdown: README.md (3 entries)
```

### Mixed Execution Modes
```bash
con-duct-gallery --gallery-dir ./test-gallery
```

**Output**:
```
Scanning gallery directory: ./test-gallery
Discovered entry: full-execution
Discovered entry: skip-execution
Found 2 entries
Executing entry: full-execution
  Running setup.sh...
  Running command.sh...
  Generating plot...
Generated plot: test-gallery/full-execution/plots/usage.png
Executing entry: skip-execution
  Skipping execution (no command.sh)
  Validating existing logs...
  Generating plot...
Generated plot: test-gallery/skip-execution/plots/usage.png
Generated markdown: README.md (2 entries)
```

## Standard Error

### Warning: Skip Mode Missing Logs
```bash
con-duct-gallery
```

**stderr**:
```
Warning: Entry 'broken-skip' skipped - command.sh absent but info.json missing
```

**stdout**:
```
Scanning gallery directory: ./gallery
Discovered entry: broken-skip
Discovered entry: working-entry
Found 2 entries
Executing entry: working-entry
  Running setup.sh...
  Running command.sh...
  Generating plot...
Generated plot: gallery/working-entry/plots/usage.png
Generated markdown: README.md (1 entry)
```

**Exit code**: 0 (warnings don't cause failure)

### Warning: Skip Mode Plot Failure
```bash
con-duct-gallery
```

**stderr**:
```
Warning: Entry 'corrupted-logs' skipped - plot generation failed
```

**stdout**:
```
Scanning gallery directory: ./gallery
Discovered entry: corrupted-logs
Found 1 entry
Executing entry: corrupted-logs
  Skipping execution (no command.sh)
  Validating existing logs...
  Generating plot...
Generated markdown: README.md (0 entries)
```

**Exit code**: 1 (no successful entries)

### Error: No Entries Found
```bash
con-duct-gallery --gallery-dir empty/
```

**stderr**:
```
Error: No valid gallery entries found in empty/
```

**Exit code**: 1

## Behavioral Contract

### Execution Order
1. Scan gallery directory
2. Discover all entries (validate basic structure)
3. For each entry:
   a. Check for command.sh existence
   b. If present: Execute mode (run scripts, generate logs, plot)
   c. If absent: Skip mode (validate logs, generate plot)
4. Generate markdown from successful entries
5. Write to README.md in current directory

### Error Handling
- **Fatal errors** (exit 1): No entries found, write failures to README.md
- **Non-fatal errors** (warnings, continue): Individual entry failures (both modes)

### Entry Processing Independence
- Entry failures do not affect other entries
- Mixed execution modes supported in same gallery
- Execution order: discovered order (directory listing)
- Each entry processed sequentially

### Backward Compatibility Guarantees
- Existing entries with command.sh: Behavior unchanged
- CLI arguments: No breaking changes
- Output format: README.md structure unchanged
- Exit codes: Unchanged
- Error messages: Expanded (new messages for skip mode), existing messages unchanged

### Idempotency
- Execute mode: Same gallery + same arguments → potentially different output (commands re-executed)
- Skip mode: Same gallery + same arguments → same output (deterministic from existing logs)
- Mixed mode gallery: Partial idempotency (skip mode entries deterministic, execute mode entries may vary)

### File System Effects

**Reads from**:
- `<gallery-dir>/*/command.sh` (optional existence check)
- `<gallery-dir>/*/setup.sh` (execute mode only, if exists)
- `<gallery-dir>/*/.duct/*info.json` (both modes)
- `<gallery-dir>/*/.duct/*usage.json` (both modes)

**Writes to**:
- `<gallery-dir>/*/.duct/` (execute mode only, via duct)
- `<gallery-dir>/*/plots/` (both modes, via con-duct)
- `README.md` in current working directory (both modes)

### Performance Expectations
- **Execute mode**: Total time = sum of command execution times + overhead (~5s for 100 entries)
- **Skip mode**: Total time = plot generation only + overhead (~10-30s for 100 entries)
- **Mixed mode**: Total time = sum of execute mode times + skip mode times + overhead

Gallery with all skip mode entries should be 10-100x faster than all execute mode (depending on command durations).

## Examples

### All Execute Mode (Current Behavior)
```bash
con-duct-gallery --gallery-dir gallery/
```
All entries have command.sh → all execute → same behavior as before feature

### All Skip Mode (Fast Regeneration)
```bash
con-duct-gallery --gallery-dir gallery-precomputed/
```
No entries have command.sh → all use existing logs → fast plot regeneration

### Mixed Mode (Typical Usage)
```bash
con-duct-gallery --gallery-dir gallery-mixed/
```
Some entries execute (command.sh present), others skip (command.sh absent) → flexible workflow

## Migration Path

### Converting Execute Entry to Skip Entry
1. Ensure entry has been executed at least once (has .duct/ logs)
2. Remove command.sh (and optionally setup.sh)
3. Entry will now use skip mode on next gallery generation
4. Logs and plots preserved from last execution

### Converting Skip Entry to Execute Entry
1. Add command.sh to entry directory
2. Entry will now use execute mode on next gallery generation
3. Existing logs will be overwritten (if duct uses --clobber)

### Validation
Use `con-duct-gallery` to validate conversion:
- If successful: Entry included in output
- If failed: Warning message indicates what's missing
