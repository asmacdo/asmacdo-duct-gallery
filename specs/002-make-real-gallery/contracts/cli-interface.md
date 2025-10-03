# CLI Contract: con-duct-gallery

## Command: `con-duct-gallery`

### Synopsis
```bash
con-duct-gallery [OPTIONS]
```

### Description
Generate gallery README from entries in the entries/ directory. Scans for gallery entries, validates structure, and produces README.md with entry documentation.

### Options

#### `-o, --output PATH`
**Type**: File path
**Required**: No
**Default**: `README.md` (in current working directory)
**Description**: Path to output README file

**Contract**:
- Must be writable location
- Parent directory must exist
- If file exists, will be overwritten
- Relative paths resolved from current working directory

**Examples**:
```bash
con-duct-gallery -o README.md
con-duct-gallery --output docs/gallery.md
```

#### `--gallery-dir PATH`
**Type**: Directory path
**Required**: No
**Default**: `entries/` (relative to repository root)
**Description**: Path to gallery entries directory

**Contract**:
- Must be existing directory (fails with error if not - FR-011)
- Must be readable
- Relative paths resolved from current working directory

**Examples**:
```bash
con-duct-gallery --gallery-dir entries/
con-duct-gallery --gallery-dir /absolute/path/to/entries/
```

### Exit Codes

| Code | Meaning | Trigger |
|------|---------|---------|
| 0 | Success | README generated successfully (even if some entries skipped) |
| 1 | Error | entries/ directory does not exist (FR-011) |
| 1 | Error | Output path not writable |
| 1 | Error | Invalid arguments |

### Output

#### Standard Output
- Success message: "Generated README with N entries"
- Warning messages for incomplete entries (FR-010):
  ```
  WARNING: Skipping entry 'example-1': Missing required file command.sh
  WARNING: Skipping entry 'example-2': plots/ directory empty
  ```

#### Standard Error
- Error messages on failure:
  ```
  ERROR: Gallery directory does not exist: /path/to/entries/
  ERROR: Cannot write to output file: /path/to/README.md
  ```

### Behavior Contracts

#### FR-002: Auto-generate README from entries
```python
# Given
entries/ exists with valid entries
output path writable

# When
con-duct-gallery runs

# Then
README.md created with all valid entries
Exit code 0
```

#### FR-010: Skip incomplete entries with warning
```python
# Given
entries/incomplete-entry/ missing command.sh

# When
con-duct-gallery runs

# Then
Warning logged to stdout
Incomplete entry excluded from README
Other entries still processed
Exit code 0 (success despite warnings)
```

#### FR-011: Fail when entries/ missing
```python
# Given
entries/ does not exist

# When
con-duct-gallery runs

# Then
Error message to stderr
No README.md created/modified
Exit code 1
```

### Idempotency (FR-007)

Running the command multiple times with same inputs produces identical output:
```bash
$ con-duct-gallery -o README.md
Generated README with 2 entries

$ md5sum README.md
abc123... README.md

$ con-duct-gallery -o README.md
Generated README with 2 entries

$ md5sum README.md
abc123... README.md  # Same hash - identical output
```

### Entry Discovery Contract

Entry is considered **valid** if:
- Directory exists in entries/
- Contains `command.sh` file (readable)
- Contains `plots/` directory
- `plots/` contains at least one `.png` file

Entry is considered **incomplete** if any of above conditions fail.

Discovery process:
1. List all immediate subdirectories of entries/
2. For each subdirectory:
   - Check validation rules
   - If valid: Add to entries list
   - If invalid: Add to warnings list with reason
3. Sort valid entries by name (alphabetical)
4. Generate README from sorted list

### README Format Contract (FR-009)

Generated README structure:
```markdown
# Gallery

## Entry: {sorted_entry_1_name}

```bash
{contents of entry_1/command.sh}
```

![Plot]({relative path to first .png in entry_1/plots/})

---

## Entry: {sorted_entry_2_name}

...
```

Requirements:
- Title: Exactly "# Gallery"
- Entry order: Alphabetical by directory name
- Code block: Language hint must be `bash`
- Plot path: Relative to README.md location
- Separator: Exactly `---` with blank lines before/after
- No trailing newlines after final separator

### Example Usage

```bash
# Standard usage (generate README in current directory from entries/)
$ con-duct-gallery
Generated README with 2 entries
WARNING: Skipping entry 'incomplete-example': Missing required file command.sh

# Custom locations
$ con-duct-gallery --output docs/gallery.md --gallery-dir /data/gallery-entries/
Generated README with 5 entries

# Test mode (use test fixtures)
$ con-duct-gallery --gallery-dir tests/fixtures/gallery/ -o test-output.md
Generated README with 2 entries
```

### Contract Test Requirements

Tests must verify:
1. Valid entries → README generated with correct format
2. Incomplete entries → Warnings logged, other entries processed
3. Missing entries/ directory → Error exit, no README created
4. Idempotency → Multiple runs produce identical output
5. Entry ordering → Alphabetical by name
6. Plot paths → Relative paths correct from README location
7. Command content → Bash block contains exact command.sh contents
