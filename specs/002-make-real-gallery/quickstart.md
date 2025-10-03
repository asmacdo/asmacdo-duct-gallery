# Phase 1: Quickstart Test Scenario

## Objective
Validate that the real gallery structure works end-to-end: relocate fixtures → generate README → verify output.

## Prerequisites
- Python 3.11+ installed
- Repository cloned
- Test fixtures exist at `tests/fixtures/gallery/`

## Test Scenario 1: Relocate and Generate

### Setup
```bash
# Start from repository root
cd /home/austin/devel/asmacdo-duct-gallery

# Ensure clean state
rm -rf entries/
rm -f README.md
```

### Execution
```bash
# Step 1: Create production gallery directory
mkdir entries/

# Step 2: Copy test fixtures to production location
cp -r tests/fixtures/gallery/example-1 entries/
cp -r tests/fixtures/gallery/example-2 entries/

# Step 3: Verify structure
ls -la entries/
# Expected: example-1/ and example-2/ directories

ls -la entries/example-1/
# Expected: command.sh, setup.sh, .duct/, plots/

# Step 4: Generate README
con-duct-gallery --gallery-dir entries/ -o README.md

# Step 5: Verify README exists
ls -la README.md
# Expected: README.md file created
```

### Expected Output
```
Generated README with 2 entries
```

### Verification
```bash
# Check README format
cat README.md
```

Expected content:
```markdown
# Gallery

## Entry: example-1

```bash
#!/bin/bash
# Test fixture command - uses real duct execution
# Use a command that runs long enough to generate usage data
 duct -p .duct/run --sample-interval 0.05 --report-interval 0.1 --clobber -- bash -c 'for i in {1..30}; do echo "Step $i"; sleep 0.2; done'
exit 0
```

![Plot](entries/example-1/plots/usage.png)

---

## Entry: example-2

```bash
#!/bin/bash
# Test fixture command - uses real duct execution
# Use a command that runs long enough to generate usage data
 duct -p .duct/run --sample-interval 0.05 --report-interval 0.1 --clobber -- bash -c 'for i in {1..20}; do echo "Processing $i"; sleep 0.3; done'
exit 0
```

![Plot](entries/example-2/plots/usage.png)

---
```

### Success Criteria
- [x] README.md created at repository root
- [x] Contains exactly 2 entry sections
- [x] Entry order is alphabetical (example-1 before example-2)
- [x] Each section has: heading, bash code block, plot image, separator
- [x] Bash blocks contain exact command.sh contents
- [x] Plot paths point to entries/*/plots/*.png
- [x] No errors or warnings (both entries are complete)

---

## Test Scenario 2: Incomplete Entry Handling

### Setup
```bash
# Create incomplete entry (missing command.sh)
mkdir -p entries/incomplete-example/plots/
touch entries/incomplete-example/plots/dummy.png
```

### Execution
```bash
con-duct-gallery --gallery-dir entries/ -o README.md
```

### Expected Output
```
WARNING: Skipping entry 'incomplete-example': Missing required file command.sh
Generated README with 2 entries
```

### Verification
```bash
# Check that incomplete entry is NOT in README
grep "incomplete-example" README.md
# Expected: No output (entry excluded)

# Check that valid entries still included
grep "example-1" README.md
# Expected: Match found
```

### Success Criteria
- [x] Warning logged for incomplete entry
- [x] Incomplete entry excluded from README
- [x] Valid entries (example-1, example-2) still processed
- [x] Exit code 0 (success despite warning)
- [x] README contains 2 entries (not 3)

---

## Test Scenario 3: Missing entries/ Directory

### Setup
```bash
# Remove entries directory
rm -rf entries/
```

### Execution
```bash
con-duct-gallery --gallery-dir entries/ -o README.md
```

### Expected Output (to stderr)
```
ERROR: Gallery directory does not exist: entries/
```

### Expected Exit Code
```
1
```

### Verification
```bash
echo $?
# Expected: 1

ls README.md 2>/dev/null || echo "README.md not created"
# Expected: "README.md not created"
```

### Success Criteria
- [x] Error message clearly states directory missing
- [x] Exit code 1 (failure)
- [x] No README.md created
- [x] No partial/corrupted README.md

---

## Test Scenario 4: Idempotency

### Setup
```bash
# Restore valid entries
mkdir entries/
cp -r tests/fixtures/gallery/* entries/
```

### Execution
```bash
# Generate README first time
con-duct-gallery --gallery-dir entries/ -o README.md
md5sum README.md > /tmp/first-run.md5

# Generate README second time
con-duct-gallery --gallery-dir entries/ -o README.md
md5sum README.md > /tmp/second-run.md5

# Compare checksums
diff /tmp/first-run.md5 /tmp/second-run.md5
```

### Expected Output
```
# No output from diff (files identical)
```

### Success Criteria
- [x] Both runs succeed
- [x] MD5 hashes identical
- [x] README content byte-for-byte identical

---

## Test Scenario 5: Integration Test Compatibility

### Execution
```bash
# Run existing integration test
pytest tests/integration/test_full_pipeline.py::test_execute_entries_and_generate_markdown
```

### Expected Output
```
tests/integration/test_full_pipeline.py::test_execute_entries_and_generate_markdown PASSED
```

### Success Criteria
- [x] Test passes (exit code 0)
- [x] All assertions pass:
  - README created at expected location
  - Contains expected entry headings
  - Contains bash code blocks
  - Contains plot image references

---

## Cleanup
```bash
# Remove temporary files
rm -f /tmp/first-run.md5 /tmp/second-run.md5

# Note: Keep entries/ and README.md for manual inspection if desired
# Or clean up completely:
# rm -rf entries/ README.md
```

---

## Quickstart Completion Checklist

- [ ] Scenario 1: Valid entries → README generated correctly
- [ ] Scenario 2: Incomplete entry → Warning logged, entry skipped
- [ ] Scenario 3: Missing directory → Error, no README created
- [ ] Scenario 4: Idempotency → Multiple runs produce identical output
- [ ] Scenario 5: Integration test passes → Existing test compatibility confirmed

All scenarios passing = Feature ready for production use
