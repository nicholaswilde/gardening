# Scripts Registry

This document lists the utility and automation scripts available in the `scripts/` directory of this repository.

## Scripts Overview

| Script | Language | Purpose | Usage |
|---|---|---|---|
| `add_log_entry.py` | Python 3 | Appends a formatted observation log to a plant profile | `python3 scripts/add_log_entry.py <plant-name> "Message"` |
| `build_dashboard.py` | Python 3 | Generates the seasonal planting dashboard | `python3 scripts/build_dashboard.py` |
| `generate_typos_config.py` | Python 3 | Generates the `_typos.toml` whitelist configuration from `dictionary.txt` | `python3 scripts/generate_typos_config.py` |
| `new_bed.py` | Python 3 | Scaffolds a new raised bed profile template | `python3 scripts/new_bed.py <bed-name>` |
| `new_plant.py` | Python 3 | Scaffolds a new plant profile template | `python3 scripts/new_plant.py <plant-name>` |
| `optimize-images.sh` | Bash | Converts `.jpg` images to `.webp` and optimizes `.png` images in-place | `bash scripts/optimize-images.sh` |

---

## Detailed Specifications

### 1. `add_log_entry.py`

- **Path**: `scripts/add_log_entry.py`
- **Description**: Automatically appends a new dated log entry to the `## :memo: Log & Observations`
  section of a specified plant profile while preserving reverse chronological order.
- **Arguments**:
    - `plant_name`: Name of the plant (e.g. `rosemary`)
    - `observation`: The log entry message (e.g. `Growth accelerating`)
- **Dependencies**: `sys`, `os`, `datetime`

### 2. `build_dashboard.py`

- **Path**: `scripts/build_dashboard.py`
- **Description**: Parses all Markdown files in `docs/plants/`, extracts their front-matter metadata
  (specifically `title` and `season`), and builds an optimal planting schedule sorted chronologically by season.
- **Output**: `docs/seasonal-dashboard.md`
- **Dependencies**: `os`, `re`, `collections.defaultdict`

### 2. `generate_typos_config.py`

- **Path**: `scripts/generate_typos_config.py`
- **Description**: Reads allowed spellings from `dictionary.txt`, sorts/deduplicates them, and writes
  a whitelisted configuration file to extend typos exclusions and extend words.
- **Output**: `_typos.toml`
- **Dependencies**: `os`

### 3. `new_bed.py`

- **Path**: `scripts/new_bed.py`
- **Description**: Generates a new raised bed Markdown document from a Jinja2 template.
- **Arguments**:
    - `filename`: Name of the new bed (e.g. `raised-bed-4`)
- **Output**: `docs/beds/<filename>.md`
- **Dependencies**: `sys`, `os`, `datetime`, `jinja2`

### 4. `new_plant.py`

- **Path**: `scripts/new_plant.py`
- **Description**: Generates a new plant Markdown profile from a Jinja2 template.
- **Arguments**:
    - `filename`: Name of the new plant (e.g. `poblano-pepper`)
- **Output**: `docs/plants/<filename>.md`
- **Dependencies**: `sys`, `os`, `datetime`, `jinja2`

### 5. `optimize-images.sh`

- **Path**: `scripts/optimize-images.sh`
- **Description**: Scans `docs/assets/images/` to process JPEG photos (converts to lossy WebP and removes
  source JPEGs) and PNG graphics (optimizes in-place using oxipng).
- **External CLI Dependencies**: `cwebp` (from webp package), `oxipng` (from cargo/apt)
