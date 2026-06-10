# Add Plant Log Entry

## Description

This skill outlines the protocol for adding dated log entries and observations to a specific plant profile
under the `## :memo: Log & Observations` section. It ensures consistent date formatting and
chronological sorting (newest entries at the top).

## Protocol

1. **Locate File:** Identify the target plant file path: `docs/plants/<plant_name>.md`.
2. **Verify Section:** Open the file and verify the presence of the `## :memo: Log & Observations` heading.
3. **Draft Entry:** Construct the log entry using the current date:
    - Format: `* **YYYY-MM-DD**: <Detailed observations, growth updates, or actions taken>`
4. **Insert Entry:** Insert the entry directly below the `## :memo: Log & Observations` heading
   (or above any existing log entries). This preserves the reverse chronological order (newest at the top).
5. **Run Quality Checks:** Validate formatting using the markdown linter:

    ```bash
    rumdl check docs/plants/<plant_name>.md
    ```

6. **Git Checkpoint:** Stage and commit the updated plant profile with a conventional commit message:

    ```bash
    git add docs/plants/<plant_name>.md
    git commit -m "docs(plants): log observations for <plant_name>"
    ```

## Examples

### Example 1: Adding an observation for Poblano Pepper

- Plant name: `poblano-pepper`
- Date: `2026-06-09`
- Observation: "Flowering has begun. Spotted first tiny peppers forming on lower branches."
- Draft: `* **2026-06-09**: Flowering has begun. Spotted first tiny peppers forming on lower branches.`
- Insertion:

  ```diff
   ## :memo: Log & Observations

  +* **2026-06-09**: Flowering has begun. Spotted first tiny peppers forming on lower branches.
   * **2026-05-15**: Transplanted into raised bed.
  ```
