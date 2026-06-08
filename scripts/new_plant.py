#!/usr/bin/env python3
import sys
import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

def main():
    if len(sys.argv) < 2:
        print("Error: Provide a filename (e.g., python3 scripts/new_plant.py tomato)")
        sys.exit(1)
    
    filename = sys.argv[1]
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Get the project root directory (assuming script is in /scripts)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # Setup Jinja2 environment pointing to the templates directory
    template_dir = os.path.join(project_root, "templates")
    env = Environment(loader=FileSystemLoader(template_dir))
    
    # Load and render the template
    template = env.get_template("plant.md.j2")
    content = template.render(filename=filename, current_date=current_date)
    
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
