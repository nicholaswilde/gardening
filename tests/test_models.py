import unittest
import os
import glob
import sys

# Ensure scripts directory is in python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.lib.models import PlantProfile, LogEntry, AdmonitionRow, PlantFrontmatter

SAMPLE_PLANT_MD = """---
common_name: Janet Craig Corn Plant
botanical_name: Dracaena fragrans 'Janet Craig'
type: Dracaena
location: Master Bedroom
instance_id: 1
status: Active
---

# :deciduous_tree: Janet Craig Corn Plant (1)

=== "2026-06-10"

    ![dracaena-janet-craig-1][1]{ loading=lazy }

![dracaena-janet-craig-1-moisture-2026-06-11][2]{ loading=lazy }

!!! example ""

    **:material-leaf: Type:** Houseplant (Dracaena)

    **:material-dna: Variety:** 'Janet Craig'

    **:material-storefront-outline: Origin:** Nursery Start

    **:material-map-marker-outline: Location:** Bedroom

    **:material-calendar-check-outline: Date Planted:** 2026-06-09 (Unknown)

    **:material-list-status: Status:** Active Growth

## :clipboard: Cultivation Status

## :memo: Log & Observations

* **2026-06-11:** A graph of the soilure moisture.
* **2026-06-09:** Initial logging.

## :pushpin: Notes

* **Sensors:** Monitoring temperature and soil moisture levels using a Third Reality 3RSM0147Z sensor.

## :potted_plant: Soil Management

* **2026-06-09:** Initial setup.

## :hourglass_flowing_sand: Crop History

| Year | Season | Crop | Notes |
| :--- | :--- | :--- | :--- |
| | | | |

## :wrench: Care Instructions

See the full [Dracaena Care Guide](../reference/care-guides/dracaena.md) for detailed light and watering protocols.

[1]: <../assets/images/dracaena-janet-craig-1-2026-06-10.webp>
[2]: <../assets/images/dracaena-janet-craig-1-2026-06-11.webp>
"""

class TestPlantProfile(unittest.TestCase):

    def test_parse_sample(self):
        profile = PlantProfile.from_markdown(SAMPLE_PLANT_MD)
        self.assertEqual(profile.frontmatter.common_name, "Janet Craig Corn Plant")
        self.assertEqual(profile.frontmatter.botanical_name, "Dracaena fragrans 'Janet Craig'")
        self.assertEqual(profile.frontmatter.instance_id, 1)
        self.assertEqual(profile.title, ":deciduous_tree: Janet Craig Corn Plant (1)")
        self.assertIn("=== \"2026-06-10\"", profile.header_body)
        self.assertEqual(profile.admonition_title, 'example ""')
        
        # Check admonition values
        self.assertEqual(profile.get_admonition_value("Type"), "Houseplant (Dracaena)")
        self.assertEqual(profile.get_admonition_value("Variety"), "'Janet Craig'")
        self.assertEqual(profile.get_admonition_value("Origin"), "Nursery Start")
        
        # Check logs
        logs = profile.get_log_entries()
        self.assertEqual(len(logs), 2)
        self.assertEqual(logs[0].date, "2026-06-11")
        self.assertEqual(logs[0].message, "A graph of the soilure moisture.")
        self.assertEqual(logs[1].date, "2026-06-09")
        self.assertEqual(logs[1].message, "Initial logging.")
        
        # Check sections
        self.assertIn("## :pushpin: Notes", profile.sections)
        self.assertIn("## :potted_plant: Soil Management", profile.sections)
        
        # Check image references
        self.assertEqual(profile.image_references["1"], "../assets/images/dracaena-janet-craig-1-2026-06-10.webp")
        self.assertEqual(profile.image_references["2"], "../assets/images/dracaena-janet-craig-1-2026-06-11.webp")

    def test_modify_and_serialize(self):
        profile = PlantProfile.from_markdown(SAMPLE_PLANT_MD)
        
        # Modify admonition
        profile.set_admonition_value("Origin", "Bare Root", "material-pine-tree-variant-outline")
        self.assertEqual(profile.get_admonition_value("Origin"), "Bare Root")
        
        # Add a new log entry
        profile.add_log_entry(LogEntry(date="2026-06-12", message="Watered the plant."))
        logs = profile.get_log_entries()
        self.assertEqual(len(logs), 3)
        self.assertEqual(logs[0].date, "2026-06-12")
        self.assertEqual(logs[0].message, "Watered the plant.")
        
        # Add new image reference
        profile.image_references["3"] = "../assets/images/dracaena-janet-craig-1-2026-06-12.webp"
        
        serialized = profile.serialize()
        self.assertIn("**:material-pine-tree-variant-outline: Origin:** Bare Root", serialized)
        self.assertIn("* **2026-06-12:** Watered the plant.", serialized)
        self.assertIn("[3]: <../assets/images/dracaena-janet-craig-1-2026-06-12.webp>", serialized)

    def test_roundtrip_fidelity(self):
        profile = PlantProfile.from_markdown(SAMPLE_PLANT_MD)
        serialized = profile.serialize()
        # Reparse
        profile2 = PlantProfile.from_markdown(serialized)
        
        self.assertEqual(profile.frontmatter.common_name, profile2.frontmatter.common_name)
        self.assertEqual(profile.title, profile2.title)
        self.assertEqual(len(profile.admonition_rows), len(profile2.admonition_rows))
        self.assertEqual(profile.get_admonition_value("Type"), profile2.get_admonition_value("Type"))
        self.assertEqual(profile.image_references, profile2.image_references)

    def test_grid_position(self):
        sample_md = """---
common_name: Oregano
location: raised-bed-1
grid_position: [1, 3]
tags: [active]
---
# :herb: Oregano
"""
        profile = PlantProfile.from_markdown(sample_md)
        self.assertIn("grid_position", PlantFrontmatter.model_fields)
        self.assertEqual(profile.frontmatter.grid_position, [1, 3])

    def test_parse_all_repository_plants(self):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        plant_files = glob.glob(os.path.join(project_root, "docs", "plants", "*.md"))
        self.assertGreater(len(plant_files), 0, "No plant files found in docs/plants")
        
        for filepath in plant_files:
            with self.subTest(filepath=filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                try:
                    profile = PlantProfile.from_markdown(content)
                    self.assertIsNotNone(profile.title)
                    # Test serialization doesn't crash
                    serialized = profile.serialize()
                    self.assertTrue(len(serialized) > 0)
                except Exception as e:
                    self.fail(f"Failed to parse or serialize {os.path.basename(filepath)}: {e}")

if __name__ == "__main__":
    unittest.main()
