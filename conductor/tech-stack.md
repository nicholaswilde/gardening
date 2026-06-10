# Tech Stack

## Core Technologies

- **Python**: >=3.14 (main programming language for build scripts and templating)
- **Zensical**: >=0.0.44 (static site engine and documentation formatter)
- **Jinja2**: >=3.1.6 (templating engine for generating plant/bed files)
- **Trefle API**: Used to lookup and verify botanical taxonomy and metadata (e.g., scientific name, family, genus,
  preferred light, soil pH)
- **GitHub CLI (`gh`)**: Used to interface with GitHub to manage issues, pull requests, and automate repository workflows.

## Architecture & Data Flow

- **Data Source**: Markdown files stored in `docs/` folder representing plants, containers, beds, and reference sheets.
- **Build Output**: Static HTML generated locally/CI to `site/` folder, using Zensical configuration defined in `zensical.toml`.
- **Automation**: Task-based build workflows using Python runner scripts.
- **External API Integration**: Query and lookup plant information from the Trefle API using the `TREFLE_TOKEN`
  environment variable defined in the `.env` file.
- **GitHub Integration**: Interface with GitHub via the `gh` tool to manage issues (e.g., new plant submissions, log entries, image uploads) and pull requests (e.g., branches, review status, merging) for automated and manual repository tracking.
