# Plant States Retrieval

## Description

This skill allows listing the cultivation states of all plant profiles currently present in the gardening repository using the `scripts/get_plant_states.py` script.

## Protocol

1. **Execute the task:** Run the `get-plant-states` task:

    ```bash
    task get-plant-states
    ```

2. **Verify Output:**
    - The output will display a table containing the filename, plant title, and current/final state for each plant profile under `docs/plants/`.
    - Active plants will show a state prefixed with `Current:`.
    - Archived plants will show a state prefixed with `Final:`.

## Examples

### Example: Running the task

```bash
task get-plant-states
```
