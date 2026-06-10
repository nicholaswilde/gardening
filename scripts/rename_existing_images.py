#!/usr/bin/env python3
import os
import re
import glob

def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    plants_dir = os.path.join(project_root, "docs", "plants")
    images_dir = os.path.join(project_root, "docs", "assets", "images")
    
    # regex to find tabs like === "YYYY-MM-DD"
    tab_pattern = re.compile(r'===\s*"(\d{4}-\d{2}-\d{2})"')
    
    # regex to find image definitions at the bottom
    # e.g., [1]: <../assets/images/oregano.webp>
    ref_pattern = re.compile(r'^\[(\d+)\]:\s*<\.\./assets/images/([^>]+)>', re.MULTILINE)
    
    md_files = glob.glob(os.path.join(plants_dir, "*.md"))
    
    for filepath in md_files:
        filename = os.path.basename(filepath)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find all tab dates
        dates = tab_pattern.findall(content)
        # Find all image references
        refs = ref_pattern.findall(content)
        
        if not dates or not refs:
            continue
            
        # We assume one image and one date tab for existing ones, or match them.
        # To be safe, if there's only one date and one reference, we match them.
        if len(dates) == 1 and len(refs) == 1:
            date = dates[0]
            ref_num, img_filename = refs[0]
            
            # Skip if image name already has the date appended
            if date in img_filename:
                print(f"Skipping {filename}: Reference '{img_filename}' already contains date '{date}'")
                continue
                
            img_basename, img_ext = os.path.splitext(img_filename)
            old_image_path = os.path.join(images_dir, img_filename)
            
            new_img_filename = f"{img_basename}-{date}{img_ext}"
            new_image_path = os.path.join(images_dir, new_img_filename)
            
            # Rename the physical file if it exists
            if os.path.exists(old_image_path):
                if not os.path.exists(new_image_path):
                    os.rename(old_image_path, new_image_path)
                    print(f"Renamed image: {img_filename} -> {new_img_filename}")
                else:
                    print(f"New image already exists, skipping rename of {img_filename}")
            else:
                print(f"Image {old_image_path} does not exist (may have already been renamed or missing)")
                
            # Update the reference in the markdown content
            # Replace: [ref_num]: <../assets/images/img_filename>
            # with: [ref_num]: <../assets/images/new_img_filename>
            old_ref_str = f"[{ref_num}]: <../assets/images/{img_filename}>"
            new_ref_str = f"[{ref_num}]: <../assets/images/{new_img_filename}>"
            
            if old_ref_str in content:
                new_content = content.replace(old_ref_str, new_ref_str)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated reference in {filename}: {old_ref_str} -> {new_ref_str}")
            else:
                print(f"Could not find exact reference string in {filename} to replace")
                
        else:
            print(f"Warning: {filename} has multiple dates ({len(dates)}) or references ({len(refs)}). Skipping automatic processing.")

if __name__ == "__main__":
    main()
