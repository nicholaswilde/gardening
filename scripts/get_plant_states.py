#!/usr/bin/env python3
# scripts/get_plant_states.py

import os
import re

# Resolve plants directory relative to the script location
script_dir = os.path.dirname(os.path.abspath(__file__))
plants_dir = os.path.normpath(os.path.join(script_dir, "..", "docs", "plants"))
results = []

for filename in sorted(os.listdir(plants_dir)):
    if not filename.endswith(".md"):
        continue
    filepath = os.path.join(plants_dir, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Get Title
    title_match = re.search(r'^#\s*(?::\w+:\s*)?(.+)', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else filename
    
    # Search for Current State or Final State in markdown table
    state_match = re.search(r'\|\s*\*\*(Current|Final)\s+State\*\*\s*\|\s*([^|\n]+)', content, re.IGNORECASE)
    if state_match:
        state_type = state_match.group(1).strip()
        state_val = state_match.group(2).strip()
        state = f"{state_type}: {state_val}"
    else:
        state = "Not Found"
        
    results.append((filename, title, state))

print(f"%-30s | %-30s | %s" % ("File", "Plant Title", "Current / Final State"))
print("-" * 90)
for file, title, state in results:
    print(f"%-30s | %-30s | %s" % (file, title, state))
