#!/usr/bin/env python3

import os
import sys
import re
from collections import defaultdict

# Ensure the scripts directory is in the path to import lib.models
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.models import PlantProfile

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
            
        try:
            profile = PlantProfile.from_markdown(content)
            
            # Clean title
            title = profile.title
            title = re.sub(r'^:\w+:\s*', '', title) # strip starting emoji
            title = re.sub(r'\s*\(\d+\)$', '', title).strip() # strip ending (1)
            
            # Extract season from admonition block "Date Planted" (e.g. "2026-06-09 (Unknown)" or "2021-11-01 (Late Fall / Winter)")
            season = None
            date_planted_val = profile.get_admonition_value("Date Planted")
            if date_planted_val:
                m = re.search(r'\(([^)]+)\)', date_planted_val)
                if m:
                    season = m.group(1).strip()
            
            # Legacy fallback: check Cultivation Status table inside sections if it exists
            if not season:
                for heading, sec_content in profile.sections.items():
                    if "Cultivation Status" in heading:
                        season_match = re.search(r'\|\s*\*\*Season Planted\*\*\s*\|\s*([^|]+)\s*\|', sec_content)
                        if season_match:
                            season = season_match.group(1).strip()
                            break
            
            if title and season:
                # Only add if a season is actually defined and not 'Unknown'
                if season != 'Unknown':
                    seasons[season].append((title, filename))
        except Exception as e:
            print(f"Warning: Failed to parse {filename} in dashboard build: {e}")

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
                for title, filename in sorted(seasons[target_season]):
                    section_lines.append(f"* [{title}](plants/{filename})")
                sections.append("\n".join(section_lines))
        
        f.write("\n\n".join(sections) + "\n")
    print(f"✅ Dashboard rebuilt: {DASHBOARD_FILE}")

if __name__ == "__main__":
    build_dashboard()
