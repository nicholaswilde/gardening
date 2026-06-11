#!/usr/bin/env python3
# scripts/update_plant_date.py

import os
import sys
import re
from datetime import datetime

def get_season_planted(month):
    if month in (2, 3):
        return "Early Spring"
    elif month == 4:
        return "Mid-Spring"
    elif month == 5:
        return "Late Spring"
    elif month == 6:
        return "Early Summer"
    elif month in (7, 8):
        return "Mid-Summer"
    elif month == 9:
        return "Late Summer"
    elif month == 10:
        return "Early Fall"
    elif month == 11:
        return "Mid-Fall"
    elif month in (12, 1):
        return "Late Fall / Winter"
    return "Unknown"

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 scripts/update_plant_date.py <plant-name-or-path> <date>")
        print("Example: python3 scripts/update_plant_date.py oregano 2021-11-01")
        print("Example: python3 scripts/update_plant_date.py docs/plants/mint.md 2025-06")
        sys.exit(1)

    plant_arg = sys.argv[1].strip()
    date_arg = sys.argv[2].strip()

    project_root = "/home/nicholas/git/nicholaswilde/gardening"

    # Resolve markdown path
    if plant_arg.endswith(".md"):
        filepath = os.path.abspath(plant_arg)
    else:
        # Standardize kebab-case name
        plant_name = plant_arg.replace(".md", "")
        filepath = os.path.join(project_root, "docs", "plants", f"{plant_name}.md")

    if not os.path.exists(filepath):
        print(f"Error: Plant profile '{filepath}' not found.")
        sys.exit(1)

    # Parse and validate new date
    # Support YYYY-MM-DD or YYYY-MM
    new_date = None
    new_season = None
    
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date_arg):
        new_date = date_arg
        try:
            dt = datetime.strptime(new_date, "%Y-%m-%d")
            new_season = get_season_planted(dt.month)
        except ValueError as e:
            print(f"Error: Invalid date format: {e}")
            sys.exit(1)
    elif re.match(r'^\d{4}-\d{2}$', date_arg):
        new_date = f"{date_arg}-01"
        try:
            dt = datetime.strptime(new_date, "%Y-%m-%d")
            new_season = get_season_planted(dt.month)
        except ValueError as e:
            print(f"Error: Invalid date format: {e}")
            sys.exit(1)
    else:
        print("Error: Date must be in YYYY-MM-DD or YYYY-MM format.")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract old date from front matter
    old_date = None
    fm_planted_match = re.search(r'^planted:\s*([\d-]+)', content, re.MULTILINE)
    if fm_planted_match:
        old_date = fm_planted_match.group(1).strip()

    # Modify content
    modified = False

    # 1. Update front matter
    if fm_planted_match:
        content = content.replace(f"planted: {old_date}", f"planted: {new_date}")
        modified = True
        print(f"- Updated front matter 'planted' field: {old_date} -> {new_date}")
    else:
        # If not present in front matter, insert it before botanical_name or at the end of front matter
        fm_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
        if fm_match:
            orig_fm = fm_match.group(1)
            new_fm = orig_fm + f"\nplanted: {new_date}"
            content = content.replace(orig_fm, new_fm)
            modified = True
            print(f"- Added 'planted' field to front matter: {new_date}")

    # 2. Update Date Planted in Cultivation Status table
    table_date_pattern = r'(\|\s*\*\*Date Planted\*\*\s*\|\s*)[^|\n]+'
    if re.search(table_date_pattern, content):
        content = re.sub(table_date_pattern, rf'\g<1>{new_date} |', content)
        modified = True
        print(f"- Updated Date Planted in table: {new_date}")

    # 3. Update Season Planted in Cultivation Status table
    table_season_pattern = r'(\|\s*\*\*Season Planted\*\*\s*\|\s*)[^|\n]+'
    if re.search(table_season_pattern, content):
        content = re.sub(table_season_pattern, rf'\g<1>{new_season} |', content)
        modified = True
        print(f"- Updated Season Planted in table: {new_season}")

    # Update Date Planted in admonition block
    admon_date_pattern = r'(\*\*(?::material-[a-z-]+:\s*)?Date Planted:\*\*\s*)[^\n]+'
    if re.search(admon_date_pattern, content):
        content = re.sub(admon_date_pattern, rf'\g<1>{new_date} ({new_season})', content)
        modified = True
        print(f"- Updated Date Planted in admonition: {new_date} ({new_season})")

    # 4. Update matching log entry date if old_date is known
    if old_date:
        log_pattern = rf'\*\s*\*\*{re.escape(old_date)}:\*\*'
        if re.search(log_pattern, content):
            content = re.sub(log_pattern, f"* **{new_date}:**", content)
            modified = True
            print(f"- Updated matching log entry date prefix from {old_date} to {new_date}")

    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Successfully updated planting date for {os.path.basename(filepath)} to {new_date} ({new_season})")
    else:
        print("No changes were made.")

if __name__ == "__main__":
    main()
