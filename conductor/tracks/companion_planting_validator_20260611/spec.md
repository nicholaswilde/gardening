# Specification: Companion Planting & Rotation Validator

## Overview
Validate raised bed crops against companion planting compatibility rules and rotation history. Results will be reported via a console task (`task validate-beds`) and injected as a warning section dynamically generated on the site dashboard.

## Functional Requirements
1. **Local Rules Database:** Create a JSON database file `data/companion_rules.json` to store companion compatibility rules (companion/combative families) and crop rotation rules.
2. **Validator Script:** Implement `scripts/validate_beds.py` that reads the rules file, parses raised bed profiles, and verifies the active crops inside.
3. **CLI Task:** Add `task validate-beds` to execute the validation script and print warnings to stdout.
4. **Dashboard Warnings:** Modify the dashboard builder (`scripts/build_dashboard.py`) to run validation and inject warnings dynamically onto the seasonal dashboard page if any issues are found.

## Acceptance Criteria
- Running `task validate-beds` reports compatibilities and warnings to the console.
- Incompatible plants or rotation violations are displayed on the site dashboard.
