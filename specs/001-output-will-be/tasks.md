# Tasks: Gallery Markdown Output

**Input**: Design documents from `/home/austin/devel/asmacdo-duct-gallery/specs/001-output-will-be/`
**Prerequisites**: plan.md, research.md, data-model.md, contracts/cli-interface.md, quickstart.md

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Phase 3.1: Setup
- [x] T001 Create project structure (src/, tests/, setup.py with con-duct-gallery entrypoint)
- [x] T002 Create requirements.txt with con-duct[all] and pytest dependencies
- [x] T003 [P] Create .gitignore for Python (\_\_pycache\_\_, .pytest_cache, .duct/, plots/)

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**

- [x] T004 [P] Create test fixture gallery entries in tests/fixtures/gallery/ (example-1, example-2 with setup.sh, command.sh)
- [x] T005 [P] Integration test: Execute entries and generate markdown in tests/integration/test_full_pipeline.py (Scenario 1)
- [ ] T006 [P] Integration test: Handle setup.sh failure in tests/integration/test_error_handling.py (Scenario 2) [DEFERRED]
- [ ] T007 [P] Integration test: Handle command.sh failure in tests/integration/test_error_handling.py (Scenario 3) [DEFERRED]
- [ ] T008 [P] Integration test: Validate output path in tests/integration/test_validation.py (Scenario 4) [DEFERRED]
- [ ] T009 [P] Integration test: Fail if no entries found in tests/integration/test_validation.py (Scenario 5) [DEFERRED]
- [ ] T010 [P] Integration test: Idempotent generation in tests/integration/test_idempotency.py (Scenario 6) [DEFERRED]

## Phase 3.3: Core Implementation (ONLY after tests are failing)
- [x] T011 [P] GalleryEntry model in src/models/gallery_entry.py (name, path, setup_script, command_script, command_text, usage_json, plot_path fields)
- [x] T012 [P] Entry discovery logic in src/discovery.py (scan gallery dir, validate structure, create GalleryEntry instances)
- [x] T013 [P] Script executor in src/executor.py (run setup.sh, run command.sh, capture exit codes and output)
- [x] T014 [P] Plot generator in src/plot_generator.py (call con-duct plot on usage.json, save to plots/ dir)
- [x] T015 [P] Path resolver in src/path_utils.py (calculate relative paths from output to plot images)
- [x] T016 Markdown renderer in src/renderers/markdown.py (format entry sections, generate full markdown content)
- [x] T017 CLI entrypoint in src/gallery_render.py (argparse, orchestrate: discover → execute → plot → render → write)

## Phase 3.4: Integration
- [x] T018 Wire up full pipeline in src/gallery_render.py main() (validate output path, discover, execute each entry, generate plots, render markdown, write file)
- [x] T019 Error handling and logging in src/gallery_render.py (skip failed entries with warnings, fail fast on fatal errors, clear error messages)
- [x] T020 Output validation in src/gallery_render.py (check parent dir exists and writable before execution)

## Phase 3.5: Polish
- [ ] T021 [P] Unit tests for GalleryEntry model in tests/unit/test_gallery_entry.py [DEFERRED]
- [ ] T022 [P] Unit tests for path resolver in tests/unit/test_path_utils.py [DEFERRED]
- [ ] T023 [P] Unit tests for markdown renderer in tests/unit/test_markdown_renderer.py [DEFERRED]
- [x] T024 Manual testing: Run on real gallery entries, verify markdown renders correctly in GitHub/VS Code
- [ ] T025 Update quickstart.md with actual installation and usage instructions [DEFERRED]

## Dependencies
- Setup (T001-T003) before all other tasks
- Tests (T004-T010) before implementation (T011-T020)
- T011 (GalleryEntry model) before T012 (discovery uses model)
- T012 (discovery) before T013 (executor needs entries)
- T013 (executor) before T014 (plot generator needs usage.json from execution)
- T014 (plot generator) before T015 (path resolver needs plot paths)
- T015 (path resolver) before T016 (renderer needs relative paths)
- T011-T016 before T017 (CLI integrates all components)
- T017 before T018 (integration wires up CLI)
- T018 before T019, T020 (error handling and validation extend integration)
- All implementation before polish (T021-T025)

## Parallel Execution Examples

### Launch Test Creation (T004-T010) Together
```python
# All test files are independent - can be created in parallel
Task: "Create test fixture gallery entries in tests/fixtures/gallery/"
Task: "Integration test for execute entries and generate markdown in tests/integration/test_full_pipeline.py"
Task: "Integration test for setup.sh failure in tests/integration/test_error_handling.py"
Task: "Integration test for command.sh failure in tests/integration/test_error_handling.py"
Task: "Integration test for output path validation in tests/integration/test_validation.py"
Task: "Integration test for no entries found in tests/integration/test_validation.py"
Task: "Integration test for idempotent generation in tests/integration/test_idempotency.py"
```

### Launch Core Module Implementation (T011-T016) in Groups
```python
# Independent modules can run in parallel
Task: "Create GalleryEntry model in src/models/gallery_entry.py"
Task: "Create entry discovery logic in src/discovery.py"
Task: "Create script executor in src/executor.py"
Task: "Create plot generator in src/plot_generator.py"
Task: "Create path resolver in src/path_utils.py"
# Note: T016 (markdown renderer) depends on T015 (path resolver), so run after
```

### Launch Unit Tests (T021-T023) Together
```python
# Independent test files
Task: "Unit tests for GalleryEntry model in tests/unit/test_gallery_entry.py"
Task: "Unit tests for path resolver in tests/unit/test_path_utils.py"
Task: "Unit tests for markdown renderer in tests/unit/test_markdown_renderer.py"
```

## Notes
- [P] tasks target different files with no dependencies
- Verify integration tests fail before implementing
- Each entry execution is independent (future: consider parallel execution)
- Commit after completing each phase
- con-duct[all] includes matplotlib for plotting

## Task Checklist Summary
**Total Tasks**: 25
- Setup: 3 tasks
- Tests: 7 tasks
- Core: 7 tasks
- Integration: 3 tasks
- Polish: 5 tasks

**Parallel Opportunities**:
- T003: Setup task (independent)
- T004-T010: All test creation (7 tasks)
- T011-T015: Core modules (5 tasks, some sequential)
- T021-T023: Unit tests (3 tasks)
