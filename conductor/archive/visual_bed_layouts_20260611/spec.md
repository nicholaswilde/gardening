# Specification: Visual Bed Layouts

## Overview
Enable visual representation of crop placement within raised beds using Mermaid.js grid/block diagrams. Users should be able to see the layout of a raised bed and click on individual blocks to navigate directly to the respective plant profiles.

## Functional Requirements
1. **Mermaid.js Integration:** Embed Mermaid.js diagrams directly within raised bed markdown profiles (e.g., `docs/beds/raised-bed-1.md`).
2. **Interactive Blocks:** Ensure each block in the diagram representing a planted cell is clickable and links to the correct active plant profile file path (e.g., `../plants/sungold-tomato.md`).
3. **Target Scope:** This feature will support raised beds only. Pot-based containers will not feature layouts.

## Non-Functional Requirements
- **Consistency:** Ensure Mermaid.js styling matches the dark/light themes of the static site.

## Acceptance Criteria
- Mermaid.js layout displays successfully on the static site.
- Plant blocks are clickable and successfully navigate to the corresponding plant profile.
