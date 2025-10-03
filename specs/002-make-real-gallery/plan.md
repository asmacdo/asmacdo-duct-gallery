
# Implementation Plan: Real Gallery with Relocated Test Fixtures

**Branch**: `002-make-real-gallery` | **Date**: 2025-10-03 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/home/austin/devel/asmacdo-duct-gallery/specs/002-make-real-gallery/spec.md`

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

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary
Transform test fixtures into a production gallery structure by relocating entries from `tests/fixtures/gallery/` to `entries/` at repository root. Implement automated README generation that preserves current format (entry heading, bash code block, plot image). Support graceful degradation (skip incomplete entries with warnings) while maintaining test isolation through separate fixture copies.

## Technical Context
**Language/Version**: Python 3.11+
**Primary Dependencies**: pathlib, argparse, con-duct (for plot metadata), datalad (for provenance)
**Storage**: Filesystem (gallery entries as directories, README as markdown file)
**Testing**: pytest
**Target Platform**: Linux (primary), cross-platform compatible
**Project Type**: Single CLI application
**Performance Goals**: N/A (batch processing, human-triggered regeneration)
**Constraints**: Preserve existing README format exactly, maintain backward compatibility with existing fixtures
**Scale/Scope**: 10-50 gallery entries initially, designed for easy expansion

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**I. Reproducibility-First (NON-NEGOTIABLE)**
- [x] All gallery entries can be fully reproduced from scratch (relocated entries maintain existing structure)
- [x] Duct commands documented and re-runnable (preserved in command.sh files)
- [x] Con-duct plots regeneratable from duct outputs (existing plot generation maintained)
- [x] All operations use `datalad run` for provenance (constitution requirement preserved in relocated entries)
- [x] Entry validity verified by regeneration test (integration tests verify README regeneration)

**II. Automation Over Manual Steps**
- [x] Gallery generation fully automated (README auto-generated from entries/)
- [x] Manual steps limited to: curation, initial setup, debugging (only new entry creation is manual)
- [x] CI/CD validates reproducibility (existing tests adapted to new location)
- [x] Scripts preferred over documentation for operations (README generation via script, not manual editing)

**III. Test-First Development**
- [x] Tests written before implementation (existing integration test defines behavior)
- [x] Gallery entries serve as reproducibility test cases (fixtures demonstrate expected structure)
- [x] Red-Green-Refactor cycle followed (tests fail until relocation and README generation implemented)
- [x] No implementation without failing tests (integration test already exists and fails)

**IV. Simplicity & Maintainability**
- [x] Code readable by non-experts (file operations and markdown generation are straightforward)
- [x] Simple solutions over clever ones (directory scanning + template rendering, no complex frameworks)
- [x] Common design patterns used (discovery pattern for entries, template-based README generation)
- [x] "Why" documented, not "what" (clarifications explain design decisions)
- [x] Small atomic changes (relocation separate from README generation logic)
- [x] YAGNI principle applied (no metadata beyond what's needed for current README format)

## Project Structure

### Documentation (this feature)
```
specs/[###-feature]/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
entries/                     # NEW: Production gallery entries (relocated from tests/fixtures/gallery/)
├── example-1/
│   ├── README.md           # Entry documentation
│   ├── setup.sh            # Environment setup
│   ├── command.sh          # Duct execution command
│   ├── .duct/              # Duct outputs (includes info.json)
│   └── plots/              # Generated plots
└── example-2/
    └── [same structure]

src/
├── models/                  # Data models for gallery entries
├── renderers/               # README rendering logic
├── discovery.py             # Entry discovery logic
├── executor.py              # Entry execution (existing)
├── gallery_render.py        # README generation (to be enhanced)
├── plot_generator.py        # Plot generation (existing)
└── path_utils.py            # Path utilities

tests/
├── fixtures/
│   └── gallery/             # KEPT: Test fixture copies (separate from production)
│       ├── example-1/
│       └── example-2/
├── integration/
│   └── test_full_pipeline.py  # Tests README generation from entries
└── unit/                    # NEW: Unit tests for discovery, rendering

README.md                    # AUTO-GENERATED: Gallery documentation
```

**Structure Decision**: Single project structure (Python CLI). Production gallery at `entries/` (new top-level directory), test fixtures remain in `tests/fixtures/gallery/` for isolation. Existing `src/` structure extended with enhanced rendering capabilities.

## Phase 0: Outline & Research
1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:
   ```
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

## Phase 1: Design & Contracts
*Prerequisites: research.md complete*

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Generate contract tests** from contracts:
   - One test file per endpoint
   - Assert request/response schemas
   - Tests must fail (no implementation yet)

4. **Extract test scenarios** from user stories:
   - Each story → integration test scenario
   - Quickstart test = story validation steps

5. **Update agent file incrementally** (O(1) operation):
   - Run `.specify/scripts/bash/update-agent-context.sh claude`
     **IMPORTANT**: Execute it exactly as specified above. Do not add or remove any arguments.
   - If exists: Add only NEW tech from current plan
   - Preserve manual additions between markers
   - Update recent changes (keep last 3)
   - Keep under 150 lines for token efficiency
   - Output to repository root

**Output**: data-model.md, /contracts/*, failing tests, quickstart.md, agent-specific file

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `.specify/templates/tasks-template.md` as base
- Generate tasks from Phase 1 design docs (contracts, data model, quickstart)
- CLI contract → contract test task for con-duct-gallery command
- Each entity (GalleryEntry, Gallery, README) → model/dataclass creation task [P]
- Discovery logic → unit test + implementation task
- README rendering → unit test + implementation task
- Each quickstart scenario → integration test task
- Entry relocation → manual migration task (one-time)

**Ordering Strategy**:
- TDD order: Tests before implementation
- Dependency order:
  1. Data models (GalleryEntry, Gallery, README entities) [P]
  2. Unit tests for discovery logic
  3. Discovery implementation (entry validation, scanning)
  4. Unit tests for README rendering
  5. README rendering implementation (template generation)
  6. Integration test (full pipeline)
  7. CLI wiring (argparse, main function)
  8. Manual relocation task (copy fixtures to entries/)
- Mark [P] for parallel execution (independent files)

**Estimated Output**: 15-20 numbered, ordered tasks in tasks.md

**Gallery Entry Task Ordering** (per constitution):
- Setup/relocation tasks before execution
- Entry structure validation before README generation
- Tests before implementation (TDD)

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)  
**Phase 4**: Implementation (execute tasks.md following constitutional principles)  
**Phase 5**: Validation (run tests, execute quickstart.md, performance validation)

## Complexity Tracking
*Fill ONLY if Constitution Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |


## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [x] Phase 0: Research complete (/plan command) - research.md created
- [x] Phase 1: Design complete (/plan command) - data-model.md, contracts/, quickstart.md, CLAUDE.md created
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [x] Phase 3: Tasks generated (/tasks command) - tasks.md created with 18 tasks
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS (all principles satisfied)
- [x] Post-Design Constitution Check: PASS (no violations introduced)
- [x] All NEEDS CLARIFICATION resolved (no unknowns in technical context)
- [x] Complexity deviations documented (none - design aligns with constitution)

**Artifacts Created**:
- `/specs/002-make-real-gallery/plan.md` (this file)
- `/specs/002-make-real-gallery/research.md` (Phase 0 decisions)
- `/specs/002-make-real-gallery/data-model.md` (Phase 1 entities)
- `/specs/002-make-real-gallery/contracts/cli-interface.md` (Phase 1 CLI contract)
- `/specs/002-make-real-gallery/quickstart.md` (Phase 1 test scenarios)
- `/specs/002-make-real-gallery/tasks.md` (Phase 3 implementation tasks)
- `/CLAUDE.md` (updated with feature context)

**Next Step**: Execute tasks.md (18 tasks, TDD order, 3 parallel batches)

---
*Based on Constitution v1.0.0 - See `.specify/memory/constitution.md`*
