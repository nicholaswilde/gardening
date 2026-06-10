#!/usr/bin/env python3
import sys
import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

def get_season(date_obj):
    month = date_obj.month
    day = date_obj.day
    # Season mapping matching chronological timeline
    if month in [12, 1, 2]:
        return "Late Fall / Winter"
    elif month == 3:
        return "Early Spring" if day < 15 else "Mid-Spring"
    elif month == 4:
        return "Mid-Spring" if day < 15 else "Late Spring"
    elif month == 5:
        return "Late Spring"
    elif month == 6:
        return "Early Summer" if day < 15 else "Mid-Summer"
    elif month == 7:
        return "Mid-Summer" if day < 15 else "Late Summer"
    elif month == 8:
        return "Late Summer"
    elif month == 9:
        return "Early Fall" if day < 15 else "Mid-Fall"
    elif month == 10:
        return "Mid-Fall" if day < 15 else "Late Fall / Winter"
    elif month == 11:
        return "Late Fall / Winter"
    return "Unknown"

def main():
    if len(sys.argv) < 2:
        print("Error: Provide a filename (e.g., python3 scripts/new_plant.py tomato)")
        sys.exit(1)
    
    filename = sys.argv[1]
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    title = filename.replace('-', ' ').title()
    season = get_season(now)
    
    # Get the project root directory (assuming script is in /scripts)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # Setup Jinja2 environment pointing to the templates directory
    template_dir = os.path.join(project_root, "templates")
    env = Environment(loader=FileSystemLoader(template_dir))
    
    # Load and render the template
    template = env.get_template("plant.md.j2")
    content = template.render(
        filename=filename,
        title=title,
        season=season,
        current_date=current_date
    )
    
    # Define output path
    out_dir = os.path.join(project_root, "docs", "plants")
    out_file = os.path.join(out_dir, f"{filename}.md")

    # Create directories and write file
    os.makedirs(out_dir, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Created {out_file}")

if __name__ == "__main__":
    main()
