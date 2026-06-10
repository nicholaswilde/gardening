# Process Add Image to Existing Plant Issue

## Description

This skill instructs the agent on how to use the GitHub CLI (`gh`) to fetch and parse an image upload issue submitted via the `🖼️ Add Image to Existing Plant` template, download/optimize the image, replace or add it to the plant profile, and submit a Pull Request.

## Protocol

1. **Fetch Issue Content:**
   Use the `gh` tool to retrieve the issue details:
   ```bash
   gh issue view <issue_number> --json title,body,labels
   ```
2. **Parse Form Fields:**
   Extract the field values from the issue body:
   - **Plant Name / Variety**: E.g., `butterfly-bush` or `Butterfly Bush` (resolve to kebab-case filename, e.g., `butterfly-bush.md`).
   - **Plant Image**: Parse the URL of the uploaded image.
   - **Additional Notes**: E.g., `replace primary photo`.
3. **Setup Branch:**
   ```bash
   git checkout -b issue-<issue_number>-add-image
   ```
4. **Download and Optimize Image:**
   - If the request is to replace/update the primary image, download the image to `docs/assets/images/<plant_name_kebab>.<ext>`, overwriting the existing image format (the optimization script will convert to `.webp` while preserving EXIF metadata).
   - If the request is to add a new image without replacing the primary one, download it to `docs/assets/images/<plant_name_kebab>-updated.<ext>`.
   - Run the optimization script:
     ```bash
     bash scripts/optimize-images.sh
     ```
5. **Update Plant Profile References:**
   - Extract the "date taken" from the optimized image file using:
     ```bash
     uv run python3 scripts/get_image_date.py docs/assets/images/<image_file>
     ```
   - Wrap the image reference in a date-labeled tab:
     ```markdown
     === "YYYY-MM-DD"

         ![plant-name][1]{ width="400" loading=lazy }
     ```
     Use the extracted date for `YYYY-MM-DD`. If there are multiple images, place them in tabs sorted in reverse chronological order (most recent first).
   - If it's a replacement primary image, ensure the markdown reference at the bottom of `docs/plants/<plant_name_kebab>.md` maps to the new `.webp` file:
     `[1]: <../assets/images/<plant_name_kebab>.webp>`
   - If it's an additional image, define a new reference (e.g., `[2]`, `[3]`) and map it to the respective WebP file.
6. **Run Quality Checks:**
   ```bash
   rumdl check docs/plants/<plant_name_kebab>.md
   task spellcheck-file FILE=docs/plants/<plant_name_kebab>.md
   task linkcheck-file FILE=docs/plants/<plant_name_kebab>.md
   ```
7. **Commit, Push & Create PR:**
   ```bash
   git add docs/plants/<plant_name_kebab>.md docs/assets/images/<plant_name_kebab>.webp
   git commit -m "docs(plants): update/add image for <plant_name_kebab> from issue #<issue_number>"
   git push origin issue-<issue_number>-add-image
   gh pr create --title "docs: Update image for <plant_name_kebab> (closes #<issue_number>)" --body "Automatically processed image update from issue #<issue_number>." --label "image-processing"
   ```
