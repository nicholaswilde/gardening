#!/usr/bin/env python3
import os
import re
import glob
import sys
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Tuple, Optional

# Add scripts directory to path to import models
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from lib.models import PlantProfile, LogEntry

ACTION_KEYWORDS = {
    "water": ["water", "irrigation", "irrigated"],
    "fertilize": ["fertiliz", "fed", "feed"],
    "prune": ["prun", "pinch", "cut back"],
    "repot": ["repot", "transplant"]
}

def to_date(val: Any) -> Optional[date]:
    if not val:
        return None
    if isinstance(val, date):
        return val
    if isinstance(val, datetime):
        return val.date()
    if isinstance(val, str):
        try:
            return datetime.strptime(val.strip(), "%Y-%m-%d").date()
        except ValueError:
            pass
    return None

def parse_care_schedule(profile: PlantProfile) -> Dict[str, int]:
    """
    Parses care schedule intervals (in days) from plant frontmatter.
    """
    fm = profile.frontmatter
    extra = getattr(fm, "model_extra", {}) or {}
    schedule = extra.get("care_schedule")
    if not schedule and hasattr(fm, "care_schedule"):
        schedule = getattr(fm, "care_schedule")
    return schedule or {}

def is_action_in_log(action: str, log_message: str) -> bool:
    msg_lower = log_message.lower()
    keywords = ACTION_KEYWORDS.get(action.lower(), [action.lower()])
    return any(kw in msg_lower for kw in keywords)

def get_last_action_date(profile: PlantProfile, action: str) -> Optional[date]:
    """
    Finds the last date an action was performed by parsing plant logs.
    Falls back to the planted date if no matching logs exist.
    """
    logs = profile.get_log_entries()
    last_date = None
    
    for entry in logs:
        if is_action_in_log(action, entry.message):
            entry_date = to_date(entry.date)
            if entry_date:
                if not last_date or entry_date > last_date:
                    last_date = entry_date
                    
    if last_date:
        return last_date
        
    # Fallback to planted date
    return to_date(profile.frontmatter.planted)

def calculate_next_date(last_date: date, interval_days: int) -> date:
    """
    Calculates the next scheduled date by adding the interval to the last date.
    """
    return last_date + timedelta(days=interval_days)

def generate_schedule_markdown(tasks: List[Dict[str, Any]], current_date: date) -> str:
    """
    Generates a structured markdown schedule from a list of calculated tasks.
    """
    # Separate overdue and upcoming
    overdue_tasks = []
    upcoming_tasks = []
    
    for t in tasks:
        if t["next_date"] < current_date:
            overdue_tasks.append(t)
        else:
            upcoming_tasks.append(t)
            
    # Sort
    overdue_tasks.sort(key=lambda x: x["next_date"])
    upcoming_tasks.sort(key=lambda x: x["next_date"])
    
    lines = []
    lines.append("# :calendar: Gardening Maintenance Schedule")
    lines.append("")
    lines.append(f"Last updated: {current_date.strftime('%Y-%m-%d')}")
    lines.append("")
    
    # Render Overdue section
    if overdue_tasks:
        lines.append("## :warning: Overdue Tasks")
        lines.append("")
        for t in overdue_tasks:
            days_ago = (current_date - t["next_date"]).days
            days_str = f"{days_ago} day ago" if days_ago == 1 else f"{days_ago} days ago"
            lines.append(f"- **[{t['common_name']}]({t['relative_path']}) ({t['location']}):** {t['action'].title()} (Overdue since {t['next_date'].strftime('%Y-%m-%d')}, {days_str})")
        lines.append("")
        
    # Group upcoming by week start (Monday)
    upcoming_weeks = {}
    current_week_start = current_date - timedelta(days=current_date.weekday())
    
    for t in upcoming_tasks:
        d = t["next_date"]
        w_start = d - timedelta(days=d.weekday())
        if w_start not in upcoming_weeks:
            upcoming_weeks[w_start] = {}
        if d not in upcoming_weeks[w_start]:
            upcoming_weeks[w_start][d] = []
        upcoming_weeks[w_start][d].append(t)
        
    # Render weeks
    for w_start in sorted(upcoming_weeks.keys()):
        week_str = w_start.strftime("%Y-%m-%d")
        if w_start == current_week_start:
            lines.append(f"## :calendar: Week of {week_str} (Current Week)")
        else:
            lines.append(f"## :calendar: Week of {week_str}")
        lines.append("")
        
        days_in_week = upcoming_weeks[w_start]
        for d in sorted(days_in_week.keys()):
            lines.append(f"### {d.strftime('%Y-%m-%d (%A)')}")
            for t in days_in_week[d]:
                lines.append(f"- **[{t['common_name']}]({t['relative_path']}) ({t['location']}):** {t['action'].title()}")
            lines.append("")
            
    if not overdue_tasks and not upcoming_tasks:
        lines.append("No active scheduled tasks found. Add a `care_schedule` to active plant profiles.")
        lines.append("")
        
    return "\n".join(lines)

def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    plants_dir = os.path.join(project_root, "docs", "plants")
    out_file = os.path.join(project_root, "docs", "schedule.md")
    
    plant_files = glob.glob(os.path.join(plants_dir, "*.md"))
    tasks = []
    
    for filepath in plant_files:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                
            profile = PlantProfile.from_markdown(content)
            # Skip if not active
            if not profile.frontmatter.tags or "active" not in profile.frontmatter.tags:
                continue
                
            schedule = parse_care_schedule(profile)
            if not schedule:
                continue
                
            location = profile.frontmatter.location or "Unknown location"
            common_name = profile.frontmatter.common_name or profile.title or os.path.splitext(os.path.basename(filepath))[0].replace("-", " ").title()
            # Clean emoji/prefix from name
            common_name = re.sub(r'^:\w+:\s*', '', common_name)
            
            for action, interval in schedule.items():
                last_date = get_last_action_date(profile, action)
                if not last_date:
                    # If absolutely no date can be resolved, use current date
                    last_date = date.today()
                    
                next_date = calculate_next_date(last_date, interval)
                
                tasks.append({
                    "common_name": common_name,
                    "location": location,
                    "action": action,
                    "next_date": next_date,
                    "relative_path": f"plants/{os.path.basename(filepath)}"
                })
        except Exception as e:
            print(f"Warning: Failed to process plant {os.path.basename(filepath)}: {e}", file=sys.stderr)
            
    current_date = date.today()
    markdown = generate_schedule_markdown(tasks, current_date)
    
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(markdown)
        
    print(f"Successfully generated schedule to {out_file}")

if __name__ == "__main__":
    main()
