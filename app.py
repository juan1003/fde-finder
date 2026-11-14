#!/usr/bin/env python3
"""
Top Forward Deployed Engineer (FDE) Roles Tracker
CLI entry point that loads data from the filesystem repository.
"""

import sys
import json
import argparse
from pathlib import Path

from fde_tracker.repository import RoleRepository
from fde_tracker.formatter import print_banner, print_table, print_detail
from fde_tracker.exporter import Exporter

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Top Forward Deployed Engineer (FDE) Roles Hiring Tracker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 app.py                      # View all active FDE roles
  python3 app.py --remote             # Filter for remote-friendly roles
  python3 app.py --company "OpenAI"   # Filter by company name
  python3 app.py --query "Python"     # Search by keyword or tech stack
  python3 app.py --detail 1           # Inspect role ID 1 specifications
  python3 app.py --json               # Output as JSON
  python3 app.py --export roles.md    # Export report to Markdown
  python3 app.py --data custom.json   # Load from a custom dataset path
        """
    )
    parser.add_argument(
        "--data",
        "-d",
        type=Path,
        default=None,
        help="Custom filesystem path to the roles JSON dataset"
    )
    parser.add_argument(
        "--query",
        "-q",
        default=None,
        help="Search by keyword, tech stack, location, or focus"
    )
    parser.add_argument(
        "--company",
        "-c",
        default=None,
        help="Filter by company name"
    )
    parser.add_argument(
        "--category",
        default=None,
        help="Filter by domain/category (e.g., 'AI', 'Data', 'Trading')"
    )
    parser.add_argument(
        "--remote",
        "-r",
        action="store_true",
        help="Filter for remote-friendly roles only"
    )
    parser.add_argument(
        "--detail",
        type=int,
        metavar="ID",
        help="Show detailed specifications for a specific role ID"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print output in JSON format"
    )
    parser.add_argument(
        "--export",
        metavar="FILE",
        type=Path,
        help="Export results to a file (.md, .json, or .csv)"
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable ANSI colored output"
    )

    args = parser.parse_args()
    enable_color = not args.no_color

    # Initialize filesystem repository
    try:
        repo = RoleRepository(data_file=args.data)
        roles = repo.filter_roles(
            query=args.query,
            company=args.company,
            remote_only=args.remote,
            category=args.category
        )
    except FileNotFoundError as err:
        print(f"Filesystem Error: {err}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as err:
        print(f"Data Format Error: Failed to parse JSON: {err}", file=sys.stderr)
        sys.exit(1)

    # 1. JSON output flag
    if args.json:
        if args.detail:
            role = repo.get_by_id(args.detail)
            print(json.dumps(role.to_dict() if role else None, indent=2))
        else:
            print(json.dumps([r.to_dict() for r in roles], indent=2))
        return

    # 2. Export flag
    if args.export:
        target = Exporter.export(roles, args.export)
        print(f"Successfully exported {len(roles)} roles to {target}")
        return

    # 3. Detail inspect flag
    if args.detail:
        role = repo.get_by_id(args.detail)
        if not role:
            print(f"Error: Role with ID #{args.detail} not found.", file=sys.stderr)
            sys.exit(1)
        print_detail(role, enable_color)
        return

    # 4. Standard banner & table display
    print_banner(enable_color)
    print_table(roles, enable_color)

if __name__ == "__main__":
    main()
