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

### 5. [Get Plant States Retrieval](./skills/get_plant_states.md)

- **Description**: Lists the current/final cultivation states of all plant profiles in the repository.
- **Trigger Condition**: When retrieving the status of all plants in the repository.
- **Command**: `task get-plant-states`
- **Behavior**: Calls `scripts/get_plant_states.py` to retrieve and output the states of all plants.

### 6. [Plant Planting Date Update](./skills/update_plant_date.md)

- **Description**: Automates updating a plant's planting date, corresponding season, and any matching initial log entry dates.
- **Trigger Condition**: When updating the planting date of an existing plant.
- **Command**: `task update-plant-date -- <plant_name> <date>`
- **Behavior**: Calls `scripts/update_plant_date.py` to parse and update the dates.

### 7. [Process New Plant Issue](./skills/process_new_plant_issue.md)

- **Description**: Automatically processes a `🌱 New Plant Entry` issue using the `gh` tool, downloads and WebP-optimizes the image, generates the plant profile page, fetches botanical details from Trefle, updates site navigation, and pushes a PR.
- **Trigger Condition**: When processing an issue to add a brand new plant.
- **Behavior**: Retrieves the issue using `gh`, parses details, calls `scripts/new_plant.py` and `scripts/verify_plant.py`, and opens a pull request.

### 8. [Process Add Plant Log Entry with Photo Issue](./skills/process_log_entry_issue.md)

- **Description**: Automatically processes a `📸 Add Plant Log Entry with Photo` issue using the `gh` tool, downloads/optimizes the photo, appends the new log entry to the plant profile, and opens a PR.
- **Trigger Condition**: When processing an issue to log a dated observation with a photo for an existing plant.
- **Behavior**: Retrieves issue details using `gh`, runs `scripts/add_log_entry.py`, embeds the optimized photo under the log entry, and submits a pull request.

### 9. [Process Add Image to Existing Plant Issue](./skills/process_add_image_issue.md)

- **Description**: Automatically processes a `🖼️ Add Image to Existing Plant` issue using the `gh` tool, downloads/optimizes the image, associates it with the plant profile, and opens a PR.
- **Trigger Condition**: When processing an issue to add/update an image for an existing plant.
- **Behavior**: Retrieves issue using `gh`, downloads and runs `scripts/optimize-images.sh`, updates references in the markdown file, and pushes a PR.

