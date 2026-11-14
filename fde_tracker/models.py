from dataclasses import dataclass, asdict
from typing import List, Dict, Any

@dataclass
class FDERole:
    id: int
    company: str
    title: str
    department: str
    location: str
    remote_friendly: bool
    comp_range: str
    category: str
    tech_stack: List[str]
    summary: str
    url: str
    posted_period: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FDERole":
        return cls(
            id=int(data["id"]),
            company=str(data["company"]),
            title=str(data["title"]),
            department=str(data.get("department", "Engineering")),
            location=str(data["location"]),
            remote_friendly=bool(data.get("remote_friendly", False)),
            comp_range=str(data.get("comp_range", "Competitive")),
            category=str(data.get("category", "General")),
            tech_stack=list(data.get("tech_stack", [])),
            summary=str(data.get("summary", "")),
            url=str(data.get("url", "")),
            posted_period=str(data.get("posted_period", "Active"))
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
