# Feature Specification: Optional Execution Skipping for Gallery Entries

**Feature Branch**: `002-gallery-entries-can`
**Created**: 2025-10-03
**Status**: Draft
**Input**: User description: "gallery entries can optionally skip execution and use existing duct logs. if an entry has a skip_execution flag or similar configuration, require that info.json and usage.json already exist, skip running setup.sh and command.sh, and just generate the plot from the existing usage.json"

---

## Clarifications

### Session 2025-10-03
- Q: Where should the skip_execution configuration be stored? → A: No configuration needed - skip execution if command.sh file does not exist
- Q: When validating usage.json for entries without command.sh, what level of validation is required? → A: Validate file readability only - assume valid since duct-produced; log and skip entry if plot generation fails

---

## User Scenarios & Testing

### Primary User Story
As a gallery maintainer, I want to regenerate gallery output without re-executing long-running duct commands, so I can update plots or markdown formatting quickly without waiting for hours of command execution when the duct logs already exist.

### Acceptance Scenarios
1. **Given** a gallery entry without command.sh but with existing info.json and usage.json files, **When** I generate the gallery output, **Then** the system skips execution and generates the plot directly from the existing usage.json
2. **Given** a gallery entry without command.sh but missing info.json, **When** I generate the gallery output, **Then** the system reports an error indicating the required file is missing and skips that entry
3. **Given** a gallery entry without command.sh but missing usage.json, **When** I generate the gallery output, **Then** the system reports an error indicating the required file is missing and skips that entry
4. **Given** a gallery entry with command.sh present, **When** I generate the gallery output, **Then** the system executes setup.sh (if present) and command.sh as normal (current behavior)
5. **Given** multiple gallery entries where some have command.sh and some do not, **When** I generate the gallery output, **Then** the system executes only those entries with command.sh and uses existing logs for the others

### Edge Cases
- When command.sh is absent but usage.json is corrupted or invalid, plot generation will fail - system logs the error, skips that entry, and continues processing others
- When info.json exists but points to a non-existent usage.json path, system reports error and skips that entry
- When an entry previously had command.sh (and was executed) but command.sh is now removed, system uses existing logs for plot-only regeneration

## Requirements

### Functional Requirements
- **FR-001**: System MUST detect whether command.sh exists in a gallery entry directory
- **FR-002**: System MUST validate that info.json exists when command.sh is absent for an entry
- **FR-003**: System MUST validate that usage.json exists when command.sh is absent for an entry
- **FR-004**: System MUST skip running setup.sh when command.sh is absent and required files exist
- **FR-005**: System MUST skip running command.sh when command.sh file does not exist
- **FR-006**: System MUST generate plots from existing usage.json when command.sh is absent
- **FR-007**: System MUST report clear error messages when command.sh is absent but required log files are missing
- **FR-008**: System MUST exclude entries with missing required files from the generated output
- **FR-009**: System MUST maintain backward compatibility with entries that have command.sh (execute normally)
- **FR-010**: System MUST determine usage.json path from info.json output_paths when command.sh is absent
- **FR-011**: System MUST validate that usage.json file is readable when command.sh is absent
- **FR-012**: System MUST log errors and skip entries where plot generation fails from existing usage.json
- **FR-013**: System MUST continue processing remaining entries when one entry's plot generation fails

### Non-Functional Requirements
- **NFR-001**: Gallery regeneration with all entries skipping execution MUST be significantly faster than full execution (no specific target defined)
- **NFR-002**: File-based detection mechanism MUST be simple and intuitive for gallery maintainers (presence/absence of command.sh)

### Key Entities
- **Gallery Entry**: A directory containing optional command.sh and setup.sh files for execution, or existing duct log files for plot-only regeneration
- **Duct Log Files**: The existing info.json and usage.json files that entries without command.sh depend on for plot generation

### Gallery Entry Requirements

- [x] **Environment setup**: Not applicable when command.sh is absent - setup.sh skipped entirely
- [x] **Execution command**: Not executed when command.sh is absent - determined by file presence
- [x] **Resource stats**: Must already exist when command.sh is absent (info.json and usage.json required)
- [x] **Plot generation**: Still automated from existing usage.json when command.sh is absent
- [x] **Metadata**: No additional metadata needed - execution behavior determined by command.sh presence
- [x] **Provenance**: When command.sh is absent, only plot generation recorded via datalad run (not command execution)
- [x] **Documentation**: Entry documentation should indicate if it uses existing logs (optional command.sh)
- [x] **Naming**: No change to naming requirements
- [x] **Reproducibility**: Entries without command.sh can be regenerated for plots but not for execution data

---

## Review & Acceptance Checklist

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

- [x] User description parsed
- [x] Key concepts extracted
- [x] Ambiguities marked
- [x] User scenarios defined
- [x] Requirements generated
- [x] Entities identified
- [x] Review checklist passed

---
