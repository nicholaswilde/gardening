# Markdown Page Deletion

## Description

This skill outlines the protocol for deleting or removing markdown files (e.g. plant profiles or bed descriptions) from the repository. Deleting files can result in broken internal links or navigation configurations, so running `lychee` is required to ensure repository link integrity.

## Protocol

1. **Delete the target file:** Remove the markdown file using `git rm`:

    ```bash
    git rm docs/plants/<plant_name>.md
    ```

2. **Clean up navigation references:** Search for any references to the deleted file inside configuration files (such as `zensical.toml` or `mkdocs.yml`) and remove them.

3. **Check for dead references (Link Check):** Run the offline link check on the entire repository to verify that no other markdown page is still linking to the deleted file:

    ```bash
    task linkcheck-offline
    ```

    *If any broken links are reported, open those files and either remove the broken links or update them to point to a valid target.*

4. **Git Checkpoint:** Commit the changes with a conventional commit message:

    ```bash
    git commit -m "docs(plants): remove <plant_name> profile"
    ```

## Examples

### Example 1: Deleting an obsolete plant profile

- Obsolete file: `docs/plants/mint.md`
- Commands:

  ```bash
  git rm docs/plants/mint.md
  task linkcheck-offline
  git commit -m "docs(plants): remove mint profile"
  ```
