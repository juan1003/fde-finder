import csv
import json
from datetime import datetime
from pathlib import Path
from typing import List, Union
from .models import FDERole

class Exporter:
    """
    Handles exporting role datasets to various file formats on the filesystem.
    Uses pathlib.Path to ensure directories and file paths are handled cleanly.
    """
    @staticmethod
    def export(roles: List[FDERole], target_path: Union[str, Path], file_format: str = "auto") -> Path:
        path = Path(target_path).resolve()
        # Ensure parent directories exist
        path.parent.mkdir(parents=True, exist_ok=True)

        if file_format == "auto":
            ext = path.suffix.lower()
            if ext == ".json":
                file_format = "json"
            elif ext == ".csv":
                file_format = "csv"
            else:
                file_format = "markdown"

        if file_format == "json":
            Exporter._export_json(roles, path)
        elif file_format == "csv":
            Exporter._export_csv(roles, path)
        else:
            Exporter._export_markdown(roles, path)

        return path

    @staticmethod
    def _export_json(roles: List[FDERole], path: Path) -> None:
        data = [r.to_dict() for r in roles]
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    @staticmethod
    def _export_csv(roles: List[FDERole], path: Path) -> None:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "ID", "Company", "Title", "Department", "Location",
                "RemoteFriendly", "CompRange", "Category", "TechStack", "ApplyURL"
            ])
            for r in roles:
                writer.writerow([
                    r.id, r.company, r.title, r.department, r.location,
                    r.remote_friendly, r.comp_range, r.category,
                    "; ".join(r.tech_stack), r.url
                ])

    @staticmethod
    def _export_markdown(roles: List[FDERole], path: Path) -> None:
        lines = [
            f"# Top Forward Deployed Engineer (FDE) Roles Hiring - {datetime.now().strftime('%B %Y')}\n",
            "| ID | Company | Role | Location | Est. Compensation | Domain |",
            "|---|---|---|---|---|---|"
        ]
        for r in roles:
            remote_tag = " (Remote OK)" if r.remote_friendly else ""
            lines.append(
                f"| {r.id} | **{r.company}** | [{r.title}]({r.url}) | {r.location}{remote_tag} | {r.comp_range} | {r.category} |"
            )

        lines.append("\n## Detailed Role Specifications\n")
        for r in roles:
            lines.extend([
                f"### {r.id}. {r.company}: {r.title}",
                f"- **Department**: {r.department}",
                f"- **Compensation**: {r.comp_range}",
                f"- **Tech Stack**: {', '.join(r.tech_stack)}",
                f"- **Overview**: {r.summary}",
                f"- **Apply Link**: [{r.url}]({r.url})\n"
            ])

        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
