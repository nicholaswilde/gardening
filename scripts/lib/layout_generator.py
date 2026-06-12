import re
from typing import List, Dict, Any, Optional

# Emoji dictionary based on plant common names
EMOJI_MAPPING = {
    "tomato": "🍅",
    "pepper": "🌶️",
    "chili": "🌶️",
    "strawberry": "🍓",
    "phlox": "🌸",
    "impatiens": "🌺",
    "rose": "🌹",
    "lavender": "🪻",
    "iris": "🪻",
    "lily": "🪻",
    "rosemary": "🌿",
    "oregano": "🌿",
    "thyme": "🌿",
    "basil": "🌿",
    "chives": "🌿",
    "cilantro": "🌿",
    "sage": "🌿",
    "mint": "🌿",
    "parsley": "🌿",
    "fern": "🌿",
}

def get_emoji_for_plant(common_name: str) -> str:
    name_lower = common_name.lower()
    for key in sorted(EMOJI_MAPPING.keys(), key=len, reverse=True):
        if key in name_lower:
            return EMOJI_MAPPING[key]
    return "🌿"

def validate_placements(placements: List[Dict[str, Any]]) -> None:
    """
    Validates that:
    1. Grid coordinates are within 2x4 boundaries (Row 1-2, Column 1-4).
    2. There are no placement collisions (multiple plants in the same coordinate).
    """
    seen_coords = set()
    for p in placements:
        pos = p.get("grid_position")
        if not pos or len(pos) != 2:
            raise ValueError(f"Invalid grid_position: {pos} for {p.get('common_name')}")
        
        row, col = pos[0], pos[1]
        if not (1 <= row <= 2) or not (1 <= col <= 4):
            raise ValueError(f"Grid position {pos} for {p.get('common_name')} is out of bounds (Row 1-2, Col 1-4).")
        
        coord = (row, col)
        if coord in seen_coords:
            raise ValueError(f"Collision detected at {pos} for {p.get('common_name')}")
        seen_coords.add(coord)

def generate_mermaid_layout(bed_title: str, dimensions: str, placements: List[Dict[str, Any]]) -> str:
    """
    Compiles the placements to a flowchart TD Mermaid diagram matching the project style guide.
    """
    validate_placements(placements)
    
    # Initialize a 2x4 grid
    grid = [[None for _ in range(4)] for _ in range(2)]
    
    for p in placements:
        row, col = p["grid_position"][0], p["grid_position"][1]
        grid[row - 1][col - 1] = p
        
    lines = []
    lines.append("flowchart TD")
    lines.append(f'    subgraph Bed ["{bed_title} ({dimensions})"]')
    lines.append("        direction TB")
    
    # Generate Row subgraphs
    for r in range(1, 3):
        lines.append(f'        subgraph Row{r} ["Row {r}"]')
        lines.append("            direction LR")
        
        cell_definitions = []
        for c in range(1, 5):
            plant = grid[r - 1][c - 1]
            cell_id = f"cell{r}_{c}"
            
            if plant:
                name = plant["common_name"]
                emoji = get_emoji_for_plant(name)
                # Ensure the name does not have any double quotes to break Mermaid
                clean_name = name.replace('"', '\\"')
                status = plant.get("status", "Active")
                cell_definitions.append(f'{cell_id}["{emoji} {clean_name}<br>({status})"]')
            else:
                cell_definitions.append(f'{cell_id}["🟫 Fallow / Compost<br>(Empty)"]')
                
        for cell_def in cell_definitions:
            lines.append(f"            {cell_def}")
        lines.append("        end")
        
    lines.append("    end")
    lines.append("")
    
    # Styling classes
    lines.append("    style Bed fill:transparent,stroke:#b4befe,stroke-width:2px")
    
    for r in range(1, 3):
        for c in range(1, 5):
            cell_id = f"cell{r}_{c}"
            plant = grid[r - 1][c - 1]
            if plant:
                lines.append(f"    style {cell_id} fill:#313244,stroke:#a6e3a1,stroke-width:2px,color:#cdd6f4,rx:5,ry:5")
            else:
                lines.append(f"    style {cell_id} fill:#1e1e2e,stroke:#585b70,stroke-width:2px,color:#a6adc8,stroke-dasharray: 5 5,rx:5,ry:5")
                
    lines.append("")
    
    # Click events
    for p in placements:
        row, col = p["grid_position"][0], p["grid_position"][1]
        cell_id = f"cell{row}_{col}"
        path = p["relative_path"]
        name = p["common_name"]
        lines.append(f'    click {cell_id} "{path}" "{name} Profile"')
        
    return "\n".join(lines) + "\n"
