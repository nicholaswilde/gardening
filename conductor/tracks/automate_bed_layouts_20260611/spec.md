# Specification: Automated Bed Layouts

## Overview

Build a Python script and command line interface to automatically parse crop placements from plant markdown files,
construct grid representations of beds, apply Catppuccin Mocha styles and emojis, and inject the layout diagrams
dynamically into raised bed profile documents.

## Functional Requirements

1. **Plant Placement Parsing:**
   * Scan active plant files in `docs/plants/*.md`.
   * Extract target raised bed (e.g., `location: raised-bed-2` in frontmatter) and coordinates (e.g.,
     `grid_position: [1, 3]`).
2. **Layout Grid Validation:**
   * Support a standard 2x4 grid size for raised beds (Row 1-2, Column 1-4).
   * Validate that all plant coordinates are within grid boundaries.
   * Check for placement collisions (more than one active plant in the same coordinate).
3. **Diagram Compilation:**
   * Build a `flowchart TD` Mermaid diagram matching the project style guide.
   * Auto-fill unmapped coordinates with a Fallow/Compost node labeled `"🟫 Fallow / Compost<br>(Empty)"`.
   * Prepend active plant labels with a representative emoji (e.g., 🍅, 🌶️, 🌿) matching their common name.
   * Apply Catppuccin Mocha styling classes (Lavender border, Surface0 fill, Green active stroke, dashed Surface2
     empty stroke).
4. **Link Injection:**
   * Embed click events on active crop nodes linking to their relative plant profiles (e.g., `../plants/oregano.md`).
   * Read target bed profiles (e.g., `docs/beds/raised-bed-2.md`) and automatically replace the Mermaid block
     enclosed in `<!-- BED_LAYOUT_START -->` and `<!-- BED_LAYOUT_END -->` markers.
5. **Task Integration:**
   * Register a task `generate-layouts` in `Taskfile.yaml` to run the compiler script.

## Non-Functional Requirements

* **Robust Error Handling:** Raise descriptive errors for overlaps, missing files, or incorrect coordinates.
* **Unit Testing:** Ensure full coverage (>80%) of parsing, validation, and layout compilation logic.
