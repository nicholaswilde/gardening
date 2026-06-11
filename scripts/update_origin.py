#!/usr/bin/env python3
# scripts/update_origin.py

import os
import sys
import re

# Ensure the scripts directory is in the path to import lib.models
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.models import PlantProfile

# Standard origin mappings matching style-guide.md
ORIGIN_MAPPINGS = {
    "seed-indoor": {
        "term": "Seed (Indoor Start)",
        "icon": ":material-seed:",
        "aliases": ["seed-indoor", "seed (indoor)", "indoor start", "indoor seed", "seed (indoor start)"]
    },
    "seed-direct": {
        "term": "Seed (Direct Sow)",
        "icon": ":material-seed-outline:",
        "aliases": ["seed-direct", "seed (direct)", "direct sow", "direct seed", "seed (direct sow)"]
    },
    "nursery-start": {
        "term": "Nursery Start",
        "icon": ":material-storefront-outline:",
        "aliases": ["nursery", "nursery-start", "nursery start", "nursery transplant"]
    },
    "bare-root": {
        "term": "Bare Root",
        "icon": ":material-pine-tree-variant-outline:",
        "aliases": ["bare root", "bare-root"]
    },
    "cutting": {
        "term": "Cutting / Clone",
        "icon": ":material-content-cut:",
        "aliases": ["cutting", "clone", "cutting / clone", "cutting/clone"]
    },
    "division": {
        "term": "Division",
        "icon": ":material-call-split:",
        "aliases": ["division"]
    },
    "volunteer": {
        "term": "Volunteer",
        "icon": ":material-recycle:",
        "aliases": ["volunteer"]
    },
    "gifted-transplant": {
        "term": "Gifted transplant",
        "icon": ":material-gift-outline:",
        "aliases": ["gift", "gifted", "gifted transplant", "gifted-transplant"]
    },
    "living-herb": {
        "term": "Living herb",
        "icon": ":material-store-outline:",
        "aliases": ["living herb", "living-herb"]
    }
}

def resolve_origin(query):
    query_clean = query.strip().lower()
    for key, data in ORIGIN_MAPPINGS.items():
        if query_clean == key or query_clean in data["aliases"]:
            return data
    # Fallback to see if it starts with or contains any key/alias
    for key, data in ORIGIN_MAPPINGS.items():
        for alias in data["aliases"]:
            if alias in query_clean:
                return data
    return None

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 scripts/update_origin.py <plant-name-or-file> <origin-type>")
        print("Standard origin-types: " + ", ".join(ORIGIN_MAPPINGS.keys()))
        sys.exit(1)
        
    target = sys.argv[1]
    origin_input = sys.argv[2]
    
    # Resolve standard origin data
    origin_data = resolve_origin(origin_input)
    if not origin_data:
        print(f"Error: Unknown origin type '{origin_input}'.")
        print("Available standard types: " + ", ".join(f"'{k}'" for k in ORIGIN_MAPPINGS.keys()))
        sys.exit(1)
        
    term = origin_data["term"]
    icon = origin_data["icon"]
    
    # Resolve file path
    filepath = target
    if not filepath.endswith(".md"):
        # Assume it's a plant name in docs/plants/
        filepath = f"docs/plants/{target}.md"
        
    if not os.path.exists(filepath):
        # Maybe check project root context
        filepath = os.path.join("/home/nicholas/git/nicholaswilde/gardening", filepath)
        if not os.path.exists(filepath):
            print(f"Error: File '{target}' or '{filepath}' not found.")
            sys.exit(1)
            
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    try:
        profile = PlantProfile.from_markdown(content)
        
        # Update origin in the admonition block using the model
        profile.set_admonition_value("Origin", term, icon.strip(":"))
        print(f"- Updated Origin in admonition block to: {term}")
        
        # Serialize the updated profile
        content = profile.serialize()
        modified = True
        
        # Update Cultivation Status table in the content if it exists (legacy fallback)
        table_pattern = r'(\|\s*\*\*Origin\*\*\s*\|\s*)[^|\n]+(\s*\|?)'
        if re.search(table_pattern, content):
            content = re.sub(table_pattern, rf'\g<1>{term}\g<2>', content)
            print(f"- Updated Origin in Cultivation Status table to: {term}")
        else:
            # If the table doesn't have an Origin row, find the Cultivation Status table and add it
            table_match = re.search(r'(\|\s*Attribute\s*\|\s*Details\s*\|.*?\n(?:\|[^\n]+\n)+)', content, re.IGNORECASE)
            if table_match and ("Date Planted" in table_match.group(1) or "Current State" in table_match.group(1)):
                original_table = table_match.group(1)
                table_lines = original_table.split('\n')
                
                # Insert Origin row at the end of the table
                last_line_idx = len(table_lines) - 1
                while last_line_idx >= 0 and not table_lines[last_line_idx].strip():
                    last_line_idx -= 1
                    
                if last_line_idx >= 0:
                    new_row = "| **Origin** | {} |".format(term)
                    table_lines.insert(last_line_idx + 1, new_row)
                    new_table = "\n".join(table_lines)
                    content = content.replace(original_table, new_table)
                    print(f"- Added Origin row to Cultivation Status table: {term}")
                    
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Successfully updated {filepath}")
    except Exception as e:
        print(f"Error updating origin: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
