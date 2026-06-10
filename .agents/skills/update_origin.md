# Plant Origin Update

## Description

This skill automates updating a plant profile's origin in both the top-level example admonition block (using standard Material Design icons) and the Cultivation Status table using the `scripts/update_origin.py` script.

## Protocol

1. **Identify standard origin mapping:** Look up the desired origin in the `docs/reference/style-guide.md` file under **Origin Mappings** to select the standard term (e.g. `Nursery Start` or `Living herb`).
2. **Execute the task:** Run the `update-origin` task with the target plant file and the origin type keyword:

    ```bash
    task update-origin -- docs/plants/<plant_name>.md <origin-type>
    ```

    Standard origin types and aliases accepted by the script:
    - `seed-indoor` (Seed (Indoor Start))
    - `seed-direct` (Seed (Direct Sow))
    - `nursery-start` (Nursery Start)
    - `bare-root` (Bare Root)
    - `cutting` (Cutting / Clone)
    - `division` (Division)
    - `volunteer` (Volunteer)
    - `gifted-transplant` (Gifted transplant)
    - `living-herb` (Living herb)

3. **Verify the change:**
    - Open the modified markdown file.
    - Confirm the admonition block has the double-spaced entry with the correct icon (e.g. `**:material-storefront-outline: Origin:** Nursery Start`).
    - Confirm the Cultivation Status table has the updated origin row.

4. **Validate and commit:**
    - Run spellcheck and linkcheck:

      ```bash
      task spellcheck-file FILE=docs/plants/<plant_name>.md
      task linkcheck-file FILE=docs/plants/<plant_name>.md
      ```

    - Commit changes following conventional commits formatting:

      ```bash
      git add docs/plants/<plant_name>.md
      git commit -m "style(plants): update <plant_name> origin to <origin>"
      ```

## Examples

### Example 1: Updating Oregano to Nursery Start

```bash
task update-origin -- oregano nursery-start
```

### Example 2: Updating Thyme to Gifted transplant

```bash
task update-origin -- docs/plants/thyme.md gifted-transplant
```
