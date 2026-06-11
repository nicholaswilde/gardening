#!/usr/bin/env python3
# scripts/archive_plant.py

import os
import sys
import re

# Ensure the scripts directory is in the path to import lib.models
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.models import PlantProfile

def main():
    if len(sys.argv) < 6:
        print("Usage: python3 scripts/archive_plant.py <plant-name> <year> <removed-date> <final-state> <outcome>")
        print("Example: python3 scripts/archive_plant.py cilantro 2025 2026-05-10 \"Harvested / Cleared\" \"High yield.\"")
        sys.exit(1)
        
    plant_name = sys.argv[1].strip()
    year = sys.argv[2].strip()
    removed_date = sys.argv[3].strip()
    final_state = sys.argv[4].strip()
    outcome = sys.argv[5].strip()
    
    project_root = "/home/nicholas/git/nicholaswilde/gardening"
    
    # Resolve Markdown file path
    orig_md_path = os.path.join(project_root, "docs", "plants", f"{plant_name}.md")
    if not os.path.exists(orig_md_path):
        print(f"Error: Plant profile '{orig_md_path}' not found.")
        sys.exit(1)
        
    new_md_name = f"{plant_name}-{year}.md"
    new_md_path = os.path.join(project_root, "docs", "plants", new_md_name)
    
    # 1. Rename Image File
    # Check if there is an image in docs/assets/images/
    img_exts = [".webp", ".png", ".jpg", ".jpeg"]
    found_img_ext = None
    orig_img_path = None
    new_img_name = None
    new_img_path = None
    
    for ext in img_exts:
        test_path = os.path.join(project_root, "docs", "assets", "images", f"{plant_name}{ext}")
        if os.path.exists(test_path):
            found_img_ext = ext
            orig_img_path = test_path
            new_img_name = f"{plant_name}-{year}{ext}"
            new_img_path = os.path.join(project_root, "docs", "assets", "images", new_img_name)
            break
            
    if orig_img_path and new_img_path:
        os.rename(orig_img_path, new_img_path)
        print(f"- Renamed image file: {os.path.basename(orig_img_path)} -> {os.path.basename(new_img_path)}")
        
    # 2. Update Markdown Content using PlantProfile
    with open(orig_md_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    try:
        profile = PlantProfile.from_markdown(content)
        
        # Get plant display title (clean title)
        display_title = profile.title
        display_title = re.sub(r'^:\w+:\s*', '', display_title) # strip starting emoji
        display_title = re.sub(r'\s*\(\d+\)$', '', display_title).strip() # strip ending (1)
        if not display_title:
            display_title = plant_name.replace('-', ' ').title()
        
        # Update tags
        tags = profile.frontmatter.tags or []
        if "active" in tags:
            tags.remove("active")
        if "archived" not in tags:
            tags.append("archived")
        profile.frontmatter.tags = tags
        profile.frontmatter.removed = removed_date
        print("- Updated frontmatter tags and added removed date.")
        
        # Update Image References
        if found_img_ext:
            # Update inline image tags in header_body and sections
            profile.header_body = profile.header_body.replace(f"![{plant_name}][", f"![{plant_name}-{year}][")
            for sec_heading, sec_content in profile.sections.items():
                profile.sections[sec_heading] = sec_content.replace(f"![{plant_name}][", f"![{plant_name}-{year}][")
                
            # Update bottom image reference mappings
            for label, path in list(profile.image_references.items()):
                clean_path = path.strip("<>")
                if f"{plant_name}{found_img_ext}" in clean_path:
                    new_path = clean_path.replace(f"{plant_name}{found_img_ext}", f"{plant_name}-{year}{found_img_ext}")
                    profile.image_references[label] = new_path
            print("- Updated image references in markdown content.")
            
        # Update Admonition block using models
        status_row_found = False
        for row in profile.admonition_rows:
            if row.key in ("Status", "Current State", "Final State"):
                row.key = "Status"
                row.value = final_state
                row.icon = "material-list-status"
                status_row_found = True
                break
        if not status_row_found:
            profile.set_admonition_value("Status", final_state, "material-list-status")
            
        profile.set_admonition_value("Date Removed", removed_date, "material-calendar-remove-outline")
        profile.set_admonition_value("Outcome", outcome, "material-chat-alert-outline")
        print("- Updated admonition block with status, date removed, and outcome.")
        
        # Serialize the updated profile back to markdown
        content = profile.serialize()
        
        # Update Cultivation Status Table to Final State table (Legacy Fallback)
        content = re.sub(
            r'(\|\s*\*\*Current State\*\*\s*\|\s*)[^|\n]+',
            r'\g<1>Final State',
            content
        )
        
        table_match = re.search(r'(\|\s*Attribute\s*\|\s*Details\s*\|.*?\n(?:\|[^\n]+\n)+)', content, re.IGNORECASE)
        if table_match and ("Date Planted" in table_match.group(1) or "Current State" in table_match.group(1)):
            orig_table = table_match.group(1)
            table_lines = orig_table.split('\n')
            new_table_lines = []
            
            has_removed_row = False
            has_outcome_row = False
            
            for line in table_lines:
                if not line.strip():
                    continue
                if "Current State" in line:
                    new_table_lines.append(f"| **Final State** | {final_state} |")
                elif "Date Removed" in line:
                    new_table_lines.append(f"| **Date Removed** | {removed_date} |")
                    has_removed_row = True
                elif "Outcome" in line:
                    new_table_lines.append(f"| **Outcome** | {outcome} |")
                    has_outcome_row = True
                else:
                    new_table_lines.append(line)
                    
            idx_to_insert = -1
            for idx, line in enumerate(new_table_lines):
                if "Date Planted" in line or "Planted" in line:
                    idx_to_insert = idx
                    break
                    
            if idx_to_insert != -1:
                if not has_removed_row:
                    new_table_lines.insert(idx_to_insert + 1, f"| **Date Removed** | {removed_date} |")
                if not has_outcome_row:
                    new_table_lines.append(f"| **Outcome** | {outcome} |")
            else:
                if not has_removed_row:
                    new_table_lines.append(f"| **Date Removed** | {removed_date} |")
                if not has_outcome_row:
                    new_table_lines.append(f"| **Outcome** | {outcome} |")
                    
            content = content.replace(orig_table, "\n".join(new_table_lines) + "\n")
            print("- Updated Cultivation Status table with Final State, Date Removed, and Outcome.")
            
        # Write the modified markdown content to the new path, and delete original
        with open(new_md_path, "w", encoding="utf-8") as f:
            f.write(content)
        os.remove(orig_md_path)
        print(f"- Created archived profile: {os.path.basename(new_md_path)}")
        print(f"- Removed original profile: {os.path.basename(orig_md_path)}")
        
        # 3. Update zensical.toml Navigation
        config_path = os.path.join(project_root, "zensical.toml")
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                config_content = f.read()
                
            modified_config = False
            
            # Remove entry from Plants list
            plant_entry_pattern = rf'(\s*\{{\s*".*?"\s*=\s*"plants/{plant_name}\.md"\s*\}},?\n)'
            nav_match = re.search(plant_entry_pattern, config_content)
            if nav_match:
                config_content = config_content.replace(nav_match.group(1), "")
                print(f"- Removed '{display_title}' entry from Plants list in zensical.toml")
                modified_config = True
                
            # Add entry to Archive section under target year
            archive_pattern = r'(Archive\s*=\s*\[\s*\n(.*?)\n\s*\]\s*,?\s*\n)'
            archive_match = re.search(archive_pattern, config_content, re.DOTALL)
            if archive_match:
                entire_archive_block = archive_match.group(1)
                archive_body = archive_match.group(2)
                
                year_pattern = rf'(\{{\s*"{year}"\s*=\s*\[\s*\n(.*?)\n\s*\]\s*\}})'
                year_match = re.search(year_pattern, archive_body, re.DOTALL)
                
                if year_match:
                    entire_year_block = year_match.group(1)
                    year_body = year_match.group(2)
                    
                    entries = [line.strip() for line in year_body.split('\n') if line.strip()]
                    new_entry = f'{{ "{display_title}" = "plants/{plant_name}-{year}.md" }},'
                    entries.append(new_entry)
                    
                    sorted_entries = sorted(list(set(entries)))
                    new_year_body = "\n".join(f"  {entry}" for entry in sorted_entries)
                    
                    new_year_block = f'{{ "{year}" = [\n{new_year_body}\n  ] }}'
                    new_archive_body = archive_body.replace(entire_year_block, new_year_block)
                    new_archive_block = entire_archive_block.replace(archive_body, new_archive_body)
                    config_content = config_content.replace(entire_archive_block, new_archive_block)
                    print(f"- Added '{display_title}' entry to Archive under {year} in zensical.toml")
                    modified_config = True
                else:
                    new_year_block = f'  {{ "{year}" = [\n    {{ "{display_title}" = "plants/{plant_name}-{year}.md" }}\n  ] }},\n'
                    new_archive_body = new_year_block + archive_body
                    new_archive_block = entire_archive_block.replace(archive_body, new_archive_body)
                    config_content = config_content.replace(entire_archive_block, new_archive_block)
                    print(f"- Created new Archive year category '{year}' and added '{display_title}' in zensical.toml")
                    modified_config = True
                    
            if modified_config:
                with open(config_path, "w", encoding="utf-8") as f:
                    f.write(config_content)
                print(f"✅ Successfully updated zensical.toml")
                
        print("🎉 Archiving complete!")
    except Exception as e:
        print(f"Error archiving plant: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
