#!/usr/bin/env python3

import os
import re
from collections import defaultdict

PLANTS_DIR = "docs/plants"
DASHBOARD_FILE = "docs/seasonal-dashboard.md"

# Regex to capture the YAML frontmatter block
FRONTMATTER_RE = re.compile(r'^---\n(.*?)\n---', re.DOTALL)

def build_dashboard():
    seasons = defaultdict(list)
    
    if not os.path.exists(PLANTS_DIR):
        print(f"Directory {PLANTS_DIR} not found.")
        return

    # Parse all markdown files
    for filename in os.listdir(PLANTS_DIR):
        if not filename.endswith('.md'):
            continue
            
        filepath = os.path.join(PLANTS_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        match = FRONTMATTER_RE.search(content)
        if match:
            fm = match.group(1)
            # Extract title and season using regex
            title_match = re.search(r'^title:\s*(.+)', fm, re.MULTILINE)
            season_match = re.search(r'^season:\s*(.+)', fm, re.MULTILINE)
            
            if title_match and season_match:
                title = title_match.group(1).strip()
                season = season_match.group(1).strip()
                
                # Only add if a season is actually defined
                if season:
                    seasons[season].append((title, filename))

    # Generate the Markdown Dashboard
    with open(DASHBOARD_FILE, 'w', encoding='utf-8') as f:
        f.write("# 🗓️ Seasonal Planting Dashboard\n\n")
        f.write("An auto-generated overview of all crops sorted by their optimal planting window.\n\n")
        
        # Sort chronologically based on your specific climate timeline
        season_order = [
            "Early Spring", "Mid-Spring", "Late Spring", 
            "Early Summer", "Mid-Summer", "Late Summer", 
            "Early Fall", "Mid-Fall", "Late Fall / Winter"
        ]
        
        for target_season in season_order:
            if target_season in seasons:
                f.write(f"## {target_season}\n")
                # Sort plants alphabetically within the season
                for title, filename in sorted(seasons[target_season]):
                    f.write(f"* [{title}](plants/{filename})\n")
                f.write("\n")

if __name__ == "__main__":
    build_dashboard()
  
