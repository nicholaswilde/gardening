import unittest
import os
import sys
import tempfile
import shutil

# Ensure scripts directory is in python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generate_layouts import (
    scan_active_plants,
    inject_layout_into_bed,
    parse_bed_metadata
)

class TestGenerateLayouts(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.plants_dir = os.path.join(self.test_dir, "docs", "plants")
        self.beds_dir = os.path.join(self.test_dir, "docs", "beds")
        os.makedirs(self.plants_dir)
        os.makedirs(self.beds_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_parse_bed_metadata(self):
        bed_content = """# :brown_square: Raised Bed 2

!!! example ""

    **:material-list-status: Status:** Active  

    **:material-ruler-square: Dimensions:** 4' x 8' x 1.5' (48 cu ft)  
"""
        title, dims = parse_bed_metadata(bed_content)
        self.assertEqual(title, "Raised Bed 2")
        self.assertEqual(dims, "4' x 8'")

    def test_scan_active_plants(self):
        # Create an active plant with grid position
        plant_active = """---
tags: [herb, active]
location: raised-bed-2
grid_position: [1, 2]
common_name: Rosemary
---
# :herb: Rosemary
"""
        # Create an inactive plant
        plant_inactive = """---
tags: [herb]
location: raised-bed-2
grid_position: [1, 3]
common_name: Thyme
---
# :herb: Thyme
"""
        # Create an active plant without grid position
        plant_no_grid = """---
tags: [herb, active]
location: raised-bed-2
common_name: Oregano
---
# :herb: Oregano
"""
        with open(os.path.join(self.plants_dir, "rosemary.md"), "w", encoding="utf-8") as f:
            f.write(plant_active)
        with open(os.path.join(self.plants_dir, "thyme.md"), "w", encoding="utf-8") as f:
            f.write(plant_inactive)
        with open(os.path.join(self.plants_dir, "oregano.md"), "w", encoding="utf-8") as f:
            f.write(plant_no_grid)

        plants = scan_active_plants(self.plants_dir)
        self.assertEqual(len(plants), 1)
        self.assertEqual(plants[0]["common_name"], "Rosemary")
        self.assertEqual(plants[0]["grid_position"], [1, 2])
        self.assertEqual(plants[0]["location"], "raised-bed-2")

    def test_inject_layout_into_bed(self):
        bed_content = """# Raised Bed 2

<!-- BED_LAYOUT_START -->
OLD MERMAID
<!-- BED_LAYOUT_END -->

Rest of the file.
"""
        mermaid_diagram = "NEW MERMAID DIAGRAM\n"
        updated = inject_layout_into_bed(bed_content, mermaid_diagram)
        
        self.assertIn("<!-- BED_LAYOUT_START -->", updated)
        self.assertIn("NEW MERMAID DIAGRAM", updated)
        self.assertIn("<!-- BED_LAYOUT_END -->", updated)
        self.assertNotIn("OLD MERMAID", updated)
        self.assertIn("Rest of the file.", updated)

if __name__ == "__main__":
    unittest.main()
