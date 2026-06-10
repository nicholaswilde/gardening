#!/usr/bin/env python3
import sys
import os
import re
import urllib.request
import urllib.parse
import json
import argparse

# Setup user agent header for requests
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def load_dotenv():
    """Load variables from .env manually to avoid external dependencies."""
    if os.path.exists(".env"):
        with open(".env") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, val = line.split("=", 1)
                    # strip quotes if present
                    val = val.strip("'\"")
                    os.environ[key] = val

def query_trefle_search(query, token):
    """Query Trefle API search endpoint."""
    url = f"https://trefle.io/api/v1/plants/search?token={token}&q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode('utf-8'))

def query_trefle_details(slug, token):
    """Query Trefle API species details endpoint."""
    url = f"https://trefle.io/api/v1/species/{slug}?token={token}"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode('utf-8'))

def parse_markdown(filepath):
    """Extract metadata from markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Get title
    title_match = re.search(r'^#\s*(?::\w+:\s*)?(.+)', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else None

    # Get YAML frontmatter
    frontmatter = {}
    fm_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if fm_match:
        for line in fm_match.group(1).split('\n'):
            if ':' in line:
                k, v = line.split(':', 1)
                frontmatter[k.strip()] = v.strip().strip("[]'\"")

    # Get Type and Variety from admonitions or main content (allowing optional Material icons)
    type_match = re.search(r'\*\*(?::material-[a-z-]+:\s*)?Type:\*\*\s*(.+)', content)
    plant_type = type_match.group(1).strip() if type_match else None

    variety_match = re.search(r'\*\*(?::material-[a-z-]+:\s*)?Variety:\*\*\s*(.+)', content)
    variety = variety_match.group(1).strip() if variety_match else None

    # Get Sunlight and Soil from notes
    sunlight_match = re.search(r'\*\*\s*Sunlight\s*:\*\*\s*(.+)', content, re.IGNORECASE)
    sunlight = sunlight_match.group(1).strip() if sunlight_match else None

    soil_match = re.search(r'\*\*\s*Soil\s*:\*\*\s*(.+)', content, re.IGNORECASE)
    soil = soil_match.group(1).strip() if soil_match else None

    return {
        'title': title,
        'frontmatter': frontmatter,
        'type': plant_type,
        'variety': variety,
        'sunlight': sunlight,
        'soil': soil,
        'content': content
    }

def main():
    parser = argparse.ArgumentParser(description="Verify markdown plant profile against Trefle database")
    parser.add_argument("filepath", help="Path to the plant markdown file")
    parser.add_argument("--slug", help="Force a specific species by Trefle slug")
    parser.add_argument("--update", action="store_true", help="Update the markdown file with verified information")
    
    args = parser.parse_args()

    if not os.path.exists(args.filepath):
        print(f"Error: File '{args.filepath}' not found.")
        sys.exit(1)

    load_dotenv()
    token = os.environ.get("TREFLE_TOKEN")
    if not token:
        print("Error: TREFLE_TOKEN not found in environment or .env file.")
        sys.exit(1)

    # Parse markdown file
    md_data = parse_markdown(args.filepath)
    plant_name = md_data['title']
    md_botanical = md_data['frontmatter'].get('botanical_name')
    
    # If botanical name is already specified, search for that directly
    search_query = md_botanical if md_botanical else plant_name

    db_data = None
    best_match = {}

    if args.slug:
        print(f"Fetching Trefle species details directly for slug '{args.slug}'...")
        try:
            details_res = query_trefle_details(args.slug, token)
            db_data = details_res.get('data', {})
            best_match = {
                'scientific_name': db_data.get('scientific_name'),
                'common_name': db_data.get('common_name'),
                'family': db_data.get('family'),
                'genus': db_data.get('genus'),
                'slug': db_data.get('slug')
            }
        except Exception as e:
            print(f"Error fetching slug details: {e}")
            sys.exit(1)
    else:
        print(f"Verifying plant info for '{plant_name}' using Trefle database (query: '{search_query}')...")
        # 1. Search Trefle
        try:
            search_res = query_trefle_search(search_query, token)
            results = search_res.get('data', [])
            if not results:
                print(f"No results found for query '{plant_name}' on Trefle.")
                sys.exit(0)

            # Rank and select the best matching result
            best_match = results[0]
            best_score = -1
            
            for r in results:
                scientific = r.get('scientific_name', '').lower()
                common = (r.get('common_name') or '').lower()
                
                score = 0
                if common == plant_name.lower() or scientific == plant_name.lower():
                    score = 3
                elif f" {plant_name.lower()} " in f" {common} " or f" {plant_name.lower()} " in f" {scientific} ":
                    score = 2
                elif plant_name.lower() in common or plant_name.lower() in scientific:
                    score = 1
                
                # Prioritize accepted status
                if r.get('status') == 'accepted':
                    score += 0.5
                    
                if score > best_score:
                    best_score = score
                    best_match = r

            slug = best_match.get('slug')
            print(f"Found match: {best_match.get('scientific_name')} (slug: {slug})")
            details_res = query_trefle_details(slug, token)
            db_data = details_res.get('data', {})
        except Exception as e:
            print(f"Error querying Trefle: {e}")
            sys.exit(1)

    db_botanical = db_data.get('scientific_name')
    print(f"\n--- Best Trefle Database Match ---")
    print(f"ID: {db_data.get('id')}")
    print(f"Scientific Name: {db_botanical}")
    print(f"Common Name: {db_data.get('common_name')}")
    print(f"Family: {db_data.get('family')}")
    print(f"Genus: {db_data.get('genus')}")

    # Comparisons
    print(f"\n--- Verification Report ---")
    
    # 1. Botanical details verification
    md_botanical = md_data['frontmatter'].get('botanical_name')
    if md_botanical:
        if md_botanical.strip().lower() == db_botanical.strip().lower():
            print(f"✅ Botanical Name: Matches ('{md_botanical}')")
        else:
            print(f"❌ Botanical Name: Discrepancy! Markdown: '{md_botanical}', Database: '{db_botanical}'")
    else:
        print(f"⚠️ Botanical Name: Missing in Markdown! (Database: '{db_botanical}')")

    # 2. Variety check
    variety = md_data['variety']
    if variety and "Tuscan Blue" in variety:
        print(f"❌ Variety: Discrepancy! Found copy-paste placeholder '{variety}' which belongs to Rosemary, not {plant_name}.")
    else:
        print(f"✅ Variety: Current markdown says '{variety}'")

    # 3. Type/Habit check
    md_type = md_data['type']
    db_habit = db_data.get('specifications', {}).get('growth_habit')
    print(f"ℹ️ Type: Markdown lists '{md_type}', Database lists growth habit as '{db_habit}'")

    # 4. Sunlight check
    sunlight = md_data['sunlight']
    db_light = db_data.get('growth', {}).get('light')
    print(f"ℹ️ Sunlight: Markdown lists '{sunlight}', Database lists light level: {db_light}/10")

    # 5. Soil / pH check
    soil = md_data['soil']
    db_ph_min = db_data.get('growth', {}).get('ph_minimum')
    db_ph_max = db_data.get('growth', {}).get('ph_maximum')
    db_ph = f"{db_ph_min} - {db_ph_max}" if db_ph_min else "Not specified"
    print(f"ℹ️ Soil: Markdown lists '{soil}', Database suggests soil pH range: {db_ph}")

    if args.update:
        print("\nUpdating markdown file with Trefle database information...")
        content = md_data['content']
        
        # Replace variety placeholder if it's the rosemary one
        if variety and "Tuscan Blue" in variety:
            # Let's clean the variety field or set it
            new_variety = "Greek Oregano" if "oregano" in plant_name.lower() else "Common"
            content = re.sub(
                rf'(\*\*(?::material-[a-z-]+:\s*)?Variety:\*\*)\s*{re.escape(variety)}',
                rf'\1 {new_variety}',
                content
            )
            print(f"- Replaced placeholder variety with '{new_variety}'.")

        # Ensure botanical_name, family, and genus are added to frontmatter
        fm_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
        if fm_match:
            original_fm = fm_match.group(1)
            new_fm_lines = []
            
            has_botanical = False
            has_family = False
            has_genus = False
            
            for line in original_fm.split('\n'):
                if line.startswith("botanical_name:"):
                    new_fm_lines.append(f"botanical_name: {db_botanical}")
                    has_botanical = True
                elif line.startswith("family:"):
                    new_fm_lines.append(f"family: {db_data.get('family')}")
                    has_family = True
                elif line.startswith("genus:"):
                    new_fm_lines.append(f"genus: {db_data.get('genus')}")
                    has_genus = True
                else:
                    new_fm_lines.append(line)
            
            if not has_botanical:
                new_fm_lines.append(f"botanical_name: {db_botanical}")
            if not has_family:
                new_fm_lines.append(f"family: {db_data.get('family')}")
            if not has_genus:
                new_fm_lines.append(f"genus: {db_data.get('genus')}")
                
            new_fm = "\n".join(new_fm_lines)
            content = content.replace(original_fm, new_fm)
            print("- Enriched frontmatter with botanical taxonomy.")
        else:
            new_fm = f"---\nbotanical_name: {db_botanical}\nfamily: {db_data.get('family')}\ngenus: {db_data.get('genus')}\n---\n\n"
            content = new_fm + content
            print("- Created frontmatter with botanical taxonomy.")

        # Add botanical_name, family, genus details in the Admonition block
        # Look for the Variety: line to insert right after or before it (allowing optional Material icons)
        variety_pattern = r'([ \t]*\*\*(?::material-[a-z-]+:\s*)?Variety:\*\*.*?\n)'
        var_match = re.search(variety_pattern, content)
        if var_match:
            original_var = var_match.group(1)
            indent = re.match(r'[ \t]*', original_var).group(0)
            # Check if botanical name is already in content
            if "Botanical Name:" not in content:
                insertion = f"{indent}**Botanical Name:** *{db_botanical}*\n\n{indent}**Family:** {db_data.get('family')}\n\n{indent}**Genus:** {db_data.get('genus')}\n\n"
                content = content.replace(original_var, insertion + original_var)
                print("- Enriched admonition block with taxonomy details.")

        # Add Trefle information under notes
        if "Trefle Database Info:" not in content:
            notes_pattern = r'(## :pushpin: Notes\n)'
            notes_match = re.search(notes_pattern, content)
            if notes_match:
                notes_header = notes_match.group(1)
                trefle_notes = f"\n* **Trefle Database Info:**\n"
                trefle_notes += f"    * **Scientific Name:** *{db_botanical}* ({db_data.get('family')} Family)\n"
                if db_light:
                    trefle_notes += f"    * **Light Level:** {db_light}/10\n"
                if db_ph_min:
                    trefle_notes += f"    * **Preferred Soil pH:** {db_ph_min} - {db_ph_max}\n"
                content = content.replace(notes_header, notes_header + trefle_notes)
                print("- Appended Trefle Database Info to Notes section.")

        with open(args.filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ File updated: {args.filepath}")

if __name__ == "__main__":
    main()
