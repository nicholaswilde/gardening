# Process Add Plant Log Entry with Photo Issue

## Description

This skill instructs the agent on how to use the GitHub CLI (`gh`) to fetch and parse a log entry issue submitted via the `📸 Add Plant Log Entry with Photo` template, download and optimize the photo, insert the log entry and photo reference, and submit a Pull Request.

## Protocol

1. **Fetch Issue Content:**
   Use the `gh` tool to retrieve the issue details:
   ```bash
   gh issue view <issue_number> --json title,body,labels
   ```
2. **Parse Form Fields:**
   Extract the field values from the issue body:
   - **Plant Name / Variety**: E.g., `butterfly-bush` or `Butterfly Bush` (resolve to kebab-case filename, e.g., `butterfly-bush.md`).
   - **Log Date**: E.g., `2026-06-10`
   - **Plant Image**: Parse the URL of the uploaded image.
   - **Observation Notes**: E.g., `Growth accelerating.`
3. **Setup Branch:**
   ```bash
   git checkout -b issue-<issue_number>-log-entry
   ```
4. **Download and Optimize Image:**
   - Determine a unique image filename based on the plant and date, e.g., `<plant_name_kebab>-<log_date>.<ext>`.
   - Download the image to `docs/assets/images/<plant_name_kebab>-<log_date>.<ext>`.
   - Run the optimization script:
     ```bash
     bash scripts/optimize-images.sh
     ```
5. **Insert Log Entry with Photo Reference:**
   - Use the `scripts/add_log_entry.py` script to append the text:
     ```bash
     uv run python3 scripts/add_log_entry.py <plant_name_kebab> "<observation_notes>"
     ```
   - Open `docs/plants/<plant_name_kebab>.md`, locate the new log entry, and append the photo markdown reference or image link under it:
     ```markdown
     * **<log_date>**: <observation_notes>
       ![Update - <log_date>](<../assets/images/<plant_name_kebab>-<log_date>.webp>){ width="400" loading=lazy }
     ```
6. **Run Quality Checks:**
   ```bash
   rumdl check docs/plants/<plant_name_kebab>.md
   task spellcheck-file FILE=docs/plants/<plant_name_kebab>.md
   task linkcheck-file FILE=docs/plants/<plant_name_kebab>.md
   ```
7. **Commit, Push & Create PR:**
   ```bash
   git add docs/plants/<plant_name_kebab>.md docs/assets/images/<plant_name_kebab>-<log_date>.webp
   git commit -m "docs(plants): add log entry and photo for <plant_name_kebab> (Closed #<issue_number>)"
   git push origin issue-<issue_number>-log-entry
   gh pr create --title "docs: Add log entry and photo for <plant_name_kebab> (closes #<issue_number>)" --body "Automatically processed log entry from issue #<issue_number>." --label "garden-log"
   ```
