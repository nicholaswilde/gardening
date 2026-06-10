#!/usr/bin/env python3
import sys
import os
from datetime import datetime

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
    new_entry = f"* **{current_date}**: {observation}\n"
    
    with open(plant_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    target_index = -1
    for i, line in enumerate(lines):
        if "## :memo: Log & Observations" in line:
            target_index = i
            break
            
    if target_index == -1:
        print("Error: '## :memo: Log & Observations' section not found in file.")
        sys.exit(1)
        
    # Insert entry:
    # Check if the line after heading is empty.
    # If yes, insert after it. If not, insert after heading with a blank line.
    if target_index + 1 < len(lines):
        next_line = lines[target_index + 1].strip()
        if not next_line:
            # It's an empty line, insert the new entry after it
            lines.insert(target_index + 2, new_entry)
        else:
            # It's not an empty line, insert empty line + entry
            lines.insert(target_index + 1, "\n" + new_entry)
    else:
        # Heading is the last line of the file
        lines.append("\n" + new_entry)
        
    with open(plant_file, "w", encoding="utf-8") as f:
        f.writelines(lines)
        
    print(f"Added log entry to {plant_file}")

if __name__ == "__main__":
    main()
