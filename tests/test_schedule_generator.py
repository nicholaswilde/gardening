import unittest
import os
import sys
from datetime import datetime, date

# Ensure scripts directory is in python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.lib.models import PlantProfile, PlantFrontmatter
# We will create scripts/generate_schedule.py with these core functions
from scripts.generate_schedule import (
    parse_care_schedule,
    get_last_action_date,
    calculate_next_date,
    generate_schedule_markdown,
    generate_ics
)

class TestScheduleGenerator(unittest.TestCase):

    def setUp(self):
        # Create a plant profile with frontmatter care schedule and logs
        self.plant_md = """---
common_name: Sungold Tomato
tags: [active]
location: raised-bed-3
planted: 2026-06-01
care_schedule:
  water: 3
  fertilize: 14
---
# :tomato: Sungold Tomato

## :memo: Log & Observations

* **2026-06-10:** Watered the tomato plant and pinched off suckers.
* **2026-06-02:** Initial log entry.
"""
        self.profile = PlantProfile.from_markdown(self.plant_md)

    def test_parse_care_schedule(self):
        schedule = parse_care_schedule(self.profile)
        self.assertEqual(schedule, {"water": 3, "fertilize": 14})

    def test_get_last_action_date_from_logs(self):
        # Test finding action in logs
        last_water = get_last_action_date(self.profile, "water")
        self.assertEqual(last_water, date(2026, 6, 10))

    def test_get_last_action_date_fallback_planted(self):
        # Test falling back to planted date because 'fertilize' is not logged
        last_fertilize = get_last_action_date(self.profile, "fertilize")
        self.assertEqual(last_fertilize, date(2026, 6, 1))

    def test_calculate_next_date(self):
        # Last water was 2026-06-10, interval is 3 days -> next water is 2026-06-13
        next_water = calculate_next_date(date(2026, 6, 10), 3)
        self.assertEqual(next_water, date(2026, 6, 13))

        # Last fertilize was 2026-06-01, interval is 14 days -> next fertilize is 2026-06-15
        next_fertilize = calculate_next_date(date(2026, 6, 1), 14)
        self.assertEqual(next_fertilize, date(2026, 6, 15))

    def test_generate_schedule_markdown(self):
        # Create mock schedule data
        # list of dicts: plant common name, location, action, last_date, next_date, relative path
        current_date = date(2026, 6, 11)
        tasks = [
            {
                "common_name": "Sungold Tomato",
                "location": "raised-bed-3",
                "action": "fertilize",
                "next_date": date(2026, 6, 15),
                "relative_path": "plants/sungold-tomato.md"
            },
            {
                "common_name": "Oregano",
                "location": "raised-bed-2",
                "action": "water",
                "next_date": date(2026, 6, 10),  # Overdue
                "relative_path": "plants/oregano.md"
            },
            {
                "common_name": "Rosemary",
                "location": "raised-bed-2",
                "action": "water",
                "next_date": date(2026, 6, 11),  # Today
                "relative_path": "plants/rosemary.md"
            }
        ]
        
        markdown = generate_schedule_markdown(tasks, current_date)
        
        self.assertIn("# :calendar: Gardening Maintenance Schedule", markdown)
        self.assertIn("Overdue Tasks", markdown)
        self.assertIn("Oregano", markdown)
        self.assertIn("Sungold Tomato", markdown)
        self.assertIn("Rosemary", markdown)
        self.assertIn("water", markdown.lower())
        self.assertIn("fertilize", markdown.lower())

    def test_generate_ics(self):
        import tempfile
        tasks = [
            {
                "common_name": "Sungold Tomato",
                "location": "raised-bed-3",
                "action": "fertilize",
                "next_date": date(2026, 6, 15),
                "relative_path": "plants/sungold-tomato.md"
            }
        ]
        
        with tempfile.NamedTemporaryFile(suffix=".ics", delete=False) as tmp:
            tmp_path = tmp.name
            
        try:
            generate_ics(tasks, tmp_path)
            with open(tmp_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            self.assertIn("BEGIN:VCALENDAR", content)
            self.assertIn("VERSION:2.0", content)
            self.assertIn("SUMMARY:Fertilize: Sungold Tomato (raised-bed-3)", content)
            self.assertIn("DTSTART;VALUE=DATE:20260615", content)
            self.assertIn("DTEND;VALUE=DATE:20260616", content)
            self.assertIn("END:VCALENDAR", content)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

if __name__ == "__main__":
    unittest.main()
