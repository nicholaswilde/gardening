# Add Plant Log Entry

## Description

This skill outlines the protocol for adding dated log entries and observations to a specific plant profile
under the `## :memo: Log & Observations` section using the automated `scripts/add_log_entry.py` script.

## Protocol

1. **Validate and Review Inputs:** Identify the target plant name (e.g. `rosemary`) and prepare the log observation message. Review the wording of the observation, check for any grammatical issues, typos, or style guidelines, and refine/correct the wording to be clear, professional, and consistent before adding it to the markdown page.
2. **Execute Log Command:** Run the log automation using `go-task`:

    ```bash
    task add-log -- <plant-name> "<Observation message>"
    ```

    *Note: This automatically prepends the log entry with the current date under the correct heading in
    `docs/plants/<plant-name>.md` while preserving reverse chronological order.*
3. **Verify File Update:** Verify the changes in the plant file:

    ```bash
    git diff docs/plants/<plant-name>.md
    ```

4. **Run Quality Checks:** Validate formatting using the markdown linter:

    ```bash
    rumdl check docs/plants/<plant-name>.md
    ```

5. **Git Checkpoint:** Stage and commit the updated plant profile with a conventional commit message:

    ```bash
    git add docs/plants/<plant-name>.md
    git commit -m "docs(plants): log observations for <plant-name>"
    ```

## Examples

### Example 1: Adding an observation for Rosemary

- Plant name: `rosemary`
- Observation: "Growth accelerating. Pinching back the top stems."
- Command:

  ```bash
  task add-log -- rosemary "Growth accelerating. Pinching back the top stems."
  ```

- Output file: `docs/plants/rosemary.md`
