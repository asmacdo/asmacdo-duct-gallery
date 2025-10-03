# CLI Interface Contract: con-duct-gallery

## Command
```bash
con-duct-gallery [OPTIONS]
```

## Required Arguments
- `-o, --output PATH` - Output markdown file path

## Optional Arguments
- `--gallery-dir PATH` - Gallery directory to scan (default: `./gallery`)

## Exit Codes
- `0` - Success, markdown generated
- `1` - Error (invalid arguments, no entries found, execution failures, write failures)

## Standard Output
- Progress messages during execution
- Entry processing status
- Success confirmation with output path

## Standard Error
- Warning messages for skipped entries
- Error messages for failures
- Execution error details

## Examples

### Basic Usage
```bash
con-duct-gallery -o gallery.md
```

**Output**:
```
Scanning gallery directory: ./gallery
Found 3 entries
Executing entry: example-1
  Running setup.sh...
  Running command.sh...
  Generating plot...
Executing entry: example-2
  Running setup.sh...
  Running command.sh...
  Generating plot...
Executing entry: example-3
  Running setup.sh...
  Running command.sh...
  Generating plot...
Generated markdown: gallery.md (3 entries)
```

### Custom Gallery Directory
```bash
con-duct-gallery -o output.md --gallery-dir /data/experiments
```

### Error: Invalid Output Path
```bash
con-duct-gallery -o /nonexistent/dir/output.md
```

**stderr**:
```
Error: Output path invalid - parent directory does not exist: /nonexistent/dir
```

**Exit code**: 1

### Warning: Entry Execution Failed
```bash
con-duct-gallery -o output.md
```

**stderr**:
```
Warning: Entry 'bad-entry' skipped - setup.sh failed with exit code 1
```

**stdout**:
```
Scanning gallery directory: ./gallery
Found 2 entries
Executing entry: good-entry
  Running setup.sh...
  Running command.sh...
  Generating plot...
Generated markdown: output.md (1 entry)
```

**Exit code**: 0 (warnings don't cause failure)

### Error: No Entries Found
```bash
con-duct-gallery -o output.md --gallery-dir empty/
```

**stderr**:
```
Error: No valid gallery entries found in empty/
```

**Exit code**: 1

## Behavioral Contract

### Execution Order
1. Validate output path (fail fast if invalid)
2. Scan gallery directory
3. Validate each entry (skip invalid, log warnings)
4. Execute entries sequentially
5. Generate markdown
6. Write output file

### Error Handling
- **Fatal errors** (exit 1): Invalid output path, no entries found, write failures
- **Non-fatal errors** (warnings, continue): Individual entry execution failures

### Idempotency
- Same gallery directory + same arguments → same output content (deterministic)
- Execution is repeatable
- Datalad provenance preserved for each run

### File System Effects
- Reads from: `<gallery-dir>/*/{setup.sh,command.sh,metadata.json}`
- Writes to: `<gallery-dir>/*/{.duct/,plots/}` (via duct/con-duct execution)
- Writes to: `<output-path>` (markdown file)

### Performance Expectations
- Total time = sum of all entry execution times + tool overhead
- Tool overhead (scanning, markdown generation): <5 seconds for 100 entries
- Entry execution time: depends entirely on duct command duration
  (could be seconds for quick commands, hours for long-running processes)
