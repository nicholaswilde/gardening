# Plant Planting Date Update

## Description

This skill automates updating a plant profile's planting date in the front matter, the Cultivation Status table, and any matching initial log entry dates, as well as calculating the corresponding planting season based on standard definitions using the `scripts/update_plant_date.py` script.

## Protocol

1. **Execute the task:** Run the `update-plant-date` task with the plant name/file and the new planting date (in `YYYY-MM-DD` or `YYYY-MM` format):

    ```bash
    task update-plant-date -- <plant-name> <date>
    ```

    *If `YYYY-MM` is provided, it defaults to the first day of that month (e.g. `YYYY-MM-01`).*

2. **Verify Output:**
    - Open the updated plant profile markdown file.
    - Confirm the front-matter `planted:` field has been updated.
    - Confirm the `Date Planted` and `Season Planted` fields in the Cultivation Status table have been updated.
    - Confirm that any initial log entry matching the old planting date prefix has been updated to the new date.

3. **Validate Quality:**
    - Run spellcheck and linkcheck:

      ```bash
      task spellcheck-file FILE=docs/plants/<plant_name>.md
      task linkcheck-file FILE=docs/plants/<plant_name>.md
      ```

4. **Git Checkpoint:**
    - Commit changes following conventional commits formatting:

      ```bash
      git add docs/plants/<plant_name>.md
      git commit -m "docs(plants): update <plant_name> planting date to <date>"
      ```

## Examples

### Example 1: Updating Mint to June 2025

```bash
task update-plant-date -- mint 2025-06
```

### Example 2: Updating Rosemary to November 1st, 2021

```bash
task update-plant-date -- docs/plants/rosemary.md 2021-11-01
```
