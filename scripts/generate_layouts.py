#!/usr/bin/env python3
import os
import re
import glob
import sys
from typing import List, Dict, Any, Tuple

# Add scripts directory to path to import models and layout generator
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from lib.models import PlantProfile
from lib.layout_generator import generate_mermaid_layout

def scan_active_plants(plants_dir: str) -> List[Dict[str, Any]]:
    """
    Scans plant profiles and extracts active plants with locations and grid positions.
    """
    active_plants = []
    plant_files = glob.glob(os.path.join(plants_dir, "*.md"))
    
    for filepath in plant_files:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            profile = PlantProfile.from_markdown(content)
            fm = profile.frontmatter
            
            # Check if active and placed in a grid location
            if fm.tags and "active" in fm.tags and fm.location and fm.grid_position:
                name = fm.common_name or profile.title or os.path.splitext(os.path.basename(filepath))[0].replace("-", " ").title()
                # Strip emoji or count prefix from title name if needed for clean layout
                clean_name = re.sub(r'^:\w+:\s*', '', name)
                
                status = fm.status or profile.get_admonition_value("Status") or "Active"
                # If status starts with Active (e.g. Active Growth), simplify or preserve
                if status.lower().startswith("active"):
                    status = "Active"
                
                active_plants.append({
                    "common_name": clean_name,
                    "grid_position": fm.grid_position,
                    "location": fm.location,
                    "status": status,
                    "relative_path": f"../plants/{os.path.basename(filepath)}"
                })
        except Exception as e:
            print(f"Warning: Failed to parse plant profile {os.path.basename(filepath)}: {e}", file=sys.stderr)
            
    return active_plants

def parse_bed_metadata(content: str) -> Tuple[str, str]:
    """
    Parses the bed title and dimensions footprint from bed profile content.
    """
    # Find heading (e.g., # :brown_square: Raised Bed 2)
    title_match = re.search(r'^#\s*:\w+:\s*(.*)$', content, re.MULTILINE)
    if not title_match:
        title_match = re.search(r'^#\s*(.*)$', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else "Raised Bed"
    
    # Find dimensions (e.g., **:material-ruler-square: Dimensions:** 4' x 8' x 1.5')
    dims_match = re.search(r'\*\*:material-ruler-square:\s*Dimensions:\*\*\s*(.*)$', content, re.MULTILINE)
    dims = "4' x 8'"
    if dims_match:
        dims_raw = dims_match.group(1).strip()
        parts = dims_raw.split("x")
        if len(parts) >= 2:
            row_dim = parts[0].strip()
            col_dim = parts[1].strip()
            # Remove any trailing depth/volume details from the second term
            col_dim = re.split(r'\s+', col_dim)[0]
            dims = f"{row_dim} x {col_dim}"
            
    return title, dims

def inject_layout_into_bed(bed_content: str, mermaid_diagram: str) -> str:
    """
    Replaces the content between layout markers with the new Mermaid diagram.
    """
    start_marker = "<!-- BED_LAYOUT_START -->"
    end_marker = "<!-- BED_LAYOUT_END -->"
    
    if start_marker not in bed_content or end_marker not in bed_content:
        raise ValueError("Bed layout markers <!-- BED_LAYOUT_START --> and <!-- BED_LAYOUT_END --> not found in bed file.")
        
    start_idx = bed_content.find(start_marker) + len(start_marker)
    end_idx = bed_content.find(end_marker)
    
    new_block = f"\n\n```mermaid\n{mermaid_diagram.strip()}\n```\n\n"
    return bed_content[:start_idx] + new_block + bed_content[end_idx:]

def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    plants_dir = os.path.join(project_root, "docs", "plants")
    beds_dir = os.path.join(project_root, "docs", "beds")
    
    print("Scanning active plant profiles...")
    plants = scan_active_plants(plants_dir)
    print(f"Found {len(plants)} active crop placements.")
    
    # Group plants by location
    bed_placements = {}
    for p in plants:
        loc = p["location"]
        if loc not in bed_placements:
            bed_placements[loc] = []
        bed_placements[loc].append(p)
        
    # Process each bed
    for loc, placements in bed_placements.items():
        bed_file = os.path.join(beds_dir, f"{loc}.md")
        if not os.path.exists(bed_file):
            print(f"Warning: Bed profile {bed_file} does not exist. Skipping.", file=sys.stderr)
            continue
            
        print(f"Processing bed: {loc}...")
        try:
            with open(bed_file, "r", encoding="utf-8") as f:
                content = f.read()
                
            title, dims = parse_bed_metadata(content)
            mermaid = generate_mermaid_layout(title, dims, placements)
            
            updated_content = inject_layout_into_bed(content, mermaid)
            
            with open(bed_file, "w", encoding="utf-8") as f:
                f.write(updated_content)
            print(f"Successfully updated layout in {bed_file}.")
        except Exception as e:
            print(f"Error processing bed {loc}: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
