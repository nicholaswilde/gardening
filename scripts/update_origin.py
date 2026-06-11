#!/usr/bin/env python3
# scripts/update_origin.py

import os
import sys
import re

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
        
    modified = False
    
    # 1. Update admonition block
    # Check if there is an admonition block
    pattern = r'(!!! example ""\n(?:(?:[ \t]+.*\n)|\n)+)'
    match = re.search(pattern, content)
    if match:
        original_block = match.group(1)
        block_lines = original_block.split('\n')
        
        # Check if Origin already exists in the admonition block
        origin_line_idx = -1
        indent = "    "
        for idx, line in enumerate(block_lines):
            if "Origin:" in line:
                origin_line_idx = idx
                # Capture indentation
                indent_match = re.match(r'^([ \t]*)', line)
                if indent_match:
                    indent = indent_match.group(1)
                break
                
        if origin_line_idx != -1:
            # Update existing line
            block_lines[origin_line_idx] = f"{indent}**{icon} Origin:** {term}"
            print(f"- Updated existing Origin in admonition block to: {term}")
        else:
            # Add to the end of admonition block (before H2 or end of block)
            # Find the last non-empty line of the admonition body
            last_item_idx = len(block_lines) - 1
            while last_item_idx >= 0 and not block_lines[last_item_idx].strip():
                last_item_idx -= 1
                
            if last_item_idx >= 0:
                # Capture indentation from the last item
                indent_match = re.match(r'^([ \t]*)', block_lines[last_item_idx])
                if indent_match:
                    indent = indent_match.group(1)
                
                # Insert empty line and then the new Origin line
                block_lines.insert(last_item_idx + 1, "")
                block_lines.insert(last_item_idx + 2, f"{indent}**{icon} Origin:** {term}")
                print(f"- Appended Origin to admonition block: {term}")
                
        new_block = "\n".join(block_lines)
        if original_block != new_block:
            content = content.replace(original_block, new_block)
            modified = True
            
    # 2. Update Cultivation Status table
    # Match: | **Origin** | ... |
    table_pattern = r'(\|\s*\*\*Origin\*\*\s*\|\s*)[^|\n]+(\s*\|?)'
    if re.search(table_pattern, content):
        content = re.sub(table_pattern, rf'\g<1>{term}\g<2>', content)
        print(f"- Updated Origin in Cultivation Status table to: {term}")
        modified = True
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
                # Add row
                new_row = "| **Origin** | {} |".format(term)
                table_lines.insert(last_line_idx + 1, new_row)
                new_table = "\n".join(table_lines)
                content = content.replace(original_table, new_table)
                print(f"- Added Origin row to Cultivation Status table: {term}")
                modified = True
                
    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Successfully updated {filepath}")
    else:
        print(f"No changes needed for {filepath}")

if __name__ == "__main__":
    main()
