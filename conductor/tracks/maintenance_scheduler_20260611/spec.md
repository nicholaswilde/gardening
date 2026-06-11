# Specification: Maintenance Scheduler

## Overview
Generate a maintenance schedule for active crops based on care intervals parsed from plant frontmatter/metadata and historical logs. The output will be presented as a standalone markdown file (`docs/schedule.md`) linked from the home page.

## Functional Requirements
1. **Interval Parsing:** Parse active plant profiles to extract care intervals from frontmatter metadata (e.g., watering or fertilization rules).
2. **Log-aware Scheduling:** Read dated logs to determine the last date an action was performed, calculating the next scheduled date.
3. **Markdown Output:** Generate `docs/schedule.md` listing upcoming maintenance tasks grouped by week/date.
4. **CLI Integration:** Provide a Taskfile task (`task schedule`) that executes the generator python script `scripts/generate_schedule.py`.

## Acceptance Criteria
- Running `task schedule` successfully generates `docs/schedule.md`.
- Next task dates are correctly calculated by applying intervals to the last logged actions.
