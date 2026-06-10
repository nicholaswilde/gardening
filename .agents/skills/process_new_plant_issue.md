# Process New Plant Issue

## Description

This skill instructs the agent on how to use the GitHub CLI (`gh`) to fetch and parse a new plant issue submitted via the `🌱 New Plant Entry` template, automatically generate the plant profile, download/optimize the image, verify taxonomy, and submit a Pull Request.

## Protocol

1. **Fetch Issue Content:**
   Use the `gh` tool to retrieve the issue description and metadata:
   ```bash
   gh issue view <issue_number> --json title,body,labels
   ```
2. **Parse Form Fields:**
   Extract the field values from the issue body:
   - **Plant Name / Variety**: E.g., `Wild Strawberry`
   - **Planting Date**: E.g., `2026-06-10`
   - **Source Type**: E.g., `Seed (Indoor Start)` (must match one of the standard origin types in `update_origin.py`)
   - **Garden Location / Zone**: E.g., `Indoor Shelf`
   - **Plant Image**: Parse the URL of the uploaded image (e.g., from `https://github.com/user-attachments/...` or `https://github.com/.../assets/...`).
   - **Initial Care Notes**: E.g., `Planted in peat moss.`
3. **Setup Branch:**
   Create a new git branch for the issue:
   ```bash
   git checkout -b issue-<issue_number>-new-plant
   ```
4. **Generate Profile Template:**
   Convert the plant name to kebab-case (e.g., `wild-strawberry`) and run the generation script:
   ```bash
   uv run python3 scripts/new_plant.py <plant_name_kebab>
   ```
5. **Download and Optimize Image:**
   - Download the image from the parsed URL using `curl` or `wget` to `docs/assets/images/<plant_name_kebab>.<ext>` (e.g., `.png` or `.jpg`).
   - Run the image optimization script to convert to optimized `.webp` (preserving EXIF metadata):
     ```bash
     bash scripts/optimize-images.sh
     ```
   - Extract the "date taken" from the optimized image file:
     ```bash
     uv run python3 scripts/get_image_date.py docs/assets/images/<plant_name_kebab>.webp
     ```
   - In `docs/plants/<plant_name_kebab>.md`, ensure the image is inside a tab labeled with this extracted date (e.g. `=== "YYYY-MM-DD"`).
   - Ensure the image is referenced correctly at the bottom of the new file:
     `[1]: <../assets/images/<plant_name_kebab>.webp>`
6. **Populate Metadata and Details:**
   Open `docs/plants/<plant_name_kebab>.md` and update:
   - **Tags/Frontmatter**:
     - Set `planted` to the parsed date.
     - Set `location` to the parsed location.
   - **Origin**: Run the update script to apply standard icons/terms:
     ```bash
     uv run python3 scripts/update_origin.py <plant_name_kebab> "<source_type>"
     ```
   - **Verify with Trefle API**:
     Verify and auto-fill botanical metadata:
     ```bash
     uv run python3 scripts/verify_plant.py docs/plants/<plant_name_kebab>.md --update
     ```
   - **Log Section**:
     Ensure the initial log matches the planting date and initial notes.
7. **Add to Navigation:**
   Add the new plant to `zensical.toml` under `[[project.nav]]` `Plants` section in alphabetical order.
8. **Run Quality Checks:**
   ```bash
   rumdl check docs/plants/<plant_name_kebab>.md
   task spellcheck-file FILE=docs/plants/<plant_name_kebab>.md
   task linkcheck-file FILE=docs/plants/<plant_name_kebab>.md
   ```
9. **Commit, Push & Create PR:**
   ```bash
   git add docs/plants/<plant_name_kebab>.md docs/assets/images/<plant_name_kebab>.webp zensical.toml
   git commit -m "feat(plants): add <plant_name> from issue #<issue_number>"
   git push origin issue-<issue_number>-new-plant
   gh pr create --title "feat: Add <plant_name> (closes #<issue_number>)" --body "Automatically processed from issue #<issue_number> using Antigravity." --label "new-plant"
   ```
