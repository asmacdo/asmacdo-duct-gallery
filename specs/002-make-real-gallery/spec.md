# Feature Specification: Real Gallery with Relocated Test Fixtures

**Feature Branch**: `002-make-real-gallery`
**Created**: 2025-10-03
**Status**: Draft
**Input**: User description: "make real gallery we can use text fixtures for now (but they should be moved) so we can replace them with real examples"

## Execution Flow (main)
```
1. Parse user description from Input
   → Feature: Transform test fixtures into real gallery
2. Extract key concepts from description
   → Actors: developers, users viewing gallery
   → Actions: relocate fixtures, generate README, run real examples
   → Data: gallery entries, plots, metadata
   → Constraints: keep fixtures usable temporarily
3. For each unclear aspect:
   → Mark with [NEEDS CLARIFICATION: specific question]
4. Fill User Scenarios & Testing section
   → User flow: maintain gallery → add entries → regenerate README
5. Generate Functional Requirements
   → Each requirement must be testable
   → Mark ambiguous requirements
6. Identify Key Entities (if data involved)
   → Gallery Entry, Plot, Metadata
7. Run Review Checklist
   → If any [NEEDS CLARIFICATION]: WARN "Spec has uncertainties"
   → If implementation details found: ERROR "Remove tech details"
8. Return: SUCCESS (spec ready for planning)
```

---

## Clarifications

### Session 2025-10-03
- Q: Where should the production gallery be located? → A: entries/
- Q: Should the README format be preserved exactly or use a different template? → A: Preserve current format exactly
- Q: What should happen when a gallery entry is missing required files (command.sh or plots)? → A: Skip entry but log warning, continue processing
- Q: What if the entries directory doesn't exist when attempting to generate the README? → A: Fail with clear error message
- Q: After relocation, how should tests reference gallery entries? → A: Tests maintain separate fixture copies in tests/fixtures/

---

## User Scenarios & Testing *(mandatory)*

### Primary User Story
A developer wants to maintain a gallery of duct command examples that showcase resource monitoring capabilities. The gallery should be easy to update and regenerate, with a production-ready structure (not buried in test fixtures). The README should be automatically generated from real gallery entries.

### Acceptance Scenarios
1. **Given** the current test fixtures exist, **When** the gallery is restructured, **Then** fixtures are moved to `entries/` at repository root
2. **Given** gallery entries exist in the new location, **When** the gallery generation command runs, **Then** a complete README.md is created with all entries
3. **Given** a developer wants to add a new example, **When** they create a new gallery entry, **Then** running regeneration includes it in the README
4. **Given** production gallery exists at entries/, **When** tests run, **Then** they still pass using separate fixture copies in tests/fixtures/

### Edge Cases
- When a gallery entry is missing required files (command.sh or plots), the system skips the entry with a warning and continues processing remaining entries
- When the entries directory doesn't exist, the system fails with a clear error message indicating the directory must be created first

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: System MUST relocate test fixtures from `tests/fixtures/gallery/` to `entries/` at repository root
- **FR-002**: System MUST generate README.md automatically from gallery entries
- **FR-003**: README MUST include each entry's command, description, and plots
- **FR-004**: Gallery structure MUST support easy addition of new entries
- **FR-005**: Tests MUST maintain separate fixture copies in tests/fixtures/ for isolation from production gallery
- **FR-006**: Each gallery entry MUST contain executable command and associated metadata
- **FR-007**: README generation MUST be repeatable and idempotent
- **FR-008**: Gallery location MUST be `entries/` at repository root
- **FR-009**: README format MUST preserve current structure (entry heading, bash code block, plot image reference, separator)
- **FR-010**: System MUST skip entries missing required files (command.sh or plots), log warning, and continue processing remaining entries
- **FR-011**: System MUST fail with clear error message when entries directory does not exist

### Key Entities

- **Gallery Entry**: A directory containing a duct command example, including:
  - Executable command script
  - Setup instructions (if needed)
  - Generated plots
  - Metadata (name, description, duct info.json path)

- **Gallery README**: Auto-generated documentation showing all entries with their commands and visualizations

- **Gallery Metadata**: Information about each entry (name, description, command, plot paths)

### Gallery Entry Requirements *(include if feature adds/modifies gallery entries)*
*Per constitution: Gallery Entry Standards section*

- [x] **Environment setup**: How to prepare environment for duct command (data prep, dependencies, containers, etc.)
- [x] **Execution command**: Datalad run + duct command specified
- [x] **Resource stats**: Required duct outputs identified (includes <prefix>info.json)
- [x] **Plot generation**: Automated via global render (info.json path in metadata)
- [x] **Metadata**: Entry name, description, versions, info.json path specified
- [x] **Provenance**: Datalad run usage planned for execution and plotting
- [x] **Documentation**: Entry README content outlined
- [x] **Naming**: Descriptive kebab-case name defined (e.g., `high-memory-python-sort`)
- [x] **Reproducibility**: Regeneration test scenario defined (setup → execute → render plots)

---

## Review & Acceptance Checklist
*GATE: Automated checks run during main() execution*

### Content Quality
- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

### Requirement Completeness
- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
- [x] Success criteria are measurable
- [x] Scope is clearly bounded
- [x] Dependencies and assumptions identified

---

## Execution Status
*Updated by main() during processing*

- [x] User description parsed
- [x] Key concepts extracted
- [x] Ambiguities marked
- [x] User scenarios defined
- [x] Requirements generated
- [x] Entities identified
- [x] Review checklist passed

---
