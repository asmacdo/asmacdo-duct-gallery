# Implementation Plan: Optional Execution Skipping for Gallery Entries

**Branch**: `002-gallery-entries-can` | **Date**: 2025-10-03 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/home/austin/devel/asmacdo-duct-gallery/specs/002-gallery-entries-can/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Detect Project Type from file system structure or context (web=frontend+backend, mobile=app+api)
   → Set Structure Decision based on project type
3. Fill the Constitution Check section based on the content of the constitution document.
4. Evaluate Constitution Check section below
   → If violations exist: Document in Complexity Tracking
   → If no justification possible: ERROR "Simplify approach first"
   → Update Progress Tracking: Initial Constitution Check
5. Execute Phase 0 → research.md
   → If NEEDS CLARIFICATION remain: ERROR "Resolve unknowns"
6. Execute Phase 1 → contracts, data-model.md, quickstart.md, agent-specific template file (e.g., `CLAUDE.md` for Claude Code, `.github/copilot-instructions.md` for GitHub Copilot, `GEMINI.md` for Gemini CLI, `QWEN.md` for Qwen Code, or `AGENTS.md` for all other agents).
7. Re-evaluate Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
8. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
9. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 8. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary
Enable gallery entries to skip execution by detecting absence of command.sh file. When command.sh is not present, validate that info.json and usage.json exist, then generate plots directly from existing duct logs. This allows fast regeneration of gallery output without re-executing long-running commands while maintaining backward compatibility with entries that have command.sh.

## Technical Context
**Language/Version**: Python 3.11+
**Primary Dependencies**: con-duct[all] (includes matplotlib), pytest, datalad
**Storage**: File system (gallery entry directories with .duct/ logs and plots/)
**Testing**: pytest for unit and integration tests
**Target Platform**: Linux (primary), cross-platform Python
**Project Type**: single (CLI tool)
**Performance Goals**: Gallery regeneration with skipped execution should complete in <10s for 100 entries (vs hours with full execution)
**Constraints**: Must maintain backward compatibility with existing gallery entries; file-based detection must be intuitive
**Scale/Scope**: 10-100 gallery entries initially, scalable to 1000+

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**I. Reproducibility-First (NON-NEGOTIABLE)**
- [x] All gallery entries can be fully reproduced from scratch (entries WITH command.sh)
- [x] Entries without command.sh use pre-existing duct-generated logs (reproducible from original execution)
- [x] Con-duct plots regeneratable from duct outputs (both execution modes)
- [x] All operations use `datalad run` for provenance (plot generation tracked even when skipping execution)
- [x] Entry validity verified by regeneration test

**II. Automation Over Manual Steps**
- [x] Gallery generation fully automated (no manual intervention for skip detection)
- [x] Manual steps limited to: curation, initial setup, debugging
- [x] File-based detection (command.sh presence) replaces configuration files
- [x] Scripts preferred over documentation for operations

**III. Test-First Development**
- [x] Tests written before implementation (integration tests for skip detection)
- [x] Gallery entries serve as reproducibility test cases
- [x] Red-Green-Refactor cycle followed
- [x] No implementation without failing tests

**IV. Simplicity & Maintainability**
- [x] Code readable by non-experts (simple file existence check)
- [x] Simple solutions over clever ones (file presence vs configuration system)
- [x] Common design patterns used (existing entry processing extended)
- [x] "Why" documented, not "what"
- [x] Small atomic changes (minimal modification to existing flow)
- [x] YAGNI principle applied (no configuration system added)

## Project Structure

### Documentation (this feature)
```
specs/002-gallery-entries-can/
├── spec.md              # Feature specification
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
│   └── cli-interface.md # Updated CLI behavior contract
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
src/
├── models/
│   └── gallery_entry.py      # GalleryEntry model (EXISTING - minor update)
├── discovery.py              # Entry discovery (EXISTING - update for skip detection)
├── executor.py               # Script execution (EXISTING - conditional execution)
├── plot_generator.py         # Plot generation (EXISTING - no changes)
├── path_utils.py             # Path utilities (EXISTING - no changes)
├── renderers/
│   └── markdown.py           # Markdown rendering (EXISTING - no changes)
└── gallery_render.py         # Main CLI (EXISTING - update process_entry logic)

tests/
├── fixtures/
│   └── gallery/
│       ├── example-1/        # EXISTING - with command.sh
│       ├── example-2/        # EXISTING - with command.sh
│       └── skip-execution-example/  # NEW - without command.sh, with logs
│           ├── .duct/
│           │   ├── runinfo.json
│           │   └── runusage.json
│           └── plots/        # Pre-existing or generated
├── integration/
│   └── test_skip_execution.py  # NEW - skip execution scenarios
└── unit/
    └── test_discovery.py     # EXISTING - update for skip detection
```

**Structure Decision**: Single project (CLI tool). Extends existing src/ structure with minimal changes to support conditional execution based on command.sh file presence. No new top-level directories required.

## Phase 0: Outline & Research

No significant unknowns remain - all technical context is clear from existing codebase and clarifications. Brief research needed on:

1. **File existence patterns in Python**: Confirm `Path.exists()` best practice
2. **Error handling strategy**: Review existing error handling in gallery_render.py for consistency
3. **Backward compatibility validation**: Confirm no breaking changes to existing entries

**Output**: research.md documenting these minimal decisions

## Phase 1: Design & Contracts

### Data Model Updates
**File**: data-model.md

**GalleryEntry** (existing model - minor update):
- Add `has_command_script: bool` property (derived from file existence check)
- Add `skip_execution: bool` property (alias for not has_command_script)
- Existing fields remain unchanged

**Entry Processing Flow** (state machine):
```
Discovery → File Check → [Has command.sh?]
                              ↓ Yes             ↓ No
                         Execute Scripts    Validate Logs
                              ↓                  ↓
                         Generate Plot      Generate Plot
                              ↓                  ↓
                         Render Entry       Render Entry
```

### CLI Contract Update
**File**: contracts/cli-interface.md

Update existing CLI contract to document:
- Command detection behavior (command.sh presence/absence)
- Error messages when logs missing for skip-execution entries
- Backward compatibility guarantees
- Exit codes remain unchanged

### Quickstart Scenarios
**File**: quickstart.md

Document two execution modes:
1. **Full execution mode**: Entry with command.sh (existing behavior)
2. **Skip execution mode**: Entry without command.sh using existing logs (new behavior)

Include validation commands to verify both modes work correctly.

### Agent Context Update
Run `.specify/scripts/bash/update-agent-context.sh claude` to add:
- Optional execution skipping feature context
- File-based detection mechanism
- Backward compatibility notes

**Output**: data-model.md, contracts/cli-interface.md, quickstart.md, CLAUDE.md update

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Integration tests FIRST (TDD): Test skip execution scenarios before implementation
- Update discovery.py to detect command.sh presence
- Update gallery_render.py process_entry() to conditionally execute
- Update GalleryEntry model with skip detection properties
- Unit tests for file detection logic

**Ordering Strategy**:
1. Test fixtures: Create skip-execution example entry (with logs, without command.sh)
2. Integration tests: Test full skip execution flow (MUST FAIL initially)
3. Unit tests: Test command.sh detection logic (MUST FAIL initially)
4. Implementation: Update discovery.py for detection
5. Implementation: Update gallery_render.py for conditional execution
6. Implementation: Update GalleryEntry model
7. Validation: Run tests, verify both modes work

**Estimated Output**: 10-12 numbered, ordered tasks in tasks.md

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)
**Phase 4**: Implementation (execute tasks.md following constitutional principles)
**Phase 5**: Validation (run tests, execute quickstart.md, verify backward compatibility)

## Complexity Tracking
*No constitutional violations - design is simple and aligns with all principles*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |

## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [x] Phase 0: Research complete (/plan command)
- [x] Phase 1: Design complete (/plan command)
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS
- [x] Post-Design Constitution Check: PASS
- [x] All NEEDS CLARIFICATION resolved
- [x] Complexity deviations documented (none)

---
*Based on Constitution v1.0.0 - See `.specify/memory/constitution.md`*
