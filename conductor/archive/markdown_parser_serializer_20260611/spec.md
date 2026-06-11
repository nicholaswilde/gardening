# Specification: Markdown Parser & Serializer

## Overview
Establish a unified Markdown parsing and serialization library in `scripts/lib/models.py` using `python-frontmatter` and `Pydantic`. This replaces fragile ad-hoc regex queries across all utility scripts, providing type safety, validating plant metadata, and significantly reducing agent token consumption.

## Functional Requirements
1. **Pydantic Schema Models:** Define schemas representing plant profiles and log entries with proper validation rules (e.g. date formats, allowed status enums, etc.).
2. **Unified Parsing/Serialization:**
   - Use `python-frontmatter` to load markdown files, separating YAML frontmatter from markdown body.
   - Parse admonitions, lists, and tables safely into model fields.
   - Serialize model instances back into style-compliant markdown files.
3. **Refactor Existing Utilities:** Update all existing scripts to load and write pages through the new model interface, completely deleting regex-based replacements:
   - `scripts/add_log_entry.py`
   - `scripts/update_origin.py`
   - `scripts/verify_plant.py`
   - `scripts/archive_plant.py`
   - `scripts/build_dashboard.py`

## Non-Functional Requirements
- **Robust Error Handling:** Throw clean, readable validation errors if a page has corrupted or outdated frontmatter/admonitions.
- **Coverage:** Cover model methods with extensive unit tests.

## Acceptance Criteria
- Unit tests pass for parsing, updating, and saving markdown plant profiles.
- All existing utility scripts run successfully using the new model library with no regression in behavior.
