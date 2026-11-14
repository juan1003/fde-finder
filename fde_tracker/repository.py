import json
from pathlib import Path
from typing import List, Optional
from .models import FDERole

class RoleRepository:
    """
    Filesystem repository for managing FDE role data.
    Uses Python's pathlib.Path for cross-platform, robust file handling.
    """
    def __init__(self, data_file: Optional[Path] = None):
        if data_file is None:
            # Resolve relative to the repository package root
            base_dir = Path(__file__).resolve().parent.parent
            self.data_dir = base_dir / "data"
            self.data_file = self.data_dir / "fde_roles.json"
        else:
            self.data_file = Path(data_file).resolve()
            self.data_dir = self.data_file.parent

    def load_roles(self) -> List[FDERole]:
        """Load and parse FDE roles from the JSON file on the filesystem."""
        if not self.data_file.exists():
            raise FileNotFoundError(
                f"Data file not found at: {self.data_file}. "
                f"Ensure the dataset is placed under {self.data_dir}."
            )

        content = self.data_file.read_text(encoding="utf-8")
        raw_list = json.loads(content)
        return [FDERole.from_dict(item) for item in raw_list]

    def save_roles(self, roles: List[FDERole]) -> None:
        """Save a list of FDE roles back to the filesystem."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        serialized = [role.to_dict() for role in roles]
        self.data_file.write_text(
            json.dumps(serialized, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8"
        )

    def filter_roles(
        self,
        query: Optional[str] = None,
        company: Optional[str] = None,
        remote_only: bool = False,
        category: Optional[str] = None
    ) -> List[FDERole]:
        """Query and filter roles based on attributes."""
        roles = self.load_roles()
        if company:
            comp_q = company.lower()
            roles = [r for r in roles if comp_q in r.company.lower()]
        if remote_only:
            roles = [r for r in roles if r.remote_friendly]
        if category:
            cat_q = category.lower()
            roles = [r for r in roles if cat_q in r.category.lower()]
        if query:
            q = query.lower()
            roles = [
                r for r in roles
                if q in r.company.lower()
                or q in r.title.lower()
                or q in r.location.lower()
                or any(q in s.lower() for s in r.tech_stack)
                or q in r.category.lower()
                or q in r.summary.lower()
            ]
        return roles

    def get_by_id(self, role_id: int) -> Optional[FDERole]:
        """Fetch a specific role by its numerical ID."""
        for role in self.load_roles():
            if role.id == role_id:
                return role
        return None
