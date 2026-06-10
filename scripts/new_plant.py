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
    import argparse
    
    # Setup sys.path to import from sibling scripts
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    from get_image_date import get_date_taken

    parser = argparse.ArgumentParser(description="Generate a new plant profile template.")
    parser.add_argument("filename", help="Kebab-case name of the plant (e.g. poblano-pepper)")
    parser.add_argument("--image-date", help="Date the image was taken (YYYY-MM-DD)")
    parser.add_argument("--image-filename", help="Filename of the image (without .webp)")
    
    args = parser.parse_args()
    filename = args.filename
    
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    title = filename.replace('-', ' ').title()
    season = get_season(now)
    
    # Get the project root directory (assuming script is in /scripts)
    project_root = os.path.dirname(script_dir)
    images_dir = os.path.join(project_root, "docs", "assets", "images")
    
    image_date = args.image_date
    image_filename = args.image_filename
    
    if not image_date or not image_filename:
        # Automatic detection logic
        detected_date = None
        detected_filename = None
        
        non_dated_image = os.path.join(images_dir, f"{filename}.webp")
        if os.path.exists(non_dated_image):
            extracted = get_date_taken(non_dated_image)
            if extracted:
                detected_date = extracted
                dated_name = f"{filename}-{extracted}"
                dated_path = os.path.join(images_dir, f"{dated_name}.webp")
                
                # Avoid renaming conflict if dated file already exists
                if not os.path.exists(dated_path):
                    os.rename(non_dated_image, dated_path)
                    print(f"Renamed {non_dated_image} to {dated_path}")
                else:
                    os.remove(non_dated_image)
                    print(f"Dated image already exists. Removed temporary {non_dated_image}")
                detected_filename = dated_name
        else:
            # Check if a dated image already exists
            import glob
            pattern = os.path.join(images_dir, f"{filename}-*.webp")
            matching_files = glob.glob(pattern)
            if matching_files:
                matching_files.sort()
                newest_image = matching_files[-1]
                detected_filename = os.path.splitext(os.path.basename(newest_image))[0]
                extracted = get_date_taken(newest_image)
                if extracted:
                    detected_date = extracted
                else:
                    # Parse date from filename ending with YYYY-MM-DD
                    parts = detected_filename.split('-')
                    if len(parts) >= 3:
                        possible_date = "-".join(parts[-3:])
                        try:
                            datetime.strptime(possible_date, "%Y-%m-%d")
                            detected_date = possible_date
                        except ValueError:
                            pass
        
        # Fallbacks
        if not image_date:
            image_date = detected_date if detected_date else current_date
        if not image_filename:
            image_filename = detected_filename if detected_filename else f"{filename}-{image_date}"

    # Setup Jinja2 environment pointing to the templates directory
    template_dir = os.path.join(project_root, "templates")
    env = Environment(loader=FileSystemLoader(template_dir))
    
    # Load and render the template
    template = env.get_template("plant.md.j2")
    content = template.render(
        filename=filename,
        title=title,
        season=season,
        current_date=current_date,
        image_date=image_date,
        image_filename=image_filename
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
