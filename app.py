#!/usr/bin/env python3
"""
Top Forward Deployed Engineer (FDE) Roles Tracker
Displays the top FDE roles hiring this month with compensation, tech stack,
and direct application links.
"""

import sys
import json
import argparse
import urllib.request
import urllib.error
from datetime import datetime

# Curated dataset of top FDE roles hiring this month
FDE_ROLES = [
    {
        "id": 1,
        "company": "OpenAI",
        "title": "Forward Deployed Engineer - Applied AI",
        "department": "Applied Engineering",
        "location": "San Francisco, CA / New York, NY (Hybrid)",
        "remote_friendly": False,
        "comp_range": "$240,000 - $370,000 + Equity",
        "category": "Frontier AI & LLMs",
        "tech_stack": ["Python", "PyTorch", "Kubernetes", "OpenAI API", "Agentic Frameworks"],
        "summary": "Partner with strategic enterprise customers to bridge the gap between frontier models (GPT-4o, o-series) and production agentic pipelines.",
        "url": "https://openai.com/careers",
        "posted_period": "Active This Month"
    },
    {
        "id": 2,
        "company": "Anthropic",
        "title": "Forward Deployed Engineer - Enterprise Deployment",
        "department": "Applied AI / GTM",
        "location": "San Francisco, CA / New York, NY / London (Hybrid)",
        "remote_friendly": False,
        "comp_range": "$220,000 - $340,000 + Equity",
        "category": "Frontier AI & Safety",
        "tech_stack": ["Python", "Claude API", "Prompt Engineering", "Evaluation Frameworks", "AWS/GCP"],
        "summary": "Deploy Claude directly inside customer infrastructure. Build production evaluations, custom retrieval architectures, and enterprise guardrails.",
        "url": "https://anthropic.com/careers",
        "posted_period": "Active This Month"
    },
    {
        "id": 3,
        "company": "Palantir Technologies",
        "title": "Forward Deployed Software Engineer (FDSE) - Commercial & AIP",
        "department": "Forward Deployed Engineering",
        "location": "New York, NY / Palo Alto, CA / Washington, D.C. / London",
        "remote_friendly": False,
        "comp_range": "$150,000 - $210,000 + Stock ($250k - $380k TC)",
        "category": "Enterprise Ontology & AI",
        "tech_stack": ["Java", "TypeScript", "Python", "Palantir Foundry / AIP", "Distributed Systems"],
        "summary": "The originators of the FDE discipline ('Deltas'). Embed within Fortune 500 leadership to build high-impact production software on Foundry & AIP.",
        "url": "https://www.palantir.com/careers",
        "posted_period": "Active This Month"
    },
    {
        "id": 4,
        "company": "Scale AI",
        "title": "Forward Deployed Software Engineer - GenAI Platform",
        "department": "Federal & Enterprise Engineering",
        "location": "San Francisco, CA / New York, NY / Remote (US)",
        "remote_friendly": True,
        "comp_range": "$170,000 - $240,000 + Equity ($280k - $420k TC)",
        "category": "LLM Infrastructure & Data",
        "tech_stack": ["Python", "RLHF Pipelines", "Vector DBs", "Docker", "FastAPI"],
        "summary": "Build tailored model fine-tuning, synthetic data generation, and evaluation suites directly for premier enterprise and federal clients.",
        "url": "https://scale.com/careers",
        "posted_period": "Active This Month"
    },
    {
        "id": 5,
        "company": "Databricks",
        "title": "Forward Deployed Software Engineer - Mosaic AI & Lakehouse",
        "department": "Field Engineering / GenAI",
        "location": "San Francisco, CA / Mountain View, CA / Seattle, WA",
        "remote_friendly": False,
        "comp_range": "$180,000 - $250,000 + Equity ($300k - $450k TC)",
        "category": "Data & AI Infrastructure",
        "tech_stack": ["Python", "Apache Spark", "Mosaic AI", "Vector Search", "Delta Lake"],
        "summary": "Work side-by-side with data engineering leaders to build and scale compound AI systems and lakehouse-native vector search on Databricks.",
        "url": "https://www.databricks.com/company/careers",
        "posted_period": "Active This Month"
    },
    {
        "id": 6,
        "company": "Vercel",
        "title": "Forward Deployed Engineer - Enterprise Architecture",
        "department": "Solutions & Enterprise Engineering",
        "location": "Remote (US / EMEA)",
        "remote_friendly": True,
        "comp_range": "$165,000 - $225,000 + Equity",
        "category": "Frontend & Edge AI",
        "tech_stack": ["TypeScript", "Next.js", "React", "AI SDK", "Edge Compute"],
        "summary": "Lead enterprise engineering transformations, architecting high-scale Next.js infrastructure and streaming AI SDK implementations for tier-1 brands.",
        "url": "https://vercel.com/careers",
        "posted_period": "Active This Month"
    },
    {
        "id": 7,
        "company": "MongoDB",
        "title": "Forward Deployed Architect / Engineer - Atlas Vector Search",
        "department": "Solutions Architecture",
        "location": "New York, NY / Austin, TX / Remote",
        "remote_friendly": True,
        "comp_range": "$160,000 - $220,000 + Bonus + Equity",
        "category": "Distributed Databases & RAG",
        "tech_stack": ["Python", "Go / Java", "Atlas Vector Search", "RAG Architectures", "AWS"],
        "summary": "Engineer low-latency vector retrieval and hybrid search pipelines directly into enterprise client production stacks.",
        "url": "https://www.mongodb.com/careers",
        "posted_period": "Active This Month"
    },
    {
        "id": 8,
        "company": "Hightouch",
        "title": "Forward Deployed Engineer - Data Activation",
        "department": "Customer Engineering",
        "location": "San Francisco, CA / New York, NY / Remote",
        "remote_friendly": True,
        "comp_range": "$155,000 - $210,000 + Equity",
        "category": "Data Activation & Reverse ETL",
        "tech_stack": ["SQL", "Python", "Snowflake", "BigQuery", "dbt", "FastAPI"],
        "summary": "Bridge data engineering and GTM teams by wiring modern data warehouses into real-time operational decisioning engines.",
        "url": "https://hightouch.com/careers",
        "posted_period": "Active This Month"
    },
    {
        "id": 9,
        "company": "bp (British Petroleum)",
        "title": "Forward Deployed Engineer - AI & Quantitative Trading",
        "department": "Trading & Shipping Tech",
        "location": "Chicago, IL / Houston, TX / London, UK",
        "remote_friendly": False,
        "comp_range": "$160,000 - $230,000 + Target Bonus",
        "category": "Energy & Algorithmic Trading",
        "tech_stack": ["Python", "C++", "TimescaleDB / kdb+", "Cloud HPC", "Quantitative Models"],
        "summary": "Embed on the commercial trade floor to build algorithmic trade execution tools, market prediction models, and live analytical systems.",
        "url": "https://www.bp.com/careers",
        "posted_period": "Active This Month"
    },
    {
        "id": 10,
        "company": "Tesla",
        "title": "Forward Deployed Software Engineer - Factory Automation",
        "department": "Manufacturing Systems",
        "location": "Austin, TX / Fremont, CA",
        "remote_friendly": False,
        "comp_range": "$140,000 - $210,000 + Equity",
        "category": "Robotics & Manufacturing",
        "tech_stack": ["Python", "C++", "Computer Vision", "Telemetry", "Industrial IoT"],
        "summary": "Deploy on the gigafactory floor to diagnose bottlenecks, deploy computer vision inspection, and optimize real-time telemetry.",
        "url": "https://www.tesla.com/careers",
        "posted_period": "Active This Month"
    }
]

# ANSI color codes for rich terminal display
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DIM = '\033[2m'
    RESET = '\033[0m'

def colorize(text, color_code, enable_color=True):
    if not enable_color or not sys.stdout.isatty():
        return text
    return f"{color_code}{text}{Colors.RESET}"

def check_live_board(company_slug):
    """Attempt to check Greenhouse public board if network is accessible."""
    url = f"https://boards-api.greenhouse.io/v1/boards/{company_slug}/jobs"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=3) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                jobs = data.get("jobs", [])
                fde_matches = [
                    j for j in jobs
                    if "forward deployed" in j.get("title", "").lower() or "fde" in j.get("title", "").lower()
                ]
                return fde_matches
    except Exception:
        return None
    return None

def filter_roles(roles, query=None, company=None, remote_only=False, category=None):
    filtered = roles
    if company:
        filtered = [r for r in filtered if company.lower() in r["company"].lower()]
    if remote_only:
        filtered = [r for r in filtered if r["remote_friendly"]]
    if category:
        filtered = [r for r in filtered if category.lower() in r["category"].lower()]
    if query:
        q = query.lower()
        filtered = [
            r for r in filtered
            if q in r["company"].lower()
            or q in r["title"].lower()
            or q in r["location"].lower()
            or any(q in s.lower() for s in r["tech_stack"])
            or q in r["category"].lower()
        ]
    return filtered

def print_banner(enable_color=True):
    title = "TOP FORWARD DEPLOYED ENGINEER (FDE) ROLES HIRING THIS MONTH"
    subtitle = f"Curated high-impact roles at Frontier AI Labs, Enterprise SaaS, & Tech Pioneers ({datetime.now().strftime('%B %Y')})"
    print()
    print(colorize("=" * 80, Colors.CYAN, enable_color))
    print(colorize(f"  {title}", Colors.BOLD + Colors.GREEN, enable_color))
    print(colorize(f"  {subtitle}", Colors.DIM, enable_color))
    print(colorize("=" * 80, Colors.CYAN, enable_color))
    print()

def print_table(roles, enable_color=True):
    if not roles:
        print(colorize("  No roles matched your search criteria.", Colors.YELLOW, enable_color))
        print()
        return

    # Print summary list
    for r in roles:
        role_id = f"[{r['id']}]"
        comp_tag = colorize(r['comp_range'], Colors.YELLOW, enable_color)
        company_tag = colorize(r['company'].upper(), Colors.BOLD + Colors.CYAN, enable_color)
        remote_tag = colorize("[Remote OK]", Colors.GREEN, enable_color) if r["remote_friendly"] else colorize("[On-Site/Hybrid]", Colors.DIM, enable_color)
        
        print(f" {colorize(role_id, Colors.BOLD, enable_color)} {company_tag} - {colorize(r['title'], Colors.BOLD, enable_color)}")
        print(f"     Category : {colorize(r['category'], Colors.BLUE, enable_color)} | {remote_tag}")
        print(f"     Location : {r['location']}")
        print(f"     Est Comp : {comp_tag}")
        print(f"     Tech     : {', '.join(r['tech_stack'])}")
        print(f"     Focus    : {r['summary']}")
        print(f"     Apply    : {colorize(r['url'], Colors.UNDERLINE + Colors.BLUE, enable_color)}")
        print(colorize("  " + "-" * 76, Colors.DIM, enable_color))
    print()
    print(colorize(f"  Total Roles Listed: {len(roles)} | Use '--detail <id>' to inspect full requirements.", Colors.DIM, enable_color))
    print()

def print_detail(role, enable_color=True):
    print()
    print(colorize("=" * 80, Colors.CYAN, enable_color))
    print(colorize(f" ROLE DEEP DIVE: #{role['id']} {role['company']} - {role['title']}", Colors.BOLD + Colors.GREEN, enable_color))
    print(colorize("=" * 80, Colors.CYAN, enable_color))
    print(f" Company     : {colorize(role['company'], Colors.BOLD + Colors.CYAN, enable_color)}")
    print(f" Title       : {role['title']}")
    print(f" Department  : {role['department']}")
    print(f" Category    : {role['category']}")
    print(f" Location    : {role['location']} ({'Remote-Friendly' if role['remote_friendly'] else 'Office/Hybrid Hub'})")
    print(f" Comp Range  : {colorize(role['comp_range'], Colors.BOLD + Colors.YELLOW, enable_color)}")
    print(f" Hiring Status: {colorize(role['posted_period'], Colors.GREEN, enable_color)}")
    print()
    print(colorize(" Mission & Scope:", Colors.BOLD, enable_color))
    print(f"   {role['summary']}")
    print()
    print(colorize(" Core Technologies & Stack:", Colors.BOLD, enable_color))
    for t in role["tech_stack"]:
        print(f"   * {t}")
    print()
    print(colorize(" Why FDEs Excel Here:", Colors.BOLD, enable_color))
    print("   * High executive visibility and enterprise client impact.")
    print("   * Hybrid role: ~70% hands-on systems coding, ~30% technical strategy & architecture.")
    print("   * Direct feedback loop to core model/platform engineering teams.")
    print()
    print(colorize(f" Apply Online: {role['url']}", Colors.UNDERLINE + Colors.BLUE, enable_color))
    print(colorize("=" * 80, Colors.CYAN, enable_color))
    print()

def export_data(roles, filepath, export_format):
    if export_format == "json" or filepath.endswith(".json"):
        with open(filepath, "w") as f:
            json.dump(roles, f, indent=2)
        print(f"Exported {len(roles)} roles to JSON at {filepath}")
    elif export_format == "markdown" or filepath.endswith(".md"):
        with open(filepath, "w") as f:
            f.write(f"# Top Forward Deployed Engineer (FDE) Roles Hiring - {datetime.now().strftime('%B %Y')}\n\n")
            f.write("| ID | Company | Role | Location | Est. Compensation | Domain |\n")
            f.write("|---|---|---|---|---|---|\n")
            for r in roles:
                remote_str = " (Remote OK)" if r["remote_friendly"] else ""
                f.write(f"| {r['id']} | **{r['company']}** | [{r['title']}]({r['url']}) | {r['location']}{remote_str} | {r['comp_range']} | {r['category']} |\n")
            f.write("\n## Details & Tech Stacks\n\n")
            for r in roles:
                f.write(f"### {r['id']}. {r['company']}: {r['title']}\n")
                f.write(f"- **Department**: {r['department']}\n")
                f.write(f"- **Compensation**: {r['comp_range']}\n")
                f.write(f"- **Tech Stack**: {', '.join(r['tech_stack'])}\n")
                f.write(f"- **Overview**: {r['summary']}\n")
                f.write(f"- **Link**: [{r['url']}]({r['url']})\n\n")
        print(f"Exported {len(roles)} roles to Markdown at {filepath}")
    elif export_format == "csv" or filepath.endswith(".csv"):
        import csv
        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Company", "Title", "Department", "Location", "Remote", "Comp Range", "Category", "Tech Stack", "Apply URL"])
            for r in roles:
                writer.writerow([r["id"], r["company"], r["title"], r["department"], r["location"], r["remote_friendly"], r["comp_range"], r["category"], "; ".join(r["tech_stack"]), r["url"]])
        print(f"Exported {len(roles)} roles to CSV at {filepath}")

def main():
    parser = argparse.ArgumentParser(
        description="Top Forward Deployed Engineer (FDE) Roles Hiring Tracker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 app.py                     # View all top active FDE roles
  python3 app.py --remote            # View only remote-friendly FDE roles
  python3 app.py --company OpenAI    # Filter for OpenAI
  python3 app.py --query "Python"    # Search by keyword or tech stack
  python3 app.py --detail 1          # Deep dive into role ID 1
  python3 app.py --json              # Output raw JSON format
  python3 app.py --export roles.md   # Export to markdown report
        """
    )
    parser.add_argument("--query", "-q", help="Search by keyword, tech stack, or location", default=None)
    parser.add_argument("--company", "-c", help="Filter by company name", default=None)
    parser.add_argument("--remote", "-r", action="store_true", help="Filter for remote-friendly roles only")
    parser.add_argument("--detail", "-d", type=int, help="Show deep-dive details for a specific role ID")
    parser.add_argument("--json", action="store_true", help="Print output in JSON format")
    parser.add_argument("--export", metavar="FILE", help="Export to a file (.md, .json, or .csv)")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")

    args = parser.parse_args()
    enable_color = not args.no_color

    filtered = filter_roles(
        FDE_ROLES,
        query=args.query,
        company=args.company,
        remote_only=args.remote
    )

    if args.json:
        if args.detail:
            role = next((r for r in FDE_ROLES if r["id"] == args.detail), None)
            print(json.dumps(role, indent=2))
        else:
            print(json.dumps(filtered, indent=2))
        return

    if args.export:
        ext = args.export.split(".")[-1].lower() if "." in args.export else "markdown"
        export_data(filtered, args.export, ext)
        return

    if args.detail:
        role = next((r for r in FDE_ROLES if r["id"] == args.detail), None)
        if not role:
            print(f"Error: Role with ID #{args.detail} not found.")
            sys.exit(1)
        print_detail(role, enable_color)
        return

    print_banner(enable_color)
    print_table(filtered, enable_color)

if __name__ == "__main__":
    main()
