# Skills Catalog

This catalog details the custom agent skills available in this repository to automate or verify development tasks.

## Available Skills

### 1. [Style Guide Enforcement](./skills/enforce_style.md)

- **Description**: Mandates reading `docs/reference/style-guide.md` and applying exact emoji and
  icon shortcodes (Material Design) for all markdown files and templates.
- **Trigger Condition**: Any time a markdown file or Jinja2 template is created, edited, or refactored.
- **Behavior**: Ensures layout consistency and correct visual branding across the static site.

### 2. [New Plant Profile Generation](./skills/new_plant.md)

- **Description**: Automates creation of a plant profile template using `scripts/new_plant.py`,
  verifying layout, and completing details.
- **Trigger Condition**: When adding a new plant to the repository's documentation database.
- **Command**: `uv run python3 scripts/new_plant.py <plant_name>`
- **Output**: `docs/plants/<plant_name>.md`

### 3. [Add Plant Log Entry](./skills/add_log_entry.md)

- **Description**: Automates adding formatted log entries and observations to a specified plant profile under the log section.
- **Trigger Condition**: When editing an existing plant profile to record dated observations or care events.
- **Command**: `task add-log -- <plant_name> "<observation>"`
- **Behavior**: Runs `scripts/add_log_entry.py` to prepend the formatted log entry below the H2 heading.

### 4. [Plant Profile Verification](./skills/verify_plant.md)

- **Description**: Automates checking and updating botanical taxonomy and metadata (botanical name, family, genus, variety, type) using the Trefle database.
- **Trigger Condition**: When verifying accuracy, resolving placeholder fields, or updating plant profile files.
- **Command**: `task verify-plant -- <path_to_markdown> [--slug <slug>] [--update]`
- **Behavior**: Calls `scripts/verify_plant.py` to check against the Trefle database and optionally write corrections.
