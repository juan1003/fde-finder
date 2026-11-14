# Forward Deployed Engineer (FDE) Roles Tracker

A modular Python CLI application and data repository that tracks high-impact **Forward Deployed Engineer (FDE)** and **Forward Deployed Software Engineer (FDSE)** roles actively hiring across AI labs, enterprise software, and tech infrastructure pioneers.

---

## Project Structure

```text
some-program/
├── data/
│   └── fde_roles.json          # Formatted JSON dataset of active roles
├── fde_tracker/                # Core Python package
│   ├── __init__.py             # Package exports
│   ├── models.py               # FDERole dataclass schema & serializers
│   ├── repository.py           # Pathlib-based filesystem data access layer
│   ├── formatter.py            # ANSI-colored terminal table & detail viewer
│   └── exporter.py             # Export handlers (Markdown, CSV, JSON)
├── app.py                      # CLI entry point
├── pyproject.toml              # Standard PEP 517/621 packaging metadata
├── README.md                   # Project documentation
└── top_fde_roles.md            # Exported Markdown summary
```

---

## Features

- **Filesystem Decoupling**: Role data is stored in human-readable [data/fde_roles.json](file:///Users/juandejesus/Projects/some-program/data/fde_roles.json), separate from code logic.
- **Robust Pathlib Handling**: Uses Python's standard `pathlib.Path` to resolve files relative to package root, guaranteeing consistent execution from any working directory.
- **Typed Data Layer**: Uses `@dataclass` models (`FDERole`) for schema consistency and validation.
- **Rich CLI & Exporting**: Filter by remote work, company, tech stack keywords, or domain; inspect role specs; and export to JSON, Markdown, or CSV.

---

## Usage

### 1. Browse All Roles
```bash
python3 app.py
```

### 2. Remote & Keyword Filtering
```bash
# Only show remote-friendly opportunities
python3 app.py --remote

# Search by technology (e.g. Python, PyTorch, Next.js, Spark)
python3 app.py --query "Python"

# Filter by company
python3 app.py --company "Anthropic"

# Filter by domain category
python3 app.py --category "Frontier AI"
```

### 3. Detailed Role Breakdown
```bash
# View deep-dive requirements, tech stacks, and scope for a specific role ID
python3 app.py --detail 1
```

### 4. Data Exports & Custom Datasets
```bash
# Export to Markdown report
python3 app.py --export top_fde_roles.md

# Export to CSV spreadsheet
python3 app.py --export roles.csv

# Output as JSON (piping to jq)
python3 app.py --json

# Load a custom external dataset from the filesystem
python3 app.py --data /path/to/my_roles.json
```
