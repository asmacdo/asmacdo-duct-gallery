# Phase 0: Research & Decisions

## Overview
This feature relocates gallery entries from test fixtures to production location while implementing automated README generation. No unknowns remain - all technical decisions clarified during specification phase.

## Technical Decisions

### Decision 1: Gallery Location
**Decision**: `entries/` at repository root

**Rationale**:
- Clear, descriptive name indicating contents are individual gallery entries
- Top-level placement signals production status (not test infrastructure)
- Avoids ambiguity with "examples" (could be code samples) or "gallery" (could contain non-entry artifacts)

**Alternatives Considered**:
- `gallery/`: Too generic, doesn't convey that contents are discrete entries
- `examples/`: Implies code examples rather than complete reproducible demonstrations

### Decision 2: README Format
**Decision**: Preserve existing format exactly (entry heading, bash code block, plot image, separator)

**Rationale**:
- Current format is simple and effective
- Minimizes implementation complexity (no new formatting logic needed)
- Ensures continuity for existing users
- Satisfies constitution's simplicity principle (YAGNI)

**Alternatives Considered**:
- Enhanced format with metadata: Rejected due to increased complexity without clear user value
- Minimal format (command + plot only): Rejected as less readable

### Decision 3: Error Handling for Missing Files
**Decision**: Skip incomplete entries with warning, continue processing

**Rationale**:
- Graceful degradation allows partial gallery regeneration
- Warnings provide visibility into issues without blocking progress
- Supports iterative development of new entries (can regenerate README during setup)

**Alternatives Considered**:
- Fail immediately: Too fragile, blocks all regeneration on single incomplete entry
- Skip silently: Hides problems, makes debugging difficult
- Include with placeholders: Pollutes README with incomplete content

### Decision 4: Missing entries/ Directory
**Decision**: Fail with clear error message

**Rationale**:
- Directory existence is prerequisite - absence indicates misconfiguration
- Clear error guides user to resolution (create directory)
- Prevents confusing edge cases (empty README generation)

**Alternatives Considered**:
- Auto-create directory: Might mask real issues (wrong working directory, git state problems)
- Generate README with "no entries": Confusing output, unclear whether system is working

### Decision 5: Test Isolation Strategy
**Decision**: Maintain separate fixture copies in tests/fixtures/

**Rationale**:
- Test stability: Production gallery changes don't break tests
- Test speed: No dependency on production gallery state
- Clear separation of concerns: Tests validate behavior, not specific production data

**Alternatives Considered**:
- Tests use production entries/: Fragile, production changes could break tests
- Symlinks: Platform compatibility issues, unclear ownership

## Technology Stack Confirmation

### Python Standard Library
**Usage**: pathlib for file operations, argparse for CLI

**Rationale**: No external dependencies needed for file discovery and path manipulation. Standard library is sufficient and reduces complexity.

### Existing Codebase Integration
**Discovery**: Leverage existing `discovery.py` pattern for entry scanning

**Rendering**: Extend existing `gallery_render.py` and `renderers/` modules

**Rationale**: Reuse established patterns rather than introducing new architectural approaches. Maintains consistency with existing codebase.

## Implementation Approach

### README Generation Flow
1. Discover entries in `entries/` directory (scan for subdirectories)
2. For each entry:
   - Validate required files exist (command.sh, plots/)
   - If incomplete: Log warning, skip entry
   - If complete: Read command.sh, identify plot paths
3. Generate markdown sections using template:
   - `## Entry: {name}`
   - Bash code block with command.sh contents
   - Plot image reference
   - Separator (`---`)
4. Write complete README.md to repository root

### Entry Relocation Process
1. Copy existing fixtures from `tests/fixtures/gallery/` to `entries/`
2. Verify structure matches expected format
3. Run README generation to confirm functionality
4. Update integration test to point to new location (if needed)

## Risk Assessment

### Low Risk
- File operations (well-understood, standard library)
- README format (already defined and tested)
- Test isolation (fixtures remain in place)

### Medium Risk
- Path handling across platforms (mitigated by pathlib)
- Incomplete entry detection (mitigated by explicit validation + warnings)

### Mitigation Strategies
- Use pathlib for cross-platform compatibility
- Comprehensive error messages guide users to resolution
- Integration tests verify end-to-end behavior
- Keep test fixtures as ground truth during transition

## Open Questions
None - all ambiguities resolved during clarification phase.

## References
- Constitution v1.0.0: Gallery Entry Standards section
- Existing codebase: `src/discovery.py`, `src/gallery_render.py`
- Integration test: `tests/integration/test_full_pipeline.py`
