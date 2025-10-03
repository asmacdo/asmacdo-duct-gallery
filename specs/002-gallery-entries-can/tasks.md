# Tasks: Optional Execution Skipping for Gallery Entries

**Feature**: 002-gallery-entries-can
**Input**: Design documents from `/home/austin/devel/asmacdo-duct-gallery/specs/002-gallery-entries-can/`
**Prerequisites**: plan.md ✓, research.md ✓, data-model.md ✓, contracts/ ✓, quickstart.md ✓

## Summary
Enable gallery entries to skip execution by detecting absence of command.sh file. When command.sh is not present, validate that info.json and usage.json exist, then generate plots directly from existing duct logs.

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Phase 3.1: Setup

- [x] T001 Create test fixture for skip execution mode in `tests/fixtures/gallery/skip-execution-example/`
  - Create directory structure: `.duct/`, `metadata.json`
  - Copy example logs from `tests/fixtures/gallery/example-1/.duct/` (runinfo.json, runusage.json)
  - Do NOT create command.sh or setup.sh (this entry tests skip mode)

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**

- [x] T002 [P] Integration test for skip execution mode in `tests/integration/test_skip_execution.py`
  - Test skip-execution-example entry is discovered
  - Test entry processes without executing command.sh
  - Test plot is generated from existing logs
  - Test entry is included in README.md output
  - MUST FAIL initially (skip logic not yet implemented)

- [x] T003 [P] Integration test for mixed mode gallery in `tests/integration/test_skip_execution.py`
  - Test gallery with both execute mode and skip mode entries
  - Test both entry types process correctly
  - Test README.md includes both entries
  - MUST FAIL initially (skip logic not yet implemented)

- [x] T004 [P] Integration test for skip mode error handling in `tests/integration/test_skip_execution.py`
  - Test entry without command.sh and without logs → warning, skipped
  - Test entry without command.sh but with corrupted logs → warning, skipped
  - Test other entries continue processing after skip mode failure
  - MUST FAIL initially (skip logic not yet implemented)

- [x] T005 [P] Unit test for command.sh detection in `tests/unit/test_gallery_entry.py`
  - Test has_command_script property returns True when command.sh exists
  - Test has_command_script property returns False when command.sh missing
  - Test skip_execution property (inverse of has_command_script)
  - MUST FAIL initially (properties not yet implemented)

## Phase 3.3: Core Implementation (ONLY after tests are failing)

- [x] T006 Add skip execution properties to GalleryEntry model in `src/models/gallery_entry.py`
  - Add @property has_command_script() → bool (checks self.command_script.exists())
  - Add @property skip_execution() → bool (returns not self.has_command_script)
  - No changes to __init__ or existing fields

- [x] T007 Update process_entry logic for conditional execution in `src/gallery_render.py`
  - Add command.sh existence check at start of process_entry()
  - If entry.has_command_script: execute existing code path (setup.sh, command.sh, plot)
  - If entry.skip_execution: validate logs exist, generate plot, skip execution
  - Add skip mode error handling: missing info.json → warning "command.sh absent but info.json missing"
  - Add skip mode error handling: missing usage.json → warning "command.sh absent but usage.json missing at {path}"
  - Add output message: "Skipping execution (no command.sh)" for skip mode entries

- [x] T008 Update process_entry log validation for skip mode in `src/gallery_render.py`
  - When skip_execution == True: validate .duct/*info.json exists before plot generation
  - When skip_execution == True: validate usage.json exists at path from info.json
  - Return False (skip entry) if either validation fails
  - Log appropriate warning message for each failure type

## Phase 3.4: Integration

- [x] T009 Run integration tests and verify both execution modes work
  - Execute `pytest tests/integration/test_skip_execution.py`
  - Verify all skip execution tests pass
  - Verify mixed mode gallery test passes
  - Verify error handling tests pass

- [x] T010 Run existing integration tests for backward compatibility
  - Execute `pytest tests/integration/test_full_pipeline.py`
  - Verify existing execute mode behavior unchanged
  - Verify no regressions in current functionality

## Phase 3.5: Polish

- [x] T011 [P] Run unit tests in `tests/unit/test_gallery_entry.py`
  - Verify has_command_script property tests pass
  - Verify skip_execution property tests pass

- [x] T012 Manual validation using quickstart.md scenarios
  - Test Scenario 1: Execute Mode (existing behavior)
  - Test Scenario 2: Skip Mode (new behavior)
  - Test Scenario 3: Mixed Mode Gallery
  - Test Scenario 4: Skip Mode with Missing Logs (error handling)
  - Test Scenario 5: Convert Execute Entry to Skip Entry

- [x] T013 Performance validation for skip mode
  - Create test gallery with 10 skip-mode entries
  - Run `time con-duct-gallery --gallery-dir <test-gallery>`
  - Verify execution completes in <10 seconds (vs potentially hours with full execution)

## Dependencies

**Critical Path**:
- T001 (test fixture) → T002-T005 (all tests)
- T002-T005 (all tests) → T006-T008 (implementation)
- T006 (model properties) → T007-T008 (process_entry updates)
- T007-T008 (implementation) → T009-T013 (validation)

**Parallel Execution**:
- T002, T003, T004, T005 can run in parallel (different test files/sections)
- T009, T010 can run in parallel (different test files)
- T011, T013 can run in parallel (different validation types)

## Parallel Example

```bash
# Launch T002-T005 together (test writing phase):
# All tests in different sections of test files, no conflicts
Task: "Write skip execution integration test in tests/integration/test_skip_execution.py"
Task: "Write mixed mode integration test in tests/integration/test_skip_execution.py"
Task: "Write error handling integration test in tests/integration/test_skip_execution.py"
Task: "Write command detection unit test in tests/unit/test_gallery_entry.py"

# Launch T009-T010 together (test execution phase):
Task: "Run skip execution integration tests"
Task: "Run existing integration tests for backward compatibility"
```

## Notes

- **TDD Approach**: Write tests first (T002-T005), verify they fail, then implement (T006-T008)
- **Minimal Changes**: Only modify `src/models/gallery_entry.py` and `src/gallery_render.py`
- **Backward Compatibility**: All existing entries with command.sh continue working unchanged
- **File-Based Detection**: Simple command.sh existence check, no configuration needed
- **Error Handling**: Skip mode failures are non-fatal warnings, other entries continue processing

## Validation Checklist
*GATE: Verify before marking Phase 3 complete*

- [x] All contracts have corresponding tests (CLI contract → integration tests T002-T004)
- [x] All entities have model tasks (GalleryEntry → T006)
- [x] All tests come before implementation (T002-T005 before T006-T008)
- [x] Parallel tasks truly independent (T002-T005 different test sections, T009-T010 different files)
- [x] Each task specifies exact file path (all tasks include file paths)
- [x] No task modifies same file as another [P] task (verified)

## Task Generation Rules Applied

1. **From Contracts** (`contracts/cli-interface.md`):
   - Execute mode behavior → T002 (integration test)
   - Skip mode behavior → T002 (integration test)
   - Mixed mode behavior → T003 (integration test)
   - Error handling → T004 (integration test)

2. **From Data Model** (`data-model.md`):
   - GalleryEntry properties → T005 (unit test), T006 (implementation)
   - Processing flow → T007-T008 (implementation)

3. **From Quickstart** (`quickstart.md`):
   - Test fixtures → T001 (setup)
   - Manual validation → T012 (polish)
   - Performance validation → T013 (polish)

4. **Ordering**: Setup → Tests → Models → Implementation → Validation → Polish

---
*Generated from plan.md, data-model.md, contracts/cli-interface.md, quickstart.md*
*Constitution principles: Test-first development, minimal changes, backward compatibility*
