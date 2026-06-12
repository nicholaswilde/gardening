import re
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict
import frontmatter

# Icons mapping matching style-guide.md
STANDARD_ICONS = {
    "Type": "material-leaf",
    "Variety": "material-dna",
    "Origin": "material-storefront-outline",
    "Location": "material-map-marker-outline",
    "Date Planted": "material-calendar-check-outline",
    "Status": "material-list-status",
    "Sunlight": "material-weather-sunny",
    "Soil": "material-texture",
    "Botanical Name": "material-tag-text-outline",
    "Family": "material-sitemap-outline",
    "Genus": "material-folder-outline",
    "Date Removed": "material-calendar-remove-outline",
    "Outcome": "material-chat-alert-outline"
}

# Standard origin icons from style-guide.md
ORIGIN_ICONS = {
    "Seed (Indoor Start)": "material-seed",
    "Seed (Direct Sow)": "material-seed-outline",
    "Nursery Start": "material-storefront-outline",
    "Bare Root": "material-pine-tree-variant-outline",
    "Cutting / Clone": "material-content-cut",
    "Division": "material-call-split",
    "Volunteer": "material-recycle",
    "Gifted transplant": "material-gift-outline",
    "Living herb": "material-store-outline"
}

class PlantFrontmatter(BaseModel):
    model_config = ConfigDict(extra="allow")
    common_name: Optional[str] = None
    botanical_name: Optional[str] = None
    type: Optional[str] = None
    location: Optional[str] = None
    instance_id: Optional[Any] = None
    status: Optional[str] = None
    tags: Optional[List[str]] = None
    planted: Optional[Any] = None
    family: Optional[str] = None
    genus: Optional[str] = None
    removed: Optional[Any] = None
    grid_position: Optional[List[int]] = None

class AdmonitionRow(BaseModel):
    key: str
    value: str
    icon: Optional[str] = None

    def serialize(self) -> str:
        icon_str = f":{self.icon}: " if self.icon else ""
        return f"**{icon_str}{self.key}:** {self.value}"

class LogEntry(BaseModel):
    date: str
    message: str

    def serialize(self) -> str:
        return f"* **{self.date}:** {self.message}"

class PlantProfile(BaseModel):
    frontmatter: PlantFrontmatter
    title: str  # H1 title line (without # prefix)
    header_body: str = ""  # Content between title and admonition
    admonition_title: Optional[str] = None  # e.g., 'example ""'
    admonition_rows: List[AdmonitionRow] = Field(default_factory=list)
    sections: Dict[str, str] = Field(default_factory=dict)  # heading -> raw content under it
    image_references: Dict[str, str] = Field(default_factory=dict)  # label -> path/url

    @classmethod
    def from_markdown(cls, text: str) -> "PlantProfile":
        # Load frontmatter
        post = frontmatter.loads(text)
        fm = PlantFrontmatter.model_validate(post.metadata)
        
        # Parse body
        body = post.content
        lines = body.splitlines()
        
        title = ""
        header_body_lines = []
        admonition_title = None
        admonition_lines = []
        sections = {}
        image_references = {}
        
        # Parse states
        # 0 = searching title
        # 1 = header body
        # 2 = reading admonition
        # 3 = reading sections/body
        state = 0
        current_section = None
        current_section_lines = []
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Check for image references at the end
            ref_match = re.match(r'^\[([^\]]+)\]:\s*<([^>]+)>$', line.strip())
            if not ref_match:
                ref_match = re.match(r'^\[([^\]]+)\]:\s*([^\s]+)$', line.strip())
            if ref_match:
                image_references[ref_match.group(1)] = ref_match.group(2)
                i += 1
                continue
                
            if state == 0:
                if line.strip().startswith("#"):
                    title = line.lstrip("#").strip()
                    state = 1
                elif line.strip():
                    header_body_lines.append(line)
                    state = 1
            elif state == 1:
                if line.strip().startswith("!!!"):
                    admonition_title = line.strip().lstrip("!").strip()
                    state = 2
                elif line.strip().startswith("##"):
                    current_section = line.strip()
                    current_section_lines = []
                    state = 3
                else:
                    header_body_lines.append(line)
            elif state == 2:
                if line.startswith("    ") or line.startswith("\t") or not line.strip():
                    admonition_lines.append(line)
                elif line.strip().startswith("##"):
                    current_section = line.strip()
                    current_section_lines = []
                    state = 3
                else:
                    header_body_lines.append(line)
                    state = 1
            elif state == 3:
                if line.strip().startswith("##"):
                    if current_section:
                        sections[current_section] = "\n".join(current_section_lines)
                    current_section = line.strip()
                    current_section_lines = []
                else:
                    current_section_lines.append(line)
            i += 1
            
        if current_section:
            sections[current_section] = "\n".join(current_section_lines)
            
        # Parse admonition lines into rows
        admonition_rows = []
        admonition_row_re = re.compile(r'^[ \t]*\*\*(?::([a-zA-Z0-9_-]+):\s*)?([^:]+):\*\*\s*(.*)$')
        
        for aline in admonition_lines:
            sline = aline.strip()
            if not sline:
                continue
            m = admonition_row_re.match(sline)
            if m:
                icon = m.group(1)
                key = m.group(2).strip()
                val = m.group(3).strip()
                admonition_rows.append(AdmonitionRow(key=key, value=val, icon=icon))
            else:
                admonition_rows.append(AdmonitionRow(key="", value=sline))
                
        header_body = "\n".join(header_body_lines)
        
        return cls(
            frontmatter=fm,
            title=title,
            header_body=header_body,
            admonition_title=admonition_title,
            admonition_rows=admonition_rows,
            sections=sections,
            image_references=image_references
        )

    def get_admonition_value(self, key: str) -> Optional[str]:
        for row in self.admonition_rows:
            if row.key.lower() == key.lower():
                return row.value
        return None

    def set_admonition_value(self, key: str, value: str, icon: Optional[str] = None):
        # Update existing
        for row in self.admonition_rows:
            if row.key.lower() == key.lower():
                row.value = value
                if icon:
                    row.icon = icon
                return
        # Or add new
        if not icon:
            icon = STANDARD_ICONS.get(key)
        self.admonition_rows.append(AdmonitionRow(key=key, value=value, icon=icon))

    def get_log_entries(self) -> List[LogEntry]:
        log_section_key = None
        for heading in self.sections.keys():
            if "Log & Observations" in heading:
                log_section_key = heading
                break
                
        if not log_section_key:
            return []
            
        content = self.sections[log_section_key]
        entries = []
        log_re = re.compile(r'^\s*\*\s*\*\*(\d{4}-\d{2}-\d{2}):\*\*\s*(.*)$')
        for line in content.splitlines():
            m = log_re.match(line)
            if m:
                entries.append(LogEntry(date=m.group(1), message=m.group(2).strip()))
        return entries

    def set_log_entries(self, entries: List[LogEntry]):
        log_section_key = None
        for heading in self.sections.keys():
            if "Log & Observations" in heading:
                log_section_key = heading
                break
                
        if not log_section_key:
            log_section_key = "## :memo: Log & Observations"
            
        serialized_entries = [entry.serialize() for entry in entries]
        self.sections[log_section_key] = "\n" + "\n".join(serialized_entries) + "\n"

    def add_log_entry(self, entry: LogEntry):
        entries = self.get_log_entries()
        entries.insert(0, entry)
        self.set_log_entries(entries)

    def serialize(self) -> str:
        metadata = self.frontmatter.model_dump(exclude_none=True)
        post = frontmatter.Post(content="", **metadata)
        fm_str = frontmatter.dumps(post)
        
        body_parts = []
        body_parts.append(f"# {self.title}")
        
        if self.header_body.strip():
            body_parts.append(self.header_body.strip())
            
        if self.admonition_title:
            admon_block = [f"!!! {self.admonition_title}"]
            for i, row in enumerate(self.admonition_rows):
                if i > 0:
                    admon_block.append("")
                if row.key == "":
                    admon_block.append(f"    {row.value}")
                else:
                    admon_block.append(f"    {row.serialize()}")
            body_parts.append("\n".join(admon_block))
            
        for heading, content in self.sections.items():
            body_parts.append(heading)
            if content.strip():
                body_parts.append(content.strip())
                
        if self.image_references:
            ref_lines = []
            for label, path in sorted(self.image_references.items(), key=lambda x: x[0]):
                if path.startswith("<") and path.endswith(">"):
                    ref_lines.append(f"[{label}]: {path}")
                else:
                    ref_lines.append(f"[{label}]: <{path}>")
            body_parts.append("\n".join(ref_lines))
            
        return fm_str.strip() + "\n\n" + "\n\n".join(body_parts) + "\n"
