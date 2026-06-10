# New Plant Profile Generation

## Description

This skill automates the creation and initialization of a new plant documentation page using the custom
`scripts/new_plant.py` script. It ensures that new plant profiles are placed in the correct directory,
follow the required styling conventions, and have their metadata correctly initialized.

## Protocol

1. **Validate Input:** Ensure a valid plant name in kebab-case format (e.g., `poblano-pepper`) is provided.
2. **Generate Profile Template:** Execute the python scaffolding script with the plant name:

    ```bash
    uv run python3 scripts/new_plant.py <plant_name>
    ```

3. **Verify File Creation:** Confirm that the file `docs/plants/<plant_name>.md` has been successfully created.
4. **Populate Details:** Open `docs/plants/<plant_name>.md` and fill in the missing details:
    - **Tags:** Update tags list in the front-matter (e.g., `herb`, `annual`, `perennial`, `active`, etc.).
    - **Location:** Update the location in front-matter to match the bed or container name.
    - **Type & Variety:** Specify the botanical type and variety in the metadata block.
    - **Cultivation Details:** Fill in the Location and Origin attributes.
    - **Notes:** Fill in sun and soil requirements.
5. **Update Navigation Config:** Open `zensical.toml` and add the new plant to the `Plants` list under `[[project.nav]]` in alphabetical order, mapping the display title to the plant profile path (e.g. `{ "Mint" = "plants/mint.md" }`).
6. **Run Quality Checks:** Check for formatting, spelling, and link integrity:

    ```bash
    rumdl check docs/plants/<plant_name>.md
    task spellcheck-file FILE=docs/plants/<plant_name>.md
    task linkcheck-file FILE=docs/plants/<plant_name>.md
    ```

    If any lint issues are found, resolve them or run:

    ```bash
    rumdl check --fix docs/plants/<plant_name>.md
    ```

7. **Git Checkpoint:** Stage and commit the new plant profile and the updated zensical.toml with a conventional commit message:

    ```bash
    git add docs/plants/<plant_name>.md zensical.toml
    git commit -m "docs(plants): add <plant_name> profile and update navigation"
    ```

## Examples

### Example 1: Creating a poblano pepper profile

- Kebab-case plant name: `poblano-pepper`
- Command:

  ```bash
  uv run python3 scripts/new_plant.py poblano-pepper
  ```

- Output file: `docs/plants/poblano-pepper.md`
- Verify & populate details, check format, commit.
