# Implementation Plan: Companion Planting & Rotation Validator

## Phase 1: Create Rules and Validator Logic
- [ ] Task: Create `data/companion_rules.json` with initial companion and rotation rules
- [ ] Task: Create Python script `scripts/validate_beds.py`
- [ ] Task: Write unit tests for rules loading, validation logic, and warnings reporting
- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: CLI Task and Dashboard Warnings
- [ ] Task: Add `validate-beds` task to `Taskfile.yaml`
- [ ] Task: Update `scripts/build_dashboard.py` to run validation and inject warnings into `docs/seasonal-dashboard.md`
- [ ] Task: Run `task dashboard` and verify warnings are generated correctly
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)
