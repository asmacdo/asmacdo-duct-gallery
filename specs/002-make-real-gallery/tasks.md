# Tasks: Real Gallery with Relocated Test Fixtures

**Input**: Design documents from `/home/austin/devel/asmacdo-duct-gallery/specs/002-make-real-gallery/`
**Prerequisites**: plan.md, research.md, data-model.md, contracts/cli-interface.md, quickstart.md

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → Tech stack: Python 3.11+, pathlib, argparse, pytest
   → Structure: Single CLI application
2. Load design documents:
   → data-model.md: GalleryEntry, Gallery, README, READMESection
   → contracts/cli-interface.md: con-duct-gallery CLI
   → quickstart.md: 5 test scenarios
3. Generate tasks by category:
   → Setup: Project structure
   → Tests: Contract tests, unit tests, integration tests
   → Core: Data models, discovery, rendering
   → Integration: CLI wiring, entry relocation
   → Polish: Edge case tests, documentation
4. Apply task rules:
   → Different files = [P] for parallel
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001-T018)
6. SUCCESS (18 tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- All paths are absolute for clarity

---

## Phase 3.1: Setup

- [ ] **T001** Create production gallery directory structure
  - Create `entries/` at repository root
  - Create `tests/unit/` directory
  - Verify structure matches plan.md
  - No code changes, filesystem only

---

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3

**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**

- [ ] **T002 [P]** Unit test for GalleryEntry validation in `tests/unit/test_gallery_entry.py`
  - Test valid entry (has command.sh, plots/*.png)
  - Test missing command.sh (should fail validation)
  - Test missing plots/ directory (should fail validation)
  - Test empty plots/ directory (should fail validation)
  - Import from `src/models/gallery_entry.py` (doesn't exist yet - test will fail to import)

- [ ] **T003 [P]** Unit test for Gallery discovery in `tests/unit/test_gallery.py`
  - Test discovering valid entries (returns list of GalleryEntry)
  - Test entries/ directory doesn't exist (should raise error per FR-011)
  - Test incomplete entries (should add to warnings list per FR-010)
  - Test alphabetical ordering of entries
  - Import from `src/models/gallery.py` (doesn't exist yet - test will fail to import)

- [ ] **T004 [P]** Unit test for README rendering in `tests/unit/test_readme_renderer.py`
  - Test rendering single entry (correct markdown format per FR-009)
  - Test rendering multiple entries (alphabetical order)
  - Test plot path resolution (relative to README.md)
  - Test idempotency (same inputs → identical output per FR-007)
  - Import from `src/renderers/readme_renderer.py` (doesn't exist yet - test will fail to import)

- [ ] **T005 [P]** Contract test for CLI in `tests/contract/test_cli_contract.py`
  - Test default behavior (entries/ dir, README.md output)
  - Test --gallery-dir option
  - Test --output option
  - Test exit code 0 on success
  - Test exit code 1 when entries/ missing (FR-011)
  - Test warning output for incomplete entries (FR-010)
  - Import CLI from `src/cli.py` or similar (doesn't exist yet - test will fail to import)

- [ ] **T006** Integration test for full pipeline in `tests/integration/test_full_pipeline.py`
  - Update existing test to use new structure
  - Test: Create entries/ with fixtures → Run CLI → Verify README format
  - Test: Incomplete entry → Warning logged, entry skipped
  - Test: Missing entries/ → Error exit
  - Test: Idempotency (two runs produce identical README)
  - Use temp directory for isolation

---

## Phase 3.3: Core Implementation (ONLY after tests are failing)

- [ ] **T007 [P]** Create GalleryEntry model in `src/models/gallery_entry.py`
  - Implement dataclass with fields from data-model.md:
    - name: str
    - path: Path
    - command_script: Path
    - plots_dir: Path
    - readme_file: Optional[Path]
    - setup_script: Optional[Path]
  - Implement `validate()` method:
    - Check command_script exists and readable
    - Check plots_dir exists and contains *.png files
    - Return validation result (bool, optional error message)
  - Immutable value object (frozen dataclass)
  - Run T002 to verify tests pass

- [ ] **T008 [P]** Create Gallery model in `src/models/gallery.py`
  - Implement class with fields from data-model.md:
    - entries_dir: Path
    - entries: List[GalleryEntry]
    - incomplete_entries: List[str]
  - Implement `discover_entries()` method:
    - Scan entries_dir for subdirectories
    - Validate each entry using GalleryEntry.validate()
    - Separate valid/invalid entries
    - Sort valid entries alphabetically by name
  - Implement `get_warnings()` method:
    - Return formatted warning strings for incomplete entries
  - Validate entries_dir exists (raise error if not - FR-011)
  - Run T003 to verify tests pass

- [ ] **T009 [P]** Create READMESection model in `src/models/readme_section.py`
  - Implement dataclass with fields from data-model.md:
    - entry_name: str
    - command_content: str
    - plot_path: str
  - Implement `render()` method:
    - Generate markdown section per FR-009 format:
      - `## Entry: {entry_name}`
      - Triple backtick bash block with command_content
      - `![Plot]({plot_path})`
      - `---` separator
  - No validation (assumes valid inputs from Gallery)

- [ ] **T010** Create README renderer in `src/renderers/readme_renderer.py`
  - Implement `generate_readme(gallery: Gallery, output_path: Path) -> None`
  - For each complete entry in gallery:
    - Read command.sh content
    - Find first .png in plots/ directory
    - Calculate relative plot path from output_path to plot file
    - Create READMESection
  - Render template:
    - Header: `# Gallery\n\n`
    - All sections joined with proper spacing
  - Write to output_path (overwrite if exists)
  - Idempotent (same inputs → identical output)
  - Run T004 to verify tests pass

- [ ] **T011** Create CLI entry point in `src/cli.py`
  - Implement argparse with options from contracts/cli-interface.md:
    - `-o, --output PATH` (default: README.md)
    - `--gallery-dir PATH` (default: entries/)
  - Implement main() function:
    - Parse arguments
    - Create Gallery instance (handle errors from missing directory)
    - Call readme_renderer.generate_readme()
    - Print success message + warning count
    - Print warnings to stdout (FR-010)
    - Exit code 0 on success, 1 on error (FR-011)
  - Error handling:
    - Missing entries/ directory → stderr + exit 1
    - Output path not writable → stderr + exit 1
  - Run T005 to verify contract test passes

- [ ] **T012** Wire CLI to package entry point in `setup.py`
  - Add console_scripts entry point: `con-duct-gallery = src.cli:main`
  - Verify command is available after pip install
  - Test by running: `con-duct-gallery --help`
  - Run T006 to verify integration test passes

---

## Phase 3.4: Integration & Migration

- [ ] **T013** Relocate test fixtures to production gallery
  - Copy `tests/fixtures/gallery/example-1/` to `entries/example-1/`
  - Copy `tests/fixtures/gallery/example-2/` to `entries/example-2/`
  - Verify structure matches expected format (command.sh, plots/, etc.)
  - Keep test fixtures in place (FR-005: test isolation)
  - Manual task (one-time operation)

- [ ] **T014** Generate initial production README
  - Run: `con-duct-gallery --gallery-dir entries/ -o README.md`
  - Verify README.md created at repository root
  - Verify format matches existing README (FR-009)
  - Verify both entries included
  - Compare to expected output from quickstart.md Scenario 1
  - Manual verification task

---

## Phase 3.5: Polish & Edge Cases

- [ ] **T015 [P]** Add edge case test for plot path formats in `tests/unit/test_plot_path_resolution.py`
  - Test different README output locations (root, subdirectory)
  - Test entries at different depths
  - Test plot path always relative to README location
  - Verify no absolute paths in generated README

- [ ] **T016 [P]** Add error message clarity test in `tests/unit/test_error_messages.py`
  - Test missing entries/ directory → clear error (FR-011)
  - Test missing command.sh → clear warning (FR-010)
  - Test empty plots/ → clear warning
  - Test unwritable output → clear error
  - Verify error messages include paths

- [ ] **T017** Run all quickstart scenarios from `quickstart.md`
  - Scenario 1: Valid entries → README generated
  - Scenario 2: Incomplete entry → Warning, entry skipped
  - Scenario 3: Missing entries/ → Error exit
  - Scenario 4: Idempotency → Identical MD5 hashes
  - Scenario 5: Integration test passes
  - Manual verification (checklist in quickstart.md)

- [ ] **T018** Update repository README.md via regeneration
  - Verify entries/ populated with real examples
  - Run: `con-duct-gallery`
  - Verify generated README matches expected format
  - Commit README.md to repository
  - Final validation task

---

## Dependencies

### Blocking Dependencies
- **T001 blocks T002-T006**: Need directory structure before tests
- **T002-T006 block T007-T012**: Tests must fail before implementation (TDD)
- **T007-T008 block T010**: Renderer needs models
- **T010 blocks T011**: CLI needs renderer
- **T011 blocks T012**: Entry point needs CLI
- **T012 blocks T013-T014**: Need working CLI before migration
- **T013-T014 block T017-T018**: Need production data before validation

### Parallel Opportunities
- **T002, T003, T004, T005** [P]: Independent test files
- **T007, T008, T009** [P]: Independent model files
- **T015, T016** [P]: Independent edge case test files

---

## Parallel Execution Example

### Batch 1: Write all test files (after T001)
```bash
# Launch tests in parallel - they will all fail (expected for TDD)
Task: "Unit test for GalleryEntry validation in tests/unit/test_gallery_entry.py"
Task: "Unit test for Gallery discovery in tests/unit/test_gallery.py"
Task: "Unit test for README rendering in tests/unit/test_readme_renderer.py"
Task: "Contract test for CLI in tests/contract/test_cli_contract.py"
```

### Batch 2: Implement models (after tests written)
```bash
# Launch model creation in parallel
Task: "Create GalleryEntry model in src/models/gallery_entry.py"
Task: "Create Gallery model in src/models/gallery.py"
Task: "Create READMESection model in src/models/readme_section.py"
```

### Batch 3: Edge case tests (after core implementation)
```bash
# Launch edge case tests in parallel
Task: "Add edge case test for plot path formats in tests/unit/test_plot_path_resolution.py"
Task: "Add error message clarity test in tests/unit/test_error_messages.py"
```

---

## Validation Checklist
*GATE: Verify before marking tasks complete*

- [x] CLI contract (con-duct-gallery) has test (T005)
- [x] All entities have model tasks (T007: GalleryEntry, T008: Gallery, T009: READMESection)
- [x] All tests come before implementation (T002-T006 before T007-T012)
- [x] Parallel tasks truly independent (different files, no shared dependencies)
- [x] Each task specifies exact file path
- [x] No task modifies same file as another [P] task
- [x] TDD order enforced (Phase 3.2 before Phase 3.3)
- [x] All 5 quickstart scenarios covered (T017)
- [x] Constitution alignment: Test-first ✓, Simplicity ✓, Automation ✓

---

## Notes

- **TDD Critical**: T002-T006 must be written and failing before T007-T012
- **Test Isolation**: Test fixtures remain in `tests/fixtures/`, production gallery in `entries/` (FR-005)
- **Idempotency**: Verify with MD5 hashes in T017 Scenario 4 (FR-007)
- **Error Handling**: Clear messages for missing directories (FR-011) and files (FR-010)
- **Commit Strategy**: Commit after each task for atomic progress
- **Manual Tasks**: T013 (relocation), T014 (initial generation), T017 (quickstart validation), T018 (final README)

---

## Task Completion Status

**Total Tasks**: 18
**Estimated Time**: 4-6 hours (with tests written first, implementation follows smoothly)

### By Phase
- Setup: 1 task
- Tests: 5 tasks (all [P] after T001)
- Core: 6 tasks (3 models [P], 3 sequential)
- Integration: 2 tasks (manual)
- Polish: 4 tasks (2 [P], 2 manual)

### Parallelization Opportunities
- **3 batches** of parallel tasks (T002-T005, T007-T009, T015-T016)
- **Speedup**: ~30-40% time savings if parallelized

**Ready for execution**: All tasks are concrete, testable, and follow TDD principles per constitution.
