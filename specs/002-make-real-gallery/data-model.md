# Phase 1: Data Model

## Entities

### GalleryEntry
Represents a single gallery entry directory with its associated files and metadata.

**Fields**:
- `name: str` - Entry directory name (kebab-case, e.g., "example-1")
- `path: Path` - Absolute path to entry directory
- `command_script: Path` - Path to command.sh file
- `plots_dir: Path` - Path to plots/ directory
- `readme_file: Optional[Path]` - Path to entry-specific README.md (if exists)
- `setup_script: Optional[Path]` - Path to setup.sh (if exists)

**Validation Rules** (from FR-010, FR-011):
- Entry directory must exist
- `command_script` must exist and be readable
- `plots_dir` must exist and contain at least one .png file
- If validation fails: Entry is incomplete (skip with warning)

**Relationships**:
- One GalleryEntry contains multiple Plot files
- Multiple GalleryEntry instances comprise a Gallery

**State**: Stateless (immutable value object representing filesystem state at discovery time)

---

### Gallery
Collection of all gallery entries in the entries/ directory.

**Fields**:
- `entries_dir: Path` - Path to entries/ directory (from FR-008: must be repository root)
- `entries: List[GalleryEntry]` - List of discovered gallery entries
- `incomplete_entries: List[str]` - Names of entries that failed validation

**Validation Rules** (from FR-011):
- `entries_dir` must exist (fail with error if not)
- `entries_dir` must be a directory
- If `entries_dir` does not exist: Raise clear error (do not auto-create)

**Operations**:
- `discover_entries() -> List[GalleryEntry]`: Scan entries_dir for subdirectories, validate each
- `get_complete_entries() -> List[GalleryEntry]`: Return only entries passing validation
- `get_warnings() -> List[str]`: Return warning messages for incomplete entries

---

### README Document
The auto-generated README.md file at repository root.

**Fields**:
- `output_path: Path` - Path to README.md (repository root)
- `sections: List[READMESection]` - Ordered list of entry sections

**Structure** (from FR-009):
```markdown
# Gallery

## Entry: {entry.name}

```bash
{contents of entry.command_script}
```

![Plot]({relative_path_to_plot})

---

## Entry: {next_entry.name}
...
```

**Generation Rules**:
- Title: "# Gallery" (preserve existing)
- For each complete entry (in sorted order):
  - Heading: `## Entry: {name}`
  - Code block: Bash block with command.sh contents
  - Plot reference: First .png file found in plots/ directory
  - Separator: `---`
- Idempotent: Regenerating produces identical output for same inputs (FR-007)

---

### READMESection
Single entry section within the README.

**Fields**:
- `entry_name: str` - Name displayed in heading
- `command_content: str` - Contents of command.sh
- `plot_path: str` - Relative path to plot image (from README.md location)

**Formatting**:
- Heading level: H2 (`##`)
- Code block: Triple backtick, language hint `bash`
- Image: Standard markdown format `![Plot](path)`

---

## Data Flow

```
1. Discovery Phase
   entries/ directory
   ↓
   [Scan subdirectories]
   ↓
   List of entry paths
   ↓
   [Validate each entry]
   ↓
   Gallery(entries=valid, incomplete_entries=invalid)

2. README Generation Phase
   Gallery
   ↓
   [For each complete entry]
   ↓
   Read command.sh content
   ↓
   Find first plot in plots/
   ↓
   Create READMESection
   ↓
   [Collect all sections]
   ↓
   Render template with sections
   ↓
   Write README.md

3. Error Handling
   Incomplete entry detected
   ↓
   Log warning with entry name + missing files
   ↓
   Continue processing remaining entries
   ↓
   Include warnings in output
```

## Validation Matrix

| Entity | Validation | Failure Action |
|--------|------------|----------------|
| Gallery | entries/ exists | Fail immediately with error (FR-011) |
| Gallery | entries/ is directory | Fail immediately with error |
| GalleryEntry | command.sh exists | Mark incomplete, skip with warning (FR-010) |
| GalleryEntry | command.sh readable | Mark incomplete, skip with warning |
| GalleryEntry | plots/ exists | Mark incomplete, skip with warning |
| GalleryEntry | plots/ contains *.png | Mark incomplete, skip with warning |
| README | output path writable | Fail with error |

## Immutability & Simplicity

All entities are value objects - they represent filesystem state at a point in time. No complex state management needed:
- Discovery scans filesystem → creates GalleryEntry instances
- README generation reads GalleryEntry instances → produces markdown
- No persistence layer (filesystem is the data store)
- No caching (regeneration is cheap enough to run on-demand)

This design satisfies Constitution Principle IV (Simplicity & Maintainability): Simple data structures, clear data flow, no unnecessary abstraction.
