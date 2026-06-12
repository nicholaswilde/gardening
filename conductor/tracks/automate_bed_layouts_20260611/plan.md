# Implementation Plan: Automated Bed Layouts

## Phase 1: Models Extension and Generator Logic [checkpoint: ae64e26]

* [x] Task: Extend Pydantic models in `scripts/lib/models.py` to support `grid_position` and bed layout metadata (6ccddac)
* [x] Task: Create layout generation core in `scripts/lib/layout_generator.py` to compile the grids to Mermaid syntax (7aa7a27)
* [x] Task: Write unit tests in `tests/test_layout_generator.py` for grid validation, collision checks, and Mermaid generation (7aa7a27)
* [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md) (ae64e26)

## Phase 2: CLI Script and Taskfile Integration

* [x] Task: Create CLI script `scripts/generate_layouts.py` to scan plant profiles and inject diagrams into bed profiles (f4057e5)
* [ ] Task: Add the `generate-layouts` task to `Taskfile.yaml` and add layout markers to bed markdown profiles
* [ ] Task: Run `task generate-layouts` to verify automated generation and links validation
* [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)
