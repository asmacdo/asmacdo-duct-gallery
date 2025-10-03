<!--
SYNC IMPACT REPORT
Version change: [INITIAL] → 1.0.0
Initial constitution creation

Modified principles: N/A (initial creation)
Added sections:
  - Core Principles (4 principles: Reproducibility-First, Automation, Test-First, Simplicity)
  - Gallery Entry Standards (includes environment setup, datalad run integration, automated plotting)
  - Validation Requirements (CI/CD reproducibility checks)
  - Governance (amendment process, versioning, compliance)

Templates requiring updates:
  ✅ plan-template.md - Updated Constitution Check with all 4 principles as checklist items
  ✅ spec-template.md - Added Gallery Entry Requirements section with setup/execution/rendering flow
  ✅ tasks-template.md - Added Gallery Entries task generation rules and ordering guidance

Key design decisions:
  - Environment setup via setup.sh script per entry
  - Datalad run integration for provenance tracking
  - Automated plot generation via global render (no per-entry plot scripts)
  - Metadata includes info.json path for rendering
  - Reproducibility flow: setup → execute → render

Follow-up TODOs: None - all templates synchronized with constitution v1.0.0
-->

# duct-gallery Constitution

## Core Principles

### I. Reproducibility-First (NON-NEGOTIABLE)
Every gallery entry MUST be fully reproducible. Duct executions must be re-runnable to
regenerate outputs. Con-duct plots must be regeneratable from duct outputs. All operations
MUST use `datalad run` to preserve complete provenance. An entry is valid only if it can be
regenerated from scratch.

**Rationale**: Reproducibility is the foundation of scientific computing and the core value
proposition of this gallery. Without guaranteed reproducibility, entries lose their
demonstrative and educational value.

### II. Automation Over Manual Steps
Gallery generation and validation MUST be fully automated. Manual intervention permitted only
for: new entry curation, initial dataset setup, debugging failures. CI/CD MUST validate
reproducibility of all entries. Scripts over documentation for operational tasks.

**Rationale**: Manual processes are error-prone and don't scale. Automation ensures
consistency, enables continuous validation, and allows the gallery to grow sustainably.

### III. Test-First Development
TDD mandatory: Tests written → User approved → Tests fail → Then implement. Each gallery
entry serves as a reproducibility test case. Red-Green-Refactor cycle strictly enforced. No
implementation without failing tests first.

**Rationale**: Tests written first ensure we build what's needed, not what's easy. Gallery
entries as tests create a self-validating system where additions must prove their worth.

### IV. Simplicity & Maintainability
Code MUST be readable by non-experts. Prefer simple solutions over clever ones. Follow common
design patterns. Document the "why" not the "what". Small atomic changes for easy review.
Avoid over-engineering (YAGNI).

**Rationale**: Simple code lasts. Complex solutions create maintenance burden and barriers to
contribution. Readable code enables collaboration and long-term sustainability.

## Gallery Entry Standards

Each gallery entry MUST include:
- **Environment setup**: Instructions/scripts to prepare environment for duct command
  (data preparation, dependencies, containers, etc.)
- **Execution command**: Datalad run + duct command for provenance-tracked execution
- **Resource stats**: Complete duct output files including <prefix>info.json
- **Plot generation**: Automated via global render with info.json path (no per-entry plot script)
- **Metadata**: Entry name, description, creation date, duct/con-duct versions, info.json path
- **Provenance**: Complete datalad run records for execution and plotting steps
- **README**: Entry-specific documentation explaining what is demonstrated

Entry directory structure:
```
gallery/
├── <entry-name>/
│   ├── README.md           # Entry documentation
│   ├── setup.sh            # Environment setup script
│   ├── command.sh          # Datalad run + duct execution command
│   ├── .duct/              # Duct outputs (auto-generated, includes info.json)
│   ├── plots/              # Con-duct plots (auto-generated via global render)
│   └── metadata.json       # Entry metadata (includes info.json path)
```

**Entry naming**: Use descriptive kebab-case names that indicate the demonstrated behavior
(e.g., `high-memory-python-sort`, `cpu-bound-matrix-multiply`, `io-heavy-file-processing`)

## Validation Requirements

Automated validation MUST verify:
- **Reproducibility**: Each entry can be re-executed successfully
- **Provenance**: All entries have valid datalad run records
- **Completeness**: Required files present (command, outputs, plots, metadata)
- **Plot regeneration**: Con-duct plots match expected output
- **Version compatibility**: Duct/con-duct versions documented and compatible

CI checks run on:
- Pull requests adding/modifying entries
- Scheduled validation (weekly) for all entries
- Manual trigger for debugging

Failed validation MUST block merges. Degraded entries MUST be flagged for repair or removal.

## Governance

Constitution supersedes all other practices. Amendments require:
- Documented rationale for change
- Update to all dependent templates (plan, spec, tasks)
- Migration plan for existing gallery entries if applicable
- Version bump following semantic versioning

All PRs/reviews MUST verify compliance with principles. Complexity MUST be justified against
simpler alternatives. When principles conflict, Reproducibility-First takes precedence.

For runtime development guidance, refer to agent-specific files (CLAUDE.md for Claude Code,
.github/copilot-instructions.md for GitHub Copilot, etc.).

**Version**: 1.0.0 | **Ratified**: 2025-10-03 | **Last Amended**: 2025-10-03
