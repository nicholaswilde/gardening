#!/usr/bin/env python3
import sys
import os
import re
import urllib.request
import urllib.parse
import json
import argparse

# Ensure the scripts directory is in the path to import lib.models
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.models import PlantProfile

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
    """Extract metadata from markdown file using PlantProfile model."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    profile = PlantProfile.from_markdown(content)
    
    return {
        'title': profile.title,
        'frontmatter': profile.frontmatter.model_dump(),
        'type': profile.get_admonition_value("Type"),
        'variety': profile.get_admonition_value("Variety"),
        'sunlight': profile.get_admonition_value("Sunlight"),
        'soil': profile.get_admonition_value("Soil"),
        'profile': profile,
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

    # Parse markdown file using our model wrapper
    md_data = parse_markdown(args.filepath)
    plant_name = md_data['title']
    
    # Strip emoji or count prefix from title name if needed for clean search
    clean_plant_name = re.sub(r'^:\w+:\s*', '', plant_name) # strip starting emoji
    clean_plant_name = re.sub(r'\s*\(\d+\)$', '', clean_plant_name).strip() # strip ending (1)
    
    md_botanical = md_data['frontmatter'].get('botanical_name')
    search_query = md_botanical if md_botanical else clean_plant_name

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
        print(f"Verifying plant info for '{clean_plant_name}' using Trefle database (query: '{search_query}')...")
        try:
            search_res = query_trefle_search(search_query, token)
            results = search_res.get('data', [])
            if not results:
                print(f"No results found for query '{clean_plant_name}' on Trefle.")
                sys.exit(0)

            best_match = results[0]
            best_score = -1
            
            for r in results:
                scientific = r.get('scientific_name', '').lower()
                common = (r.get('common_name') or '').lower()
                
                score = 0
                if common == clean_plant_name.lower() or scientific == clean_plant_name.lower():
                    score = 3
                elif f" {clean_plant_name.lower()} " in f" {common} " or f" {clean_plant_name.lower()} " in f" {scientific} ":
                    score = 2
                elif clean_plant_name.lower() in common or clean_plant_name.lower() in scientific:
                    score = 1
                
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
        print(f"❌ Variety: Discrepancy! Found copy-paste placeholder '{variety}' which belongs to Rosemary, not {clean_plant_name}.")
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
        profile = md_data['profile']
        
        # Replace variety placeholder if it's the rosemary one
        if variety and "Tuscan Blue" in variety:
            new_variety = "Greek Oregano" if "oregano" in clean_plant_name.lower() else "Common"
            profile.set_admonition_value("Variety", new_variety)
            print(f"- Replaced placeholder variety with '{new_variety}'.")

        # Ensure botanical_name, family, and genus are added to frontmatter
        profile.frontmatter.botanical_name = db_botanical
        profile.frontmatter.family = db_data.get('family')
        profile.frontmatter.genus = db_data.get('genus')
        print("- Enriched frontmatter with botanical taxonomy.")

        # Add botanical_name, family, genus details in the Admonition block
        # We set them on the admonition using standardized icons
        if not profile.get_admonition_value("Botanical Name"):
            profile.set_admonition_value("Botanical Name", f"*{db_botanical}*")
        if not profile.get_admonition_value("Family"):
            profile.set_admonition_value("Family", db_data.get('family'))
        if not profile.get_admonition_value("Genus"):
            profile.set_admonition_value("Genus", db_data.get('genus'))
        print("- Enriched admonition block with taxonomy details.")

        # Add Trefle information under notes section
        notes_header = "## :pushpin: Notes"
        if notes_header not in profile.sections:
            profile.sections[notes_header] = ""
            
        notes_content = profile.sections[notes_header]
        if "Trefle Database Info:" not in notes_content:
            trefle_notes = f"\n* **Trefle Database Info:**\n"
            trefle_notes += f"    * **Scientific Name:** *{db_botanical}* ({db_data.get('family')} Family)\n"
            if db_light is not None:
                trefle_notes += f"    * **Light Level:** {db_light}/10\n"
            if db_ph_min is not None:
                trefle_notes += f"    * **Preferred Soil pH:** {db_ph_min} - {db_ph_max}\n"
            profile.sections[notes_header] = notes_content.rstrip() + "\n" + trefle_notes
            print("- Appended Trefle Database Info to Notes section.")

        with open(args.filepath, 'w', encoding='utf-8') as f:
            f.write(profile.serialize())
        print(f"✅ File updated: {args.filepath}")

if __name__ == "__main__":
    main()
