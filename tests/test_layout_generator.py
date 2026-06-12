import unittest
import os
import sys

# Ensure scripts directory is in python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.lib.layout_generator import generate_mermaid_layout, validate_placements

class TestLayoutGenerator(unittest.TestCase):

    def setUp(self):
        self.bed_id = "raised-bed-2"
        self.bed_title = "Raised Bed 2"
        self.dimensions = "4' x 8'"
        self.valid_placements = [
            {
                "grid_position": [1, 1],
                "common_name": "Rosemary",
                "status": "Active",
                "relative_path": "../plants/rosemary.md"
            },
            {
                "grid_position": [1, 2],
                "common_name": "Rosemary",
                "status": "Active",
                "relative_path": "../plants/rosemary.md"
            },
            {
                "grid_position": [1, 3],
                "common_name": "Greek Oregano",
                "status": "Active",
                "relative_path": "../plants/oregano.md"
            },
            {
                "grid_position": [2, 4],
                "common_name": "Thyme",
                "status": "Active",
                "relative_path": "../plants/thyme.md"
            }
        ]

    def test_validate_placements_valid(self):
        # Should not raise any exceptions
        validate_placements(self.valid_placements)

    def test_validate_placements_collision(self):
        invalid_placements = [
            {
                "grid_position": [1, 1],
                "common_name": "Rosemary",
                "status": "Active",
                "relative_path": "../plants/rosemary.md"
            },
            {
                "grid_position": [1, 1],  # Collision!
                "common_name": "Thyme",
                "status": "Active",
                "relative_path": "../plants/thyme.md"
            }
        ]
        with self.assertRaises(ValueError) as context:
            validate_placements(invalid_placements)
        self.assertIn("Collision", str(context.exception))

    def test_validate_placements_out_of_bounds(self):
        # Row out of bounds
        invalid_row = [
            {
                "grid_position": [3, 1],
                "common_name": "Rosemary",
                "status": "Active",
                "relative_path": "../plants/rosemary.md"
            }
        ]
        with self.assertRaises(ValueError) as context:
            validate_placements(invalid_row)
        self.assertIn("out of bounds", str(context.exception))

        # Col out of bounds
        invalid_col = [
            {
                "grid_position": [1, 5],
                "common_name": "Rosemary",
                "status": "Active",
                "relative_path": "../plants/rosemary.md"
            }
        ]
        with self.assertRaises(ValueError) as context:
            validate_placements(invalid_col)
        self.assertIn("out of bounds", str(context.exception))

        # 0-indexed or negative coords should fail
        invalid_zero = [
            {
                "grid_position": [0, 1],
                "common_name": "Rosemary",
                "status": "Active",
                "relative_path": "../plants/rosemary.md"
            }
        ]
        with self.assertRaises(ValueError) as context:
            validate_placements(invalid_zero)
        self.assertIn("out of bounds", str(context.exception))

    def test_generate_mermaid_layout(self):
        mermaid = generate_mermaid_layout(
            bed_title=self.bed_title,
            dimensions=self.dimensions,
            placements=self.valid_placements
        )
        
        # Verify basic structure
        self.assertIn("flowchart TD", mermaid)
        self.assertIn('subgraph Bed ["Raised Bed 2 (4\' x 8\')"]', mermaid)
        self.assertIn('subgraph Row1 ["Row 1"]', mermaid)
        self.assertIn('subgraph Row2 ["Row 2"]', mermaid)
        
        # Verify cell nodes
        self.assertIn('cell1_1["🌿 Rosemary<br>(Active)"]', mermaid)
        self.assertIn('cell1_2["🌿 Rosemary<br>(Active)"]', mermaid)
        self.assertIn('cell1_3["🌿 Greek Oregano<br>(Active)"]', mermaid)
        self.assertIn('cell2_4["🌿 Thyme<br>(Active)"]', mermaid)

        # Verify fallow/compost nodes
        self.assertIn('cell1_4["🟫 Fallow / Compost<br>(Empty)"]', mermaid)
        self.assertIn('cell2_1["🟫 Fallow / Compost<br>(Empty)"]', mermaid)
        self.assertIn('cell2_2["🟫 Fallow / Compost<br>(Empty)"]', mermaid)
        self.assertIn('cell2_3["🟫 Fallow / Compost<br>(Empty)"]', mermaid)

        # Verify styles (Catppuccin Mocha palette)
        self.assertIn("style Bed fill:transparent,stroke:#b4befe,stroke-width:2px", mermaid)
        self.assertIn("style cell1_1 fill:#313244,stroke:#a6e3a1,stroke-width:2px,color:#cdd6f4,rx:5,ry:5", mermaid)
        self.assertIn("style cell1_4 fill:#1e1e2e,stroke:#585b70,stroke-width:2px,color:#a6adc8,stroke-dasharray: 5 5,rx:5,ry:5", mermaid)

        # Verify click handlers
        self.assertIn('click cell1_1 "../plants/rosemary.md" "Rosemary Profile"', mermaid)
        self.assertIn('click cell1_3 "../plants/oregano.md" "Greek Oregano Profile"', mermaid)

    def test_emoji_mapping(self):
        emoji_placements = [
            {
                "grid_position": [1, 1],
                "common_name": "Sungold Tomato",
                "status": "Active",
                "relative_path": "../plants/sungold-tomato.md"
            },
            {
                "grid_position": [1, 2],
                "common_name": "Jalapeno Pepper",
                "status": "Active",
                "relative_path": "../plants/jalapeno-pepper.md"
            },
            {
                "grid_position": [1, 3],
                "common_name": "Wild Strawberry",
                "status": "Active",
                "relative_path": "../plants/wild-strawberry.md"
            }
        ]
        mermaid = generate_mermaid_layout(
            bed_title=self.bed_title,
            dimensions=self.dimensions,
            placements=emoji_placements
        )
        self.assertIn('cell1_1["🍅 Sungold Tomato<br>(Active)"]', mermaid)
        self.assertIn('cell1_2["🌶️ Jalapeno Pepper<br>(Active)"]', mermaid)
        self.assertIn('cell1_3["🍓 Wild Strawberry<br>(Active)"]', mermaid)

if __name__ == "__main__":
    unittest.main()
