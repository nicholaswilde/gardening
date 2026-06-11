#!/usr/bin/env python3

import os
import re
from collections import defaultdict

PLANTS_DIR = "docs/plants"
DASHBOARD_FILE = "docs/seasonal-dashboard.md"

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
            
        # Parse title from H1 header
        title_match = re.search(r'^#\s+(?::\w+:\s*)?(.+)', content, re.MULTILINE)
        # Parse season from the Cultivation Status table or the new admonition block
        season_match = re.search(r'\|\s*\*\*Season Planted\*\*\s*\|\s*([^|]+)\s*\|', content)
        if not season_match:
            season_match = re.search(r'\*\*(?::material-[a-z-]+:\s*)?Date Planted:\*\*\s*[^\n\(]+\(([^)]+)\)', content)
        
        if title_match and season_match:
            title = title_match.group(1).strip()
            season = season_match.group(1).strip()
            
            # Only add if a season is actually defined and not 'Unknown'
            if season and season != 'Unknown':
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
        
        season_emojis = {
            "Early Spring": ":cherry_blossom:",
            "Mid-Spring": ":cherry_blossom:",
            "Late Spring": ":cherry_blossom:",
            "Early Summer": ":sun_with_face:",
            "Mid-Summer": ":sun_with_face:",
            "Late Summer": ":sun_with_face:",
            "Early Fall": ":maple_leaf:",
            "Mid-Fall": ":maple_leaf:",
            "Late Fall / Winter": ":snowflake:"
        }
        
        sections = []
        for target_season in season_order:
            if target_season in seasons:
                emoji = season_emojis.get(target_season, "")
                emoji_prefix = f"{emoji} " if emoji else ""
                section_lines = [f"## {emoji_prefix}{target_season}", ""]
                # Sort plants alphabetically within the season
                for title, filename in sorted(seasons[target_season]):
                    section_lines.append(f"* [{title}](plants/{filename})")
                sections.append("\n".join(section_lines))
        
        f.write("\n\n".join(sections) + "\n")

if __name__ == "__main__":
    build_dashboard()
  
