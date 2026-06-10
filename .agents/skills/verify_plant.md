# Plant Profile Verification

## Description

This skill automates the verification of a plant profile's botanical details (such as taxonomy, growth requirements, and variety) against the Trefle database using the custom `scripts/verify_plant.py` script. It highlights copy-pasted placeholders, missing classification fields (botanical name, family, genus), and allows updating profiles automatically.

## Protocol

1. **Locate Target Profile:** Identify the plant profile markdown file under `docs/plants/` that needs verification (e.g., `docs/plants/oregano.md`).
2. **Perform Dry-run Verification:** Execute the verify task on the plant profile to check for discrepancies without modifying the file:

    ```bash
    task verify-plant -- docs/plants/<plant_name>.md
    ```

3. **Handle Search Discrepancies:**
    - If Trefle fails to find the plant by its title or matches an incorrect species (e.g., choosing a wild/rare variety instead of the standard garden variety), supply the specific Trefle slug using the `--slug` flag:

      ```bash
      task verify-plant -- docs/plants/<plant_name>.md --slug <trefle-slug>
      ```

    - Search for standard garden slugs when needed (e.g., `capsicum-annuum` for peppers, `solanum-lycopersicum` for tomatoes, `thymus-vulgaris` for thyme, `coriandrum-sativum` for cilantro, `petroselinum-crispum` for parsley).

4. **Update Profile:** If discrepancies are found or frontmatter is missing taxonomy, update the profile automatically by appending the `--update` flag:

    ```bash
    task verify-plant -- docs/plants/<plant_name>.md [--slug <trefle-slug>] --update
    ```

5. **Verify Changes:**
    - Open the updated markdown file and verify the layout.
    - Check the Admonition block to ensure the variety is correctly set and not a copy-paste placeholder like Rosemary's `[e.g., Tuscan Blue, Arp]`.
    - Ensure type formatting is correct (e.g., `Vegetable` instead of `Perennial Herb` for crops).

6. **Validate Quality:** Compile the static site and run linting/spelling checks:

    ```bash
    task build
    task spellcheck-file FILE=docs/plants/<plant_name>.md
    ```

7. **Git Checkpoint:** Commit the changes with a conventional commit message:

    ```bash
    git add docs/plants/<plant_name>.md
    git commit -m "docs(plants): verify and enrich <plant_name> details with Trefle"
    ```

## Examples

### Example 1: Verifying and updating Oregano

- File: `docs/plants/oregano.md`
- Command:

  ```bash
  task verify-plant -- docs/plants/oregano.md --update
  ```

### Example 2: Forcing a specific slug for Poblano Pepper

- File: `docs/plants/poblano-pepper.md`
- Command:

  ```bash
  task verify-plant -- docs/plants/poblano-pepper.md --slug capsicum-annuum --update
  ```
