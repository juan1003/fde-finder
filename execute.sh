#!/bin/sh

# 1. Run standard display
python3 app.py

# 2. Filter for remote-friendly roles only
python3 app.py --remote

# 3. Search by keyword or tech stack (e.g. Python, Claude, Kubernetes)
python3 app.py --query "Python"

# 4. View deep-dive requirements and tech stacks for a role
python3 app.py --detail 1

# 5. Export to markdown or CSV
python3 app.py --export top_fde_roles.md
python3 app.py --export roles.csv

# 6. JSON output (piping into jq)
python3 app.py --json
