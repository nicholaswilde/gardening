# Tech Stack

## Core Technologies
- **Python**: >=3.14 (main programming language for build scripts and templating)
- **Zensical**: >=0.0.44 (static site engine and documentation formatter)
- **Jinja2**: >=3.1.6 (templating engine for generating plant/bed files)

## Architecture & Data Flow
- **Data Source**: Markdown files stored in `docs/` folder representing plants, containers, beds, and reference sheets.
- **Build Output**: Static HTML generated locally/CI to `site/` folder, using Zensical configuration defined in `zensical.toml`.
- **Automation**: Task-based build workflows using Python runner scripts.
