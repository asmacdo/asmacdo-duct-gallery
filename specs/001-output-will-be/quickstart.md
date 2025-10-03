# Quickstart: Gallery Markdown Output

## Prerequisites
- Python 3.11+
- Gallery entries exist in `gallery/` directory with setup.sh and command.sh

## Installation
```bash
# From repository root (installs con-duct[all] from requirements)
pip install .
```

## Basic Usage
```bash
# Execute all gallery entries and generate markdown
python -m src.gallery_render -o gallery.md

# Specify custom gallery directory
python -m src.gallery_render -o output.md --gallery-dir /path/to/gallery
```

## Integration Test Scenarios

### Scenario 1: Execute entries and generate markdown
**Given**: Gallery directory with 2 entries:
- `gallery/example-1/setup.sh` (prepares environment)
- `gallery/example-1/command.sh` contains `datalad run -m "example 1" duct -- python script.py`
- `gallery/example-2/setup.sh` (prepares environment)
- `gallery/example-2/command.sh` contains `datalad run -m "example 2" duct -- sleep 5`

**When**: Run `python -m src.gallery_render -o test-output.md`

**Then**:
- For each entry:
  - setup.sh is executed
  - command.sh is executed (produces .duct/usage.json)
  - Plot generated from usage.json using con-duct
- `test-output.md` is created
- File contains 2 entry sections
- Each section has heading, bash code block with command, embedded plot
- Images use relative paths from test-output.md location

**Validation**:
```bash
# Check duct outputs exist
test -f gallery/example-1/.duct/usage.json
test -f gallery/example-2/.duct/usage.json

# Check plots generated
test -f gallery/example-1/plots/*.png
test -f gallery/example-2/plots/*.png

# Check markdown structure
test -f test-output.md
grep -c "^## Entry:" test-output.md  # Should output: 2
grep -c "\`\`\`bash" test-output.md  # Should output: 2
grep -c "!\[Plot\]" test-output.md   # Should output: 2
```

---

### Scenario 2: Handle setup.sh execution failure
**Given**: Entry with failing setup.sh:
- `gallery/bad-setup/setup.sh` exits with error code 1
- `gallery/bad-setup/command.sh` exists

**When**: Run `python -m src.gallery_render -o test-output.md`

**Then**:
- Error logged: "Entry 'bad-setup' failed: setup.sh exited with code 1"
- Entry is excluded from output
- Other entries continue processing
- Command exits successfully (doesn't fail entire generation)

**Validation**:
```bash
! grep "bad-setup" test-output.md
```

---

### Scenario 3: Handle duct command execution failure
**Given**: Entry with failing duct command:
- `gallery/bad-command/setup.sh` succeeds
- `gallery/bad-command/command.sh` contains command that exits with error

**When**: Run `python -m src.gallery_render -o test-output.md`

**Then**:
- Error logged: "Entry 'bad-command' failed: command execution failed"
- Entry is excluded from output
- Other entries continue processing

**Validation**:
```bash
! grep "bad-command" test-output.md
```

---

### Scenario 4: Validate output path before execution
**Given**: Invalid output path `/nonexistent/dir/output.md`

**When**: Run `python -m src.gallery_render -o /nonexistent/dir/output.md`

**Then**:
- Error message: "Output path invalid: parent directory does not exist"
- Exit code: 1
- No commands executed (fail fast)

**Validation**:
```bash
python -m src.gallery_render -o /nonexistent/dir/output.md
test $? -eq 1
```

---

### Scenario 5: Fail if no entries found
**Given**: Empty gallery directory

**When**: Run `python -m src.gallery_render -o test-output.md --gallery-dir empty_gallery/`

**Then**:
- Error message: "No gallery entries found in empty_gallery/"
- Exit code: 1
- No output file created

**Validation**:
```bash
mkdir empty_gallery
python -m src.gallery_render -o test-output.md --gallery-dir empty_gallery/
test $? -eq 1
test ! -f test-output.md
```

---

### Scenario 6: Idempotent generation with datalad run provenance
**Given**: Gallery with 1 entry using datalad run

**When**:
1. Run `python -m src.gallery_render -o output1.md`
2. Run `python -m src.gallery_render -o output2.md`

**Then**:
- Both executions succeed
- Datalad run records provenance for both
- Generated markdown content is identical (same command, same plot pattern)

**Validation**:
```bash
python -m src.gallery_render -o output1.md
python -m src.gallery_render -o output2.md
# Compare markdown content (plots may differ if command is non-deterministic)
```

---

## Expected Output Format

```markdown
# Gallery

## Entry: example-1

\```bash
datalad run -m "example 1" duct -- python script.py
\```

![Plot](gallery/example-1/plots/resource-usage.png)

---

## Entry: example-2

\```bash
datalad run -m "example 2" duct -- sleep 5
\```

![Plot](gallery/example-2/plots/resource-usage.png)

---
```

## Execution Flow Per Entry
1. Change to entry directory
2. Execute `setup.sh` (prepare environment/data)
3. Execute `command.sh` (datalad run + duct, produces .duct/usage.json)
4. Generate plot from usage.json using con-duct → plots/
5. Read command from command.sh for markdown
6. Add entry section to markdown output

## Manual Testing Checklist
- [ ] Setup scripts execute successfully
- [ ] Duct commands produce usage.json
- [ ] Plots generated correctly from usage.json
- [ ] Generated markdown renders correctly in GitHub
- [ ] Datalad provenance recorded for all executions
- [ ] Plot images display correctly
- [ ] Code blocks have proper syntax highlighting
