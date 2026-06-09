# :art: Style Guide & Iconography

This document serves as the single source of truth for the visual language, typography, and iconography used across the Gardening repository. 

> **🤖 Instructions for AI Agents:**
> When generating, refactoring, or updating markdown pages in this repository, you **MUST** strictly adhere to the iconography mapping below. Do not invent new icons for these established fields. Always use standard GitHub emoji shortcodes (e.g., `:seedling:`) for H1/H2 headings, and Material Design shortcodes (e.g., `:material-leaf:`) for admonition properties.

## 📄 Standard Markdown Headings (Emojis)

Whenever creating top-level (`#`) or secondary (`##`) headings, prepend the title with the following emojis based on the context:

| Context / Page Type | Emoji Shortcode | Example |
| :--- | :--- | :--- |
| **Plant Profiles** (H1) | `:seedling:` | `# :seedling: Sungold Tomato` |
| **Hardware Pages** (H1) | `:seedling:` | `# :seedling: Click & Grow` |
| **Irrigation Systems** (H1) | `:shower:` | `# :shower: Irrigation` |
| **Active/Current State** (H2) | `:clipboard:` | `## :clipboard: Active Pods` |
| **Inventory Tracking** (H2) | `:package:` | `## :package: Pod Inventory` |
| **Hardware Logs** (H2) | `:wrench:` | `## :wrench: Maintenance & Hardware` |
| **Future Planning** (H2) | `:rocket:` | `## :rocket: Planned Upgrades` |
| **Water Zones** (H2) | `:droplet:` | `## :droplet: Zone Configuration` |

## 🛠️ Metadata & Admonitions (Material Icons)

When listing physical properties, infrastructure states, or botanical taxonomy (typically inside MkDocs admonition blocks), prepend the bolded label with the following Material Design icons:

### Botanical & Taxonomic
* **Type:** `:material-leaf:` (e.g., `**:material-leaf: Type:** Herb`)
* **Variety:** `:material-dna:` (e.g., `**:material-dna: Variety:** Winter Gem`)
* **Origin:** `:material-seed-outline:` (e.g., `**:material-seed-outline: Origin:** Nursery`)

### Hardware & Infrastructure
* **Model:** `:material-barcode:` (e.g., `**:material-barcode: Model:** Rain Bird`)
* **Material:** `:material-fence:` (e.g., `**:material-fence: Material:** Redwood`)
* **Dimensions:** `:material-ruler-square:` (e.g., `**:material-ruler-square: Dimensions:** 4x8`)
* **Volume:** `:material-bucket-outline:` (e.g., `**:material-bucket-outline: Volume:** 5 Gal`)
* **Drainage:** `:material-filter-outline:` (e.g., `**:material-filter-outline: Drainage:** Gravel`)
* **Constructed:** `:material-calendar-check-outline:` (e.g., `**:material-calendar-check-outline: Constructed:** 2017`)

### State & Location
* **Status:** `:material-list-status:` (e.g., `**:material-list-status: Status:** Active`)
* **Location:** `:material-map-marker-outline:` (e.g., `**:material-map-marker-outline: Location:** Patio`)
* **Station / Zone:** `:material-view-grid-outline:` (e.g., `**:material-view-grid-outline: Station:** Bed 2`)

### Projects & Engineering
* **Project Name:** `:material-flask-outline:` (e.g., `**:material-flask-outline: Project:** Telemetry`)
* **Target Integration:** `:material-connection:` (e.g., `**:material-connection: Target Integration:** MQTT`)

## 🎨 Admonition Blocks

When building summary blocks at the top of pages, utilize the built-in MkDocs admonitions formatted with the standard icons:

```text
!!! info "Botanical Profile"
    **:material-leaf: Type:** Pepper  
    **:material-dna: Variety:** Poblano
```

### 2. Add it to the Navigation

To ensure it compiles correctly and is accessible on your site, update the `Reference` block in your `zensical.toml` file to include the new page:

```toml
[[project.nav]]
Reference = [
  { "Future" = "reference/future.md" },
  { "Style Guide" = "reference/style-guide.md" },
  { "Development" = "reference/development.md" }
]
```

