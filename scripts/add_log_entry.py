#!/usr/bin/env python3
import sys
import os
from datetime import datetime

# Ensure the scripts directory is in the path to import lib.models
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.models import PlantProfile, LogEntry

def main():
    if len(sys.argv) < 3:
        print("Error: Provide plant name and observation message.")
        print('Usage: python3 scripts/add_log_entry.py <plant-name> "Observation text"')
        sys.exit(1)
        
    plant_name = sys.argv[1]
    observation = sys.argv[2]
    
    # Get the project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    plant_file = os.path.join(project_root, "docs", "plants", f"{plant_name}.md")
    
    if not os.path.exists(plant_file):
        print(f"Error: Plant file not found: {plant_file}")
        sys.exit(1)
        
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    with open(plant_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    try:
        profile = PlantProfile.from_markdown(content)
        profile.add_log_entry(LogEntry(date=current_date, message=observation))
        
        with open(plant_file, "w", encoding="utf-8") as f:
            f.write(profile.serialize())
            
        print(f"Added log entry to {plant_file}")
    except Exception as e:
        print(f"Error updating plant log: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
