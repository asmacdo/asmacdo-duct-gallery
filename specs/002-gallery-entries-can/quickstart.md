# Quickstart: Optional Execution Skipping

## Overview
Gallery entries can now operate in two modes based on the presence of `command.sh`:
- **Execute Mode**: Entry has command.sh → runs duct command and generates logs
- **Skip Mode**: Entry lacks command.sh → uses existing logs for fast plot regeneration

## Prerequisites
- Python 3.11+
- con-duct-gallery installed (`pip install .`)
- Gallery entries with either command.sh (execute) or existing logs (skip)

## Basic Usage

### Scenario 1: Execute Mode (Existing Behavior)

**Given**: Gallery entry with command.sh

```bash
# Entry structure
gallery/example-execute/
├── setup.sh           # Optional
├── command.sh         # Required for execute mode
└── metadata.json

# Generate gallery (executes command.sh)
con-duct-gallery --gallery-dir gallery/
```

**Expected**:
- setup.sh executed (if exists)
- command.sh executed
- .duct/ directory created with logs
- plots/ directory created with usage.png
- Entry included in README.md

**Validation**:
```bash
# Check duct outputs exist
test -f gallery/example-execute/.duct/*info.json
test -f gallery/example-execute/.duct/*usage.json

# Check plot generated
test -f gallery/example-execute/plots/*.png

# Check entry in README
grep "example-execute" README.md
```

---

### Scenario 2: Skip Mode (New Behavior)

**Given**: Gallery entry WITHOUT command.sh but WITH existing logs

```bash
# Entry structure
gallery/example-skip/
├── .duct/
│   ├── runinfo.json   # From previous execution
│   └── runusage.json  # From previous execution
└── metadata.json
# Note: NO command.sh or setup.sh

# Generate gallery (skips execution, uses existing logs)
con-duct-gallery --gallery-dir gallery/
```

**Expected**:
- setup.sh NOT executed (skipped)
- command.sh NOT executed (does not exist)
- Existing .duct/ logs validated
- plots/ directory created with usage.png (regenerated from logs)
- Entry included in README.md

**Validation**:
```bash
# Verify logs exist (from previous run)
test -f gallery/example-skip/.duct/runinfo.json
test -f gallery/example-skip/.duct/runusage.json

# Check plot regenerated
test -f gallery/example-skip/plots/usage.png

# Check entry in README
grep "example-skip" README.md

# Verify fast execution (< 5 seconds for single entry)
time con-duct-gallery --gallery-dir gallery/example-skip/
```

---

### Scenario 3: Mixed Mode Gallery

**Given**: Gallery with both execute and skip mode entries

```bash
# Gallery structure
gallery/
├── execute-entry/
│   ├── command.sh     # Will execute
│   └── setup.sh
└── skip-entry/
    └── .duct/         # Will skip, use logs
        ├── runinfo.json
        └── runusage.json

# Generate gallery
con-duct-gallery --gallery-dir gallery/
```

**Expected Output**:
```
Scanning gallery directory: gallery
Discovered entry: execute-entry
Discovered entry: skip-entry
Found 2 entries
Executing entry: execute-entry
  Running setup.sh...
  Running command.sh...
  Generating plot...
Generated plot: gallery/execute-entry/plots/usage.png
Executing entry: skip-entry
  Skipping execution (no command.sh)
  Validating existing logs...
  Generating plot...
Generated plot: gallery/skip-entry/plots/usage.png
Generated markdown: README.md (2 entries)
```

**Validation**:
```bash
# Both entries in output
grep -c "^## Entry:" README.md  # Should output: 2

# Verify plots
test -f gallery/execute-entry/plots/usage.png
test -f gallery/skip-entry/plots/usage.png
```

---

## Error Handling Scenarios

### Scenario 4: Skip Mode with Missing Logs

**Given**: Entry without command.sh and without logs

```bash
# Entry structure (INVALID for skip mode)
gallery/broken-skip/
└── metadata.json
# No command.sh, no .duct/ directory

# Attempt to generate gallery
con-duct-gallery --gallery-dir gallery/
```

**Expected**:
- Warning logged: "Entry 'broken-skip' skipped - command.sh absent but info.json missing"
- Entry excluded from README.md
- Other entries continue processing
- Exit code: 0 (if other entries succeed) or 1 (if no entries succeed)

**Validation**:
```bash
# Entry not in README
! grep "broken-skip" README.md

# Warning in stderr
con-duct-gallery --gallery-dir gallery/ 2>&1 | grep "broken-skip.*skipped"
```

---

### Scenario 5: Convert Execute Entry to Skip Entry

**Given**: Existing execute mode entry with logs

```bash
# Start: Execute mode entry
gallery/convert-me/
├── command.sh
├── setup.sh
└── .duct/
    ├── runinfo.json   # From previous execution
    └── runusage.json

# Step 1: Run once to ensure logs exist
con-duct-gallery --gallery-dir gallery/convert-me/

# Step 2: Remove command.sh to convert to skip mode
rm gallery/convert-me/command.sh
# Optional: remove setup.sh too
rm gallery/convert-me/setup.sh

# Step 3: Regenerate using skip mode (fast)
time con-duct-gallery --gallery-dir gallery/convert-me/
```

**Expected**:
- First run: Executes (slow)
- Second run: Skips execution (fast, uses existing logs)
- Same plot generated both times
- README.md includes entry both times

**Validation**:
```bash
# Entry in README
grep "convert-me" README.md

# Verify fast execution time (skip mode)
# Should be <5s vs potentially minutes in execute mode
```

---

## Integration Test

### Full Pipeline Test (Both Modes)

```bash
# Setup test gallery with mixed modes
mkdir -p test-gallery/{exec-entry,skip-entry}

# Create execute mode entry
cat > test-gallery/exec-entry/command.sh <<'EOF'
#!/bin/bash
duct -p .duct/run --sample-interval 0.05 --report-interval 0.1 --clobber -- bash -c 'echo "test"; sleep 1'
exit 0
EOF
chmod +x test-gallery/exec-entry/command.sh

# Create skip mode entry (using example logs from existing entry)
mkdir -p test-gallery/skip-entry/.duct
cp gallery/example-1/.duct/runinfo.json test-gallery/skip-entry/.duct/
cp gallery/example-1/.duct/runusage.json test-gallery/skip-entry/.duct/

# Generate gallery
con-duct-gallery --gallery-dir test-gallery/

# Validate
test -f README.md
grep -c "^## Entry:" README.md  # Should output: 2
test -f test-gallery/exec-entry/plots/usage.png
test -f test-gallery/skip-entry/plots/usage.png

# Cleanup
rm -rf test-gallery
```

---

## Performance Comparison

### Execute Mode Performance
```bash
# Full execution (slow)
time con-duct-gallery --gallery-dir gallery-with-command-sh/
# Expected: Depends on command execution time (seconds to hours)
```

### Skip Mode Performance
```bash
# Skip execution (fast)
time con-duct-gallery --gallery-dir gallery-without-command-sh/
# Expected: <10s for 100 entries (only plot generation)
```

### Use Cases

**When to use Execute Mode**:
- First time adding an entry
- Updating duct command or execution parameters
- Need fresh resource usage data
- Testing reproducibility

**When to use Skip Mode**:
- Regenerating gallery for markdown/formatting changes
- Updating plot styling (con-duct updates)
- Fast iteration on gallery layout
- CI/CD for documentation updates (without re-execution)

---

## Manual Testing Checklist

**Execute Mode**:
- [ ] Entry with command.sh executes successfully
- [ ] setup.sh runs before command.sh
- [ ] duct logs generated in .duct/
- [ ] Plot generated in plots/
- [ ] Entry included in README.md

**Skip Mode**:
- [ ] Entry without command.sh skips execution
- [ ] Existing logs validated
- [ ] Plot generated from existing logs
- [ ] Entry included in README.md
- [ ] Fast execution time (<10s for reasonable entry count)

**Error Handling**:
- [ ] Missing logs in skip mode → warning, entry skipped
- [ ] Corrupted logs in skip mode → warning, entry skipped
- [ ] Mixed mode gallery → both types processed correctly
- [ ] Other entries continue processing after one fails

**Backward Compatibility**:
- [ ] Existing entries with command.sh work unchanged
- [ ] CLI arguments unchanged
- [ ] Output format unchanged
- [ ] Existing integration tests pass
