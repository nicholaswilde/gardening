# Plant Archiving Workflow

## Description

This skill automates the archiving of a plant profile (e.g. when a crop is removed or harvested) using the `scripts/archive_plant.py` script. The process renames the plant profile and its associated image, updates all markdown links, shifts cultivation status to final state, and relocates the navigation reference to the Archive section of `zensical.toml`.

## Protocol

1. **Perform Archiving Command:** Run the `archive-plant` task with the plant name, the target archive year, the removal date, the final status state, and a brief outcome description:

    ```bash
    task archive-plant -- <plant-name> <year> <removed-date> <final-state> "<outcome>"
    ```

    - **`<plant-name>`**: Basename of the markdown profile (e.g. `cilantro` or `sage-2025`).
    - **`<year>`**: Year of the crop season to archive under (e.g. `2025`).
    - **`<removed-date>`**: YYYY-MM-DD when the crop was removed/cleared (e.g. `2026-05-10`).
    - **`<final-state>`**: Outcome status (options: `Harvested / Cleared`, `Composted`, `Failed`, `Relocated`).
    - **`"<outcome>"`**: Brief description of outcome or yield (e.g. `"High yield. Used in pestos."`).

2. **Verify File Changes:**
    - Confirm the profile was renamed to `docs/plants/<plant-name>-<year>.md`.
    - Confirm the image file was renamed to `docs/assets/images/<plant-name>-<year>.<ext>`.
    - Open `docs/plants/<plant-name>-<year>.md` and verify:
      - Frontmatter: contains `archived` tag and `removed: <date>` field.
      - Admonition block: holds the updated origin icon and value.
      - Cultivation Status table: holds `Final State`, `Date Removed`, and `Outcome` rows.
      - Image Links: updated to point to the new image name.

3. **Verify Configuration Change:**
    - Open `zensical.toml` and confirm the plant entry was removed from the active `Plants` array and added to the `Archive -> <year>` array in alphabetical order.

4. **Validate Quality:**
    - Run spellcheck and link checks:

      ```bash
      task spellcheck
      task linkcheck-offline
      ```

5. **Git Checkpoint:** Stage and commit the renamed profile, renamed image, and zensical config:

    ```bash
    git add docs/plants/<plant-name>-<year>.md docs/assets/images/<plant-name>-<year>.* zensical.toml
    git commit -m "style(plants): archive <plant-name> for <year>"
    ```

## Examples

### Example 1: Archiving Sage for 2025

```bash
task archive-plant -- sage 2025 2026-05-10 "Harvested / Cleared" "Excellent yield; leaves dried for tea."
```
