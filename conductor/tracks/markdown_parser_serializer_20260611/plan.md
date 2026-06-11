# Implementation Plan: Markdown Parser & Serializer

## Phase 1: Setup and Model Implementation [checkpoint: e318099]
- [x] Task: Add `python-frontmatter` and `pydantic` dependencies to `pyproject.toml` and sync environment
- [x] Task: Create `scripts/lib/models.py` defining `PlantProfile` and `LogEntry` models
- [x] Task: Write comprehensive unit tests validating parsing, modification, and saving behaviors
- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Refactor Existing Scripts
- [ ] Task: Refactor `scripts/add_log_entry.py` to use Pydantic models
- [ ] Task: Refactor `scripts/update_origin.py` to use Pydantic models
- [ ] Task: Refactor `scripts/verify_plant.py` to use Pydantic models
- [ ] Task: Refactor `scripts/archive_plant.py` to use Pydantic models
- [ ] Task: Refactor `scripts/build_dashboard.py` to use Pydantic models
- [ ] Task: Run full regression tests to ensure all refactored scripts behave identically to legacy versions
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)
